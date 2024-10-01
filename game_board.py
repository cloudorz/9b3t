import math
import random
from enum import Enum


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
        if self.next_board_index is None or self.overall_board[self.next_board_index] != GameState.ONGOING:
            pairs = []
            for i in range(9):
                if self.overall_board[i] == GameState.ONGOING:
                    for j in range(9):
                        if self.boards[i][j] == CellState.EMPTY:
                            pairs.append((i, j))
            return pairs
        else:
            return [(self.next_board_index, j) for j in range(9) if self.boards[self.next_board_index][j] == CellState.EMPTY]
         
    
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
    


class EvaluationVersionOne:

    def __init__(self):
        self._win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]

    def evaluate(self, board):
        score = sum(map(self.evaluate_mini_board, board.boards))
        return score + self.evaluate_overall_board(board.overall_board)


    def evaluate_mini_board(self, board):
        score = 0
        for row in self._win_combinations:
            values = [board[i] for i in row]
            if values.count(CellState.X) == 3:
                score += 10
            elif values.count(CellState.O) == 3:
                score -= 10
            elif values.count(CellState.X) == 2 and values.count(CellState.EMPTY) == 1:
                score += 5
            elif values.count(CellState.O) == 2 and values.count(CellState.EMPTY) == 1:
                score -= 5
        
        return score


    def evaluate_overall_board(self, overall_board):
        score = 0
        for row in self._win_combinations:
            values = [overall_board[i] for i in row]
            if values.count(GameState.X_WIN) == 3:
                score += 100
            elif values.count(GameState.O_WIN) == 3:
                score -= 100
            elif values.count(GameState.X_WIN) == 2 and values.count(GameState.ONGOING) == 1:
                score += 50
            elif values.count(GameState.O_WIN) == 2 and values.count(GameState.ONGOING) == 1:
                score -= 50
        
        return score

class EvaluationVersionTwo:

    def __init__(self):
        self._win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
    
    def evaluate(self, board):
        score = sum(map(self.evaluate_mini_board, board.boards))
        return score + self.evaluate_overall_board(board.overall_board)


    def evaluate_mini_board(self, board):
        score = 0
        for row in self._win_combinations:
            values = [board[i] for i in row]
            if values.count(CellState.X) == 3:
                score += 10
            elif values.count(CellState.O) == 3:
                score -= 10
            elif values.count(CellState.X) == 2 and values.count(CellState.EMPTY) == 1:
                score += 5
            elif values.count(CellState.O) == 2 and values.count(CellState.EMPTY) == 1:
                score -= 5
            elif values.count(CellState.X) == 1 and values.count(CellState.EMPTY) == 2:
                score += 2
            elif values.count(CellState.O) == 1 and values.count(CellState.EMPTY) == 2:
                score -= 2
            
        if board[4] == CellState.X:
            score += 3  # Reward for X in the center
        elif board[4] == CellState.O:
            score -= 3  # Reward for O in the center
        
        return score


    def evaluate_overall_board(self, overall_board):
        score = 0
        for row in self._win_combinations:
            values = [overall_board[i] for i in row]
            if values.count(GameState.X_WIN) == 3:
                score += 100
            elif values.count(GameState.O_WIN) == 3:
                score -= 100
            elif values.count(GameState.X_WIN) == 2 and values.count(GameState.ONGOING) == 1:
                score += 50
            elif values.count(GameState.O_WIN) == 2 and values.count(GameState.ONGOING) == 1:
                score -= 50
            elif values.count(GameState.X_WIN) == 1 and values.count(GameState.ONGOING) == 2:
                score += 20
            elif values.count(GameState.O_WIN) == 1 and values.count(GameState.ONGOING) == 2:
                score -= 20
            
            if overall_board[4] == GameState.X_WIN:
                score += 10
            elif overall_board[4] == GameState.O_WIN:
                score -= 10
        
        return score


class MiniMaxPlayer:

    def __init__(self, name, evaluation, default_depth=6):
        self.name = name
        self.evaluation = evaluation
        self.default_depth = default_depth

    def max_value(self, board, depth, alpha, beta):
        if board.terminal() or depth == 0:
            return self.evaluation.evaluate(board)

        max_score = -math.inf
        for action in board.actions():
            board.make_move(*action)
            score = self.min_value(board, depth - 1, alpha, beta)
            board.undo_move(*action)
            max_score = max(score, max_score)
            alpha = max(score, alpha)
            if beta <= alpha:
                break

        return max_score


    def min_value(self, board, depth, alpha, beta):
        if board.terminal() or depth == 0:
            return self.evaluation.evaluate(board)

        min_score = math.inf
        for action in board.actions():
            board.make_move(*action)
            score = self.max_value(board, depth - 1, alpha, beta)
            board.undo_move(*action)
            min_score = min(score, min_score)
            beta = min(score, beta)
            if beta <= alpha:
                break
        
        return min_score


    def x_decision(self, board):
        depth = self.default_depth
        best_score = -math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf

        for action in board.actions():
            board.make_move(*action)
            score = self.min_value(board, depth - 1, alpha, beta)
            board.undo_move(*action)
            
            if score > best_score:
                best_score = score
                best_action = action
            
            alpha = max(alpha, best_score)
            
            if beta <= alpha:
                break

        return best_action


    def o_decision(self, board):
        depth = self.default_depth
        best_score = math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf

        for action in board.actions():
            board.make_move(*action)
            score = self.max_value(board, depth - 1, alpha, beta)
            board.undo_move(*action)

            if score < best_score:
                best_score = score
                best_action = action
            
            beta = min(beta, best_score)
            
            if beta <= alpha:
                break

        return best_action
    
    def make_decision(self, board):
        return self.x_decision(board) if board.current_player == CellState.X else self.o_decision(board)


class RandomPlayer:

    def __init__(self, name):
        self.name = name

    def make_decision(self, board):
        actions = board.actions()
        if actions:
            return random.choice(actions)
        else:
            return None


def play_game(x_player, o_player):
    board = NineBoard()
    settings = {GameState.X_WIN: x_player.name, GameState.O_WIN: o_player.name}

    while not board.terminal():
        best_move = x_player.make_decision(board) if board.current_player == CellState.X else o_player.make_decision(board)

        if best_move:
            board.make_move(*best_move)

        board.display_board()

    result = board.result()
    if result == GameState.DRAW:
        print("It's a draw!")
    else:
        print(f"{settings[result]} wins!")
    
    return result


if __name__ == '__main__':
    minimax_player_2 = MiniMaxPlayer('AI', EvaluationVersionTwo(), 6)
    minimax_player = MiniMaxPlayer('AI 2', EvaluationVersionOne(), 2)
    random_player = RandomPlayer('Random')
    _ = play_game(random_player, minimax_player)