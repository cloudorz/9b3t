## Ultimate Tic-Tac-Toe 

#### An instruction on how to use this Ultimate Tic Tac Toe program:

Before running the code, make sure you have installed the following packages:
```
pip3 install pandas matplotlib glicko2
```

To run the program, you need to use the command line and provide specific arguments. The program offers three different modes of play: human vs AI, AI vs AI, and a competition mode. Here's how to use each mode:

1. Human vs AI mode:
   ```
   python3 main.py -m human [-l]
   ```
   - The `-m human` argument sets the mode to human vs AI.
   - The optional `-l` flag enables the "lite" version of the game.
   - After running this command, you'll be prompted to choose an AI opponent from a list.

2. AI vs AI mode:
   ```
   python3 main.py -m AI [-l]
   ```
   - The `-m AI` argument sets the mode to AI vs AI.
   - The optional `-l` flag enables the "lite" version of the game.
   - After running this command, you'll be prompted to choose two AI players to compete against each other.

3. Competition mode:
   ```
   python3 main.py -m competition [-l] [-t TURNS]
   ```
   - The `-m competition` argument sets the mode to competition.
   - The optional `-l` flag enables the "lite" version of the game.
   - The optional `-t TURNS` argument allows you to specify the number of turns for each matchup (default is 100).
   - This mode will run multiple games between different AI players and output the results.

Additional notes:
- The "lite" version (`-l` flag) changes the winning condition to any board in the nine boards, rather than the standard Ultimate Tic Tac Toe rules.
- In human vs AI mode, you'll play as the X player, and the AI will be the O player.
- The program uses various AI strategies, including Random, MiniMax with different depths and evaluation functions, and Monte Carlo Tree Search (MCTS) with different time limits.

#### An instruction on how to analyze the data:

**Prepare Your Data**:
   - Ensure you have a CSV file containing the match results for your players.
   - The CSV should have a structure where the first column contains player names, and subsequent columns represent matchups against other players.
   - Each cell should contain a string representation of a tuple with win data and duration data.

**Run the Script**:

   Basic usage:
   ```
   python data_analyze.py path/to/your/data.csv
   ```

   If you want to specify a custom number of turns (default is 100):
   ```
   python data_analyze.py path/to/your/data.csv --num_turns 200
   ```