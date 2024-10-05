from enum import Enum
import time


class CellState:
    X = 5
    O = 2
    EMPTY = 0

    @staticmethod
    def to_str(state):
        if state == CellState.X:
            return 'X'
        elif state == CellState.O:
            return 'O'
        else:
            return ' '

class GameState:
    ONGOING = 0
    X_WIN = 5
    O_WIN = 2
    DRAW = -16

    @staticmethod
    def to_str(state):
        if state == GameState.X_WIN:
            return 'X wins'
        elif state == GameState.O_WIN:
            return 'O wins'
        elif state == GameState.DRAW:
            return 'Draw'
        else:
            return 'Game is still ongoing'

class NineBoard:
    def __init__(self, lite=False):
        self.boards = [[CellState.EMPTY for _ in range(9)] for _ in range(9)]
        self.overall_board = [GameState.ONGOING for _ in range(9)]
        self.current_player = CellState.X
        self.next_board_index = None
        self.lite = lite
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
            return [(i, j) for i in range(9) 
                    if self.overall_board[i] == GameState.ONGOING
                    for j in range(9) 
                    if self.boards[i][j] == CellState.EMPTY]
        else:
            return [(self.next_board_index, j) for j in range(9) 
                    if self.boards[self.next_board_index][j] == CellState.EMPTY]

    
    def update_game_state(self, board_index):
        self.overall_board[board_index] = self.update_mini_board_game_state(board_index)

    
    def display_board(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    triple = self.boards[i*3 + k][j*3:j*3+3]
                    print(f"{[CellState.to_str(v) for v in triple]}", end=" | ")
                print()
            print('-' * 50)
        print('=' * 50)


    def terminal(self):
        return self.result() != GameState.ONGOING

    
    def result(self):
        if self.lite:
            if GameState.X_WIN in self.overall_board:
                return GameState.X_WIN
            elif GameState.O_WIN in self.overall_board:
                return GameState.O_WIN
        else:
            for i, j, k in self._win_combinations:
                v1, v2, v3 = self.overall_board[i], self.overall_board[j], self.overall_board[k]
                if v1 == v2 == v3:
                    return v1
        
        if GameState.ONGOING in self.overall_board:
            return GameState.ONGOING
        else:
            return GameState.DRAW


    def copy(self):
        new_board = NineBoard(lite=self.lite)
        new_board.boards = [board[:] for board in self.boards]
        new_board.overall_board = self.overall_board[:]
        new_board.current_player = self.current_player
        new_board.next_board_index = self.next_board_index
        return new_board


    def update_mini_board_game_state(self, board_index):
        board = self.boards[board_index]

        for i, j, k in self._win_combinations:
            total = board[i] + board[j] + board[k]
            if total == 15:
                return GameState.X_WIN
            elif total == 6:
                return GameState.O_WIN
        
        if CellState.EMPTY in board:
            return GameState.ONGOING
        else:
            return GameState.DRAW
    
    def play_game(self, x_player, o_player, show_board=False):
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
            
            if show_board:
                self.display_board()

        return self.result(), x_duration, o_duration
