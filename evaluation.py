import functools
from game_board import GameState, CellState

class Evaluation:
    CONFIG_ONE = {
        'score_map': {
            15: 10,
            6: -10,
            10: 5,
            4: -5,
        },
        'overall_score_map': {
            15: 100,
            6: -100,
            10: 50,
            4: -50,
        }
    }
    CONFIG_TWO = {
        'score_map': {
            15: 10,
            6: -10,
            10: 5,
            4: -5,
            5: 2,
            2: -2,
        },
        'overall_score_map': {
            15: 100,
            6: -100,
            10: 50,
            4: -50,
            5: 20,
            2: -20,
        }
    }

    def __init__(self, config, bonus=False):
        self._win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        self.score_map = config['score_map']
        self.overall_score_map = config['overall_score_map']
        self.bonus = bonus


    def evaluate(self, board):
        score = 0
        for mini_board in board.boards:
            score += self.evaluate_mini_board(tuple(mini_board))
            
        return score + self.evaluate_overall_board(tuple(board.overall_board))


    @functools.lru_cache(maxsize=None)
    def evaluate_mini_board(self, board):
        score = self._evaluate_board(board, self.score_map)

        if self.bonus:
            if board[4] == CellState.X:
                score += 3
            elif board[4] == CellState.O:
                score -= 3

        return score
    

    def _evaluate_board(self, board, score_map):
        score = 0
        for i, j, k in self._win_combinations:
            score += score_map.get(board[i] + board[j] + board[k], 0)

        return score


    @functools.lru_cache(maxsize=None)
    def evaluate_overall_board(self, overall_board):
        score = self._evaluate_board(overall_board, self.overall_score_map)
        if self.bonus:
            if overall_board[4] == GameState.X_WIN:
                score += 10
            elif overall_board[4] == GameState.O_WIN:
                score -= 10

        return score
