import multiprocessing as mp
from itertools import product
import pandas as pd
from datetime import datetime

from game_board import NineBoard, GameState
from minimax import MiniMaxPlayer
from mcts import MCTSPlayer
from evaluation import Evaluation
from random_player import RandomPlayer
from human import HumanPlayer


def create_player_list(limit=None):
    players = [
        RandomPlayer('Random'),
        MiniMaxPlayer('AI D4E1', Evaluation(Evaluation.CONFIG_ONE), 4),
        MiniMaxPlayer('AI D4E2', Evaluation(Evaluation.CONFIG_TWO, True), 4),
        MiniMaxPlayer('AI D6E1', Evaluation(Evaluation.CONFIG_ONE), 6),
        MiniMaxPlayer('AI D6E2', Evaluation(Evaluation.CONFIG_TWO, True), 6),
        MiniMaxPlayer('AI D8E1', Evaluation(Evaluation.CONFIG_ONE), 8),
        MiniMaxPlayer('AI D8E2', Evaluation(Evaluation.CONFIG_TWO, True), 8),
        MCTSPlayer('MCTS 0.5s', 0.5),
        MCTSPlayer('MCTS 1.0s', 1.0),
        MCTSPlayer('MCTS 2.0s', 2.0),
    ]
    if limit is not None:
        return players[:limit]
    return players

def play_single_game(x_player, o_player, lite):
    board = NineBoard(lite)
    result, x_duration, o_duration = board.play_game(x_player, o_player)
    return result, x_duration, o_duration

def play_games_parallel(x_player, o_player, num_games, lite):
    with mp.Pool() as pool:
        results = pool.starmap(play_single_game, 
                               [(x_player, o_player, lite)] * num_games)
    
    x_wins = 0
    o_wins = 0
    x_total_duration = 0
    o_total_duration = 0
    for result, x_duration, o_duration in results:
        if result == GameState.X_WIN:
            x_wins += 1
        elif result == GameState.O_WIN:
            o_wins += 1
        x_total_duration += x_duration
        o_total_duration += o_duration
    
    average_x_duration = x_total_duration / num_games
    average_o_duration = o_total_duration / num_games
    
    return (x_wins, o_wins), average_x_duration, average_o_duration

def host_competition(participants, num_games, lite):
    total_results = []
    player_combinations = list(product(participants, repeat=2))
    
    for x_player, o_player in player_combinations:
        result = play_games_parallel(x_player, o_player, num_games, lite)
        total_results.append(result)
        
        (x_win, o_win), average_x_duration, average_o_duration = result
        print(f"{x_player.name} vs {o_player.name}: {x_win} - {o_win}")
        print(f"X Duration: {average_x_duration}")
        print(f"O Duration: {average_o_duration}")
        print()
    
    names = [p.name for p in participants]
    len_participants = len(participants)
    len_total_results = len(total_results)
    return (names, [total_results[i:i+len_participants] for i in range(0, len_total_results, len_participants)])


def run_competition(lite=False, turns=100):
    participants = create_player_list(8)
    names, total_results = host_competition(participants, turns, lite)

    # Create a figure and a set of subplots
    df = pd.DataFrame(total_results, index=names, columns=names)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f'data/results_compeition_a1_lite_{timestamp}.csv' if lite \
                else f'data/results_compeition_a1_{timestamp}.csv'
    df.to_csv(file_name, index=False)


def play_with_human(lite=False):
    players = create_player_list()
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
    players = create_player_list()
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
    parser.add_argument('-t', '--turns',
                        type=int,
                        default=100,
                        help='Number of turns to play in competition mode')

    args = parser.parse_args()

    if args.mode == 'human':
        play_with_human(args.lite)
    elif args.mode == 'AI':
        play_with_two_AIs(args.lite)
    elif args.mode == 'competition':
        run_competition(args.lite, args.turns)
