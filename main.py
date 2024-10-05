from game_board import NineBoard, GameState
from minimax import MiniMaxPlayer
from mcts import MCTSPlayer
from evaluation import Evaluation
from random_player import RandomPlayer


def host_competition(participants, num_games=100, lite=False):
    total_results = []
    for x_player in participants:
        results = []
        for o_player in participants:
            wins = 0
            x_total_duration = 0
            o_total_duration = 0
            for _ in range(num_games):
                board = NineBoard(lite)
                result, x_duration, o_duration = board.play_game(x_player, o_player)
                if result == GameState.X_WIN:
                    wins += 1
                x_total_duration += x_duration
                o_total_duration += o_duration

            average_x_duration = x_total_duration / num_games
            average_o_duration = o_total_duration / num_games
            win_rate = wins / num_games
            results.append((win_rate, average_x_duration, average_o_duration))
            print(f"{x_player.name} vs {o_player.name}: Win Rate: {win_rate}")
            print(f"X Duration: {average_x_duration}")
            print(f"O Duration: {average_o_duration}")
        total_results.append(results)
        
    names = [p.name for p in participants]

    return (names, total_results) 


if __name__ == '__main__':
    import pandas as pd
    import cProfile
    import pstats
    import io

    def main():
        participants = [
            RandomPlayer('Random'),
            # MiniMaxPlayer('AI Eval 1_4', Evaluation(Evaluation.CONFIG_ONE), 4),
            # MiniMaxPlayer('AI Eval 2_4', Evaluation(Evaluation.CONFIG_TWO, True), 4),
            # MiniMaxPlayer('AI Eval 1_6', EvaluationVersionOne(), 6),
            MiniMaxPlayer('AI Eval 2_6', Evaluation(Evaluation.CONFIG_TWO, True), 8),
            # MCTSPlayer('MCTS 0.5s', 0.5),
            # MCTSPlayer('MCTS 1.0s', 1.0),
            # MCTSPlayer('MCTS 2.0s', 2.0),
        ]

        names, total_results = host_competition(participants, 3)

        # Create a figure and a set of subplots
        df = pd.DataFrame(total_results, index=names, columns=names)
        print(df.to_csv())
    
   # Run the profiler
    profiler = cProfile.Profile()
    profiler.run('main()')

    # Analyze and display profiling results
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    stats.print_stats(20)  # Print top 20 time-consuming functions
    print(s.getvalue())

    # Optionally, save profiling results to a file
    stats.dump_stats('profile_results.prof')
    print("Detailed profiling results saved to 'profile_results.prof'")

