from game_board import NineBoard, GameState, CellState
from minimax import MiniMaxPlayer
from mcts import MCTSPlayer
from evaluation import EvaluationVersionOne, EvaluationVersionTwo
from random_player import RandomPlayer



# def play_game(x_player, o_player):
#     board = NineBoard()
#     settings = {GameState.X_WIN: x_player.name, GameState.O_WIN: o_player.name}

#     while not board.terminal():
#         best_move = x_player.make_decision(board) if board.current_player == CellState.X else o_player.make_decision(board)

#         if best_move:
#             board.make_move(*best_move)

#         # board.display_board()

#     result = board.result()
#     if result == GameState.DRAW:
#         print("It's a draw!")
#     else:
#         print(f"{settings[result]} wins!")
    
#     return result




if __name__ == '__main__':
    minimax_player_2 = MiniMaxPlayer('AI', EvaluationVersionTwo(), 6)
    minimax_player = MiniMaxPlayer('AI 2', EvaluationVersionOne(), 4)
    random_player = RandomPlayer('Random')
    mcts_player = MCTSPlayer('MCTS', 1, 1.4)
    board = NineBoard()
    result, x_duration, o_duration = board.play_game(mcts_player, random_player)
    print(f"Result: {result}, X Duration: {x_duration}, O Duration: {o_duration}")


