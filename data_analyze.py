import pandas as pd
from glicko2 import Player
import matplotlib.pyplot as plt
from matplotlib.table import Table
import ast

# Load your data (replace with your actual data path)

def extract_wins(cell_value):
    if isinstance(cell_value, str):
        wins_data = ast.literal_eval(cell_value)
        if isinstance(wins_data, tuple):
            return wins_data[0][0], wins_data[0][1]  # X wins, O wins
    return 0, 0


def extract_durations(cell_value):
    if isinstance(cell_value, str):
        data = ast.literal_eval(cell_value)
        if isinstance(data, tuple):
            return data[1], data[2]
    return 0, 0


def analyze_glicko2(data, total_games=100):
    # Initialize Glicko-2 players (default rating 1500, RD 350, volatility 0.06)
    glicko_players = {player: Player() for player in data.columns[1:]}

    # Iterate through the matchups and update Glicko-2 ratings
    for i, player_row in data.iterrows():
        player = player_row['Unnamed: 0']  # The player in the row
        for opponent in data.columns[1:]:
            if player != opponent: # Skip the same player
                # Extract number of X and O wins
                x_wins, o_wins = extract_wins(player_row[opponent])

                # Player as X and opponent as O
                num_draws = total_games - x_wins - o_wins
                x_win_rate = (x_wins + num_draws * 0.5) / total_games
                o_win_rate = (o_wins + num_draws * 0.5) / total_games

                # Update Glicko-2 ratings for both players
                x_player = glicko_players[player]
                o_player = glicko_players[opponent]

                # Update ratings based on match outcome
                x_player.update_player([o_player.rating], [o_player.rd], [x_win_rate])
                o_player.update_player([x_player.rating], [x_player.rd], [o_win_rate])

    # Extract and display the Glicko-2 ratings
    for player, player_obj in glicko_players.items():
        print(f"Player: {player}, Rating: {player_obj.rating}, RD: {player_obj.rd}, Volatility: {player_obj.vol}")


    ratings = [player_obj.rating for player_obj in glicko_players.values()]
    player_names = list(glicko_players.keys())
    plt.figure(figsize=(10, 6))
    plt.bar(player_names, ratings, color='b')
    plt.axhline(y=1500, color='r', linestyle='--')  # Horizontal line at y=1500
    plt.title('Skill level of participants (Glicko-2 Ratings)')
    plt.xlabel('Participants')
    plt.ylabel('Rating')
    plt.show()

    # Extract the data from the csv file as {(player 1, player 2): (x_wins, o_wins)}
def show_matchup_data(data):
    player_names = data.columns[1:]
    matchup_data = [[extract_wins(player_row[opponent]) for opponent in data.columns[1:]] for _, player_row in data.iterrows()]
    
    # Create a DataFrame with player names as index and columns
    df = pd.DataFrame(matchup_data, index=player_names, columns=player_names)
    
    # Display the matchup data as a table
    plt.figure(figsize=(12, 8))
    plt.axis('off')
    plt.title('Matchup Data Table')
    
    # Create a table and add it to the plot
    table = plt.table(cellText=df.values,
                      rowLabels=df.index,
                      colLabels=df.columns,
                      cellLoc='center',
                      loc='center')
    
    # Adjust table properties for better readability
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.2)
    
    # Add color coding based on win ratios
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            cell = table[i+1, j]
            x_wins, o_wins = df.iloc[i, j]
            total = x_wins + o_wins
            if total > 0:
                win_ratio = x_wins / total
                cell_color = plt.cm.RdYlGn(win_ratio)
                cell.set_facecolor(cell_color)
    
    plt.tight_layout()
    plt.show()

def show_compared_data(data, baseline_name, total_games=100):
    player_names = data.columns[1:]
    matchup_data = [[extract_wins(player_row[opponent]) for opponent in data.columns[1:]] for _, player_row in data.iterrows()]
    baseline = {}
    n = len(player_names)
    for i in range(n):
        for j in range(i+1, n):
            i_name = player_names[i]
            j_name = player_names[j]
            if i_name == j_name:
                continue
            elif i_name == baseline_name:
                win_rate = baseline.get(j_name)
                x_wins, o_wins = matchup_data[i][j]
                num_draws = total_games - x_wins - o_wins
                current_win_rate = (o_wins + num_draws * 0.5) / total_games

                baseline[j_name] = (win_rate + current_win_rate) / 2 if win_rate is not None else current_win_rate
            elif j_name == baseline_name:
                win_rate = baseline.get(i_name)
                x_wins, o_wins = matchup_data[i][j]
                num_draws = total_games - x_wins - o_wins
                current_win_rate = (x_wins + num_draws * 0.5) / total_games
                baseline[i_name] = (win_rate + current_win_rate) / 2 if win_rate is not None else current_win_rate


    # Plotting the baseline data with win rates displayed on each bar
    plt.figure(figsize=(10, 6))
    bars = plt.bar(baseline.keys(), baseline.values(), color='skyblue')
    plt.title(f'Baseline Win Rates ({baseline_name})')
    plt.xlabel('Opponent')
    plt.ylabel('Win Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Displaying win rates on each bar
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')

    plt.show()

def show_durations(data, total_games=100):
    player_names = data.columns[1:]
    matchup_data = [[extract_durations(player_row[opponent]) for opponent in data.columns[1:]] for _, player_row in data.iterrows()]
    durations = {}
    n = len(player_names)
    for i, x_name in enumerate(player_names):
        for j, o_name in enumerate(player_names):
            x_duration, o_duration = matchup_data[i][j]
            saved_duration = durations.get(x_name)
            if saved_duration is None:
                durations[x_name] = x_duration
            else:
                durations[x_name] = (saved_duration + x_duration) / 2
            saved_duration = durations.get(o_name)
            if saved_duration is None:
                durations[o_name] = o_duration
            else:
                durations[o_name] = (saved_duration + o_duration) / 2

    plt.figure(figsize=(10, 6))
    bars = plt.bar(durations.keys(), durations.values(), color='skyblue')
    plt.title('Average time per game')
    plt.xlabel('Participants')
    plt.ylabel('Time (s)')

    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')

    plt.show()




if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze Glicko-2 ratings from a CSV file.")
    parser.add_argument("file_path", type=str, help="Path to the CSV file containing match results.")
    parser.add_argument("--num_turns", type=int, required=False, default=100, help="Total number of games played.")
    args = parser.parse_args()

    data = pd.read_csv(args.file_path)
    show_matchup_data(data)
    analyze_glicko2(data, args.num_turns)
    show_compared_data(data, "Random")
    show_compared_data(data, "MCTS 0.5s")
    show_compared_data(data, "AI D8E2")
    show_durations(data, args.num_turns)