from game_board import NineBoard, GameState, CellState
from minimax import MiniMaxPlayer
from mcts import MCTSPlayer
from evaluation import EvaluationVersionOne, EvaluationVersionTwo
from random_player import RandomPlayer



if __name__ == '__main__':
    minimax_player_2 = MiniMaxPlayer('AI', EvaluationVersionTwo(), 6)
    minimax_player = MiniMaxPlayer('AI 2', EvaluationVersionOne(), -1) # -1 is default depth for complete search
    random_player = RandomPlayer('Random')
    mcts_player = MCTSPlayer('MCTS', 0.5, 1.4)
    board = NineBoard(lite=True)
    result, x_duration, o_duration = board.play_game(mcts_player, minimax_player, True)
    print(f"Result: {result}, X Duration: {x_duration}, O Duration: {o_duration}")