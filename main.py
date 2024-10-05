from game_board import NineBoard, GameState
from minimax import MiniMaxPlayer
from mcts import MCTSPlayer
from evaluation import Evaluation
from random_player import RandomPlayer
import multiprocessing as mp
from itertools import product
import pandas as pd
from human import HumanPlayer

def play_single_game(x_player, o_player, lite):
    board = NineBoard(lite)
    result, x_duration, o_duration = board.play_game(x_player, o_player)
    return result, x_duration, o_duration

def play_games_parallel(x_player, o_player, num_games, lite):
    with mp.Pool() as pool:
        results = pool.starmap(play_single_game, 
                               [(x_player, o_player, lite)] * num_games)
    
    wins = sum(result[0] == GameState.X_WIN for result in results)
    x_total_duration = sum(result[1] for result in results)
    o_total_duration = sum(result[2] for result in results)
    
    win_rate = wins / num_games
    average_x_duration = x_total_duration / num_games
    average_o_duration = o_total_duration / num_games
    
    return win_rate, average_x_duration, average_o_duration

def host_competition(participants, num_games=100, lite=False):
    total_results = []
    player_combinations = list(product(participants, repeat=2))
    
    for x_player, o_player in player_combinations:
        result = play_games_parallel(x_player, o_player, num_games, lite)
        total_results.append(result)
        
        win_rate, average_x_duration, average_o_duration = result
        print(f"{x_player.name} vs {o_player.name}: Win Rate: {win_rate}")
        print(f"X Duration: {average_x_duration}")
        print(f"O Duration: {average_o_duration}")
        print()
    
    names = [p.name for p in participants]
    return (names, [total_results[i:i+len(participants)] for i in range(0, len(total_results), len(participants))])


def run_competition(lite=False):
    participants = [
        RandomPlayer('Random'),
        MiniMaxPlayer('AI Eval 1_4', Evaluation(Evaluation.CONFIG_ONE), 4),
        MiniMaxPlayer('AI Eval 2_4', Evaluation(Evaluation.CONFIG_TWO, True), 4),
        MiniMaxPlayer('AI Eval 1_6', Evaluation(Evaluation.CONFIG_ONE), 6),
        MiniMaxPlayer('AI Eval 2_6', Evaluation(Evaluation.CONFIG_TWO, True), 6),
        MiniMaxPlayer('AI Eval 1_8', Evaluation(Evaluation.CONFIG_ONE), 8),
        MiniMaxPlayer('AI Eval 2_8', Evaluation(Evaluation.CONFIG_TWO, True), 8),
        MCTSPlayer('MCTS 0.5s', 0.5),
        # MCTSPlayer('MCTS 1.0s', 1.0),
        # MCTSPlayer('MCTS 2.0s', 2.0),
    ]

    names, total_results = host_competition(participants, 100, lite)

    # Create a figure and a set of subplots
    df = pd.DataFrame(total_results, index=names, columns=names)
    print(df.to_csv())


def play_with_human(lite=False):
    players = [
        RandomPlayer('Random'),
        MiniMaxPlayer('AI Eval 1_4', Evaluation(Evaluation.CONFIG_ONE), 4),
        MiniMaxPlayer('AI Eval 2_4', Evaluation(Evaluation.CONFIG_TWO, True), 4),
        MiniMaxPlayer('AI Eval 1_6', Evaluation(Evaluation.CONFIG_ONE), 6),
        MiniMaxPlayer('AI Eval 2_6', Evaluation(Evaluation.CONFIG_TWO, True), 6),
        MiniMaxPlayer('AI Eval 1_8', Evaluation(Evaluation.CONFIG_ONE), 8),
        MiniMaxPlayer('AI Eval 2_8', Evaluation(Evaluation.CONFIG_TWO, True), 8),
        MCTSPlayer('MCTS 0.5s', 0.5),
        MCTSPlayer('MCTS 1.0s', 1.0),
        MCTSPlayer('MCTS 2.0s', 2.0),
    ]
    print("Choose a player to play against:")
    for i, player in enumerate(players):
        print(f"{i+1}. {player.name}")
    choice = int(input("Enter the number of the player: ")) - 1
    if 0 <= choice < len(players):
        opponent = players[choice]
    else:
        print("Invalid choice. Defaulting to MCTS 0.5s.")
        opponent = players[5]
    board = NineBoard(lite)
    board.display_board()
    human_player = HumanPlayer()
    result, x_duration, o_duration = board.play_game(human_player, opponent, show_board=True)
    print(f"Result: {GameState.to_str(result)}, X Duration: {x_duration}, O Duration: {o_duration}")
    if result == GameState.X_WIN:
        print(human_player.name + " wins!")
    elif result == GameState.O_WIN:
        print(opponent.name + " wins!")
    else:
        print("Draw!")


def play_with_two_AIs(lite=False):
    players = [
        RandomPlayer('Random'),
        MiniMaxPlayer('AI Eval 1_4', Evaluation(Evaluation.CONFIG_ONE), 4),
        MiniMaxPlayer('AI Eval 2_4', Evaluation(Evaluation.CONFIG_TWO, True), 4),
        MiniMaxPlayer('AI Eval 1_6', Evaluation(Evaluation.CONFIG_ONE), 6),
        MiniMaxPlayer('AI Eval 2_6', Evaluation(Evaluation.CONFIG_TWO, True), 6),
        MiniMaxPlayer('AI Eval 1_8', Evaluation(Evaluation.CONFIG_ONE), 8),
        MiniMaxPlayer('AI Eval 2_8', Evaluation(Evaluation.CONFIG_TWO, True), 8),
        MCTSPlayer('MCTS 0.5s', 0.5),
        MCTSPlayer('MCTS 1.0s', 1.0),
        MCTSPlayer('MCTS 2.0s', 2.0),
    ]
    print("Choose two players to play against each other:")
    for i, player in enumerate(players):
        print(f"{i+1}. {player.name}")
    player1_choice = int(input("Enter the number of the first player: ")) - 1
    player2_choice = int(input("Enter the number of the second player: ")) - 1
    if 0 <= player1_choice < len(players) and 0 <= player2_choice < len(players):
        player1 = players[player1_choice]
        player2 = players[player2_choice]
    else:
        print("Invalid choice. Defaulting to MCTS 0.5s vs Random.")
        player1 = players[5]
        player2 = players[0]
    board = NineBoard(lite)
    board.display_board()
    result, x_duration, o_duration = board.play_game(player1, player2, show_board=True)
    print(f"Result: {GameState.to_str(result)}, X Duration: {x_duration}, O Duration: {o_duration}")
    if result == GameState.X_WIN:
        print(player1.name + " wins!")
    elif result == GameState.O_WIN:
        print(player2.name + " wins!")
    else:
        print("Draw!")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Play Ultimate Tic Tac Toe')
    parser.add_argument('-m', '--mode',
                        choices=['human', 'AI', 'competition'], 
                        required=True, 
                        help='Choose the play mode: human, AI, or competition')
    parser.add_argument('-l', '--lite',
                        action='store_true',
                        help='Play a lite game with winning condition on any board in nine boards')

    args = parser.parse_args()

    if args.mode == 'human':
        play_with_human(args.lite)
    elif args.mode == 'AI':
        play_with_two_AIs(args.lite)
    elif args.mode == 'competition':
        run_competition(args.lite)
