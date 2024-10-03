import math
from evaluation import EvaluationVersionOne, EvaluationVersionTwo
from game_board import CellState, NineBoard, GameState
from random_player import RandomPlayer


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
    


if __name__ == '__main__':
    wins = 0
    minimax_player = MiniMaxPlayer('AI', EvaluationVersionOne(), 4)
    random_player = RandomPlayer('Random')
    x_total_duration = 0
    o_total_duration = 0
    for _ in range(100):
        board = NineBoard()
        result, x_duration, o_duration = board.play_game(minimax_player, random_player)
        if result == GameState.X_WIN:
            wins += 1
        x_total_duration += x_duration
        o_total_duration += o_duration
    print(f"Win rate for Minimax Player vs Random Player: {wins / 100 * 100}%")
    print(f"Average duration for X: {x_total_duration / 100}")
    print(f"Average duration for O: {o_total_duration / 100}")