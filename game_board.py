from enum import Enum
import time


class CellState(Enum):
    X = 'X'
    O = 'O'
    EMPTY = ' '

    def __str__(self):
        return str(self.value)

class GameState(Enum):
    ONGOING = ' '
    X_WIN = 'X'
    O_WIN = 'O'
    DRAW = 'D'

    def __str__(self):
        return str(self.value)

class NineBoard:
    def __init__(self):
        self.boards = [[CellState.EMPTY for _ in range(9)] for _ in range(9)]
        self.overall_board = [GameState.ONGOING for _ in range(9)]
        self.current_player = CellState.X
        self.next_board_index = None
        self._win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

    
    def make_move(self, board_index, cell_index):
        self.boards[board_index][cell_index] = self.current_player
        self.current_player = CellState.X if self.current_player == CellState.O else CellState.O
        self.update_game_state(board_index)

        self.next_board_index = cell_index

    
    def undo_move(self, board_index, cell_index):
        self.current_player = self.boards[board_index][cell_index]
        self.boards[board_index][cell_index] = CellState.EMPTY
        self.update_game_state(board_index)

        self.next_board_index = board_index


    def actions(self):
        if self.next_board_index is None or \
           self.overall_board[self.next_board_index] != GameState.ONGOING:
            pairs = []
            for i in range(9):
                if self.overall_board[i] == GameState.ONGOING:
                    for j in range(9):
                        if self.boards[i][j] == CellState.EMPTY:
                            pairs.append((i, j))
            return pairs
        else:
            actions = []
            for j in range(9):
                if self.boards[self.next_board_index][j] == CellState.EMPTY:
                    actions.append((self.next_board_index, j))
            return actions
         
    
    def update_game_state(self, board_index):
        self.overall_board[board_index] = self.update_mini_board_game_state(board_index)

    
    def display_board(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    triple = self.boards[i*3 + k][j*3:j*3+3]
                    print(f"{[str(v) for v in triple]}", end=" | ")
                print()
            print('-' * 50)
        print('=' * 50)


    def terminal(self):
        return self.result() != GameState.ONGOING

    
    def result(self):
        for row in self._win_combinations:
            values = [self.overall_board[i] for i in row]
            if values.count(GameState.X_WIN) == 3:
                return GameState.X_WIN
            elif values.count(GameState.O_WIN) == 3:
                return GameState.O_WIN
        
        if GameState.ONGOING in self.overall_board:
            return GameState.ONGOING
        else:
            return GameState.DRAW


    def copy(self):
        new_board = NineBoard()
        new_board.boards = [self.boards[i][:] for i in range(9)]
        new_board.overall_board = self.overall_board[:]
        new_board.current_player = self.current_player
        new_board.next_board_index = self.next_board_index

        return new_board


    def update_mini_board_game_state(self, board_index):
        board = self.boards[board_index]

        for row in self._win_combinations:
            values = [board[i] for i in row]
            if values.count(CellState.X) == 3:
                return GameState.X_WIN
            elif values.count(CellState.O) == 3:
                return GameState.O_WIN
        
        if CellState.EMPTY in board:
            return GameState.ONGOING
        else:
            return GameState.DRAW
    
    def play_game(self, x_player, o_player):
        x_duration = 0.0
        o_duration = 0.0
        while not self.terminal():
            best_move = None
            if self.current_player == CellState.X:
                start_time = time.time()
                best_move = x_player.make_decision(self)
                x_duration += time.time() - start_time
            else:
                start_time = time.time()
                best_move = o_player.make_decision(self)
                o_duration += time.time() - start_time

            if best_move:
                self.make_move(*best_move)
            
        return self.result(), x_duration, o_duration
