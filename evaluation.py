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
