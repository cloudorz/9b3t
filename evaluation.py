from game_board import GameState, CellState

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
        for i, j, k in self._win_combinations:
            total = board[i] + board[j] + board[k]
            if total == 15:
                score += 10
            elif total == 6:
                score -= 10
            elif total == 10:
                score += 5
            elif total == 4:
                score -= 5
        
        return score


    def evaluate_overall_board(self, overall_board):
        score = 0
        for i, j, k in self._win_combinations:
            total = overall_board[i] + overall_board[j] + overall_board[k]
            if total == 15:
                score += 100
            elif total == 6:
                score -= 100
            elif total == 10:
                score += 50
            elif total == 4:
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
        for i, j, k in self._win_combinations:
            total = board[i] + board[j] + board[k]
            if total == 15:
                score += 10
            elif total == 6:
                score -= 10
            elif total == 10:
                score += 5
            elif total == 4:
                score -= 5
            elif total == 5:
                score += 2
            elif total == 2:
                score -= 2
            
        if board[4] == CellState.X:
            score += 3  # Reward for X in the center
        elif board[4] == CellState.O:
            score -= 3  # Reward for O in the center
        
        return score


    def evaluate_overall_board(self, overall_board):
        score = 0
        for i, j, k in self._win_combinations:
            total = overall_board[i] + overall_board[j] + overall_board[k]
            if total == 15:
                score += 100
            elif total == 6:
                score -= 100
            elif total == 10:
                score += 50
            elif total == 4:
                score -= 50
            elif total == 5:
                score += 20
            elif total == 2:
                score -= 20
            
            if overall_board[4] == GameState.X_WIN:
                score += 10
            elif overall_board[4] == GameState.O_WIN:
                score -= 10
        
        return score
