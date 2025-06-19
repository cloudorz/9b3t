# Ultimate Tic-Tac-Toe

A comprehensive implementation of Ultimate Tic-Tac-Toe (also known as Nine Board Tic-Tac-Toe) with multiple AI agents including Minimax with alpha-beta pruning and Monte Carlo Tree Search (MCTS).

## About the Game

Ultimate Tic-Tac-Toe is a strategic variant of the classic game, played on a 3×3 grid of tic-tac-toe boards. Players must win individual boards to claim positions on the main board, with the ultimate goal of winning three boards in a row on the main grid.

## Features

- **Multiple AI Strategies**: Random, Minimax (various depths), and MCTS agents
- **Human vs AI Mode**: Play against sophisticated AI opponents
- **AI vs AI Mode**: Watch AI agents compete against each other  
- **Competition Mode**: Run tournaments between multiple AI agents
- **Performance Analysis**: Built-in tools for analyzing game results and AI performance
- **Lite Mode**: Alternative winning conditions for faster gameplay

[Detailed report](./9b3t_report.md) is available, including game rules, AI strategies, and performance analysis.

## Installation

Ensure you have Python 3.6+ installed, then install the required dependencies:

```bash
pip3 install pandas matplotlib glicko2
```

## Usage

The program offers three different modes of operation:

### 1. Human vs AI Mode

```bash
python3 main.py -m human [-l]
```

- **`-m human`**: Sets the mode to human vs AI
- **`-l`** (optional): Enables the "lite" version of the game
- You'll be prompted to choose an AI opponent from the available options
- You play as X, and the AI plays as O

### 2. AI vs AI Mode

```bash
python3 main.py -m AI [-l]
```

- **`-m AI`**: Sets the mode to AI vs AI
- **`-l`** (optional): Enables the "lite" version of the game  
- You'll be prompted to select two AI players to compete against each other
- Watch as different AI strategies battle it out

### 3. Competition Mode

```bash
python3 main.py -m competition [-l] [-t TURNS]
```

- **`-m competition`**: Runs a tournament between all AI players
- **`-l`** (optional): Enables the "lite" version of the game
- **`-t TURNS`** (optional): Number of games per matchup (default: 100)
- Results are saved to CSV files for further analysis

## Game Modes

- **Standard Mode**: Follow traditional Ultimate Tic-Tac-Toe rules
- **Lite Mode** (`-l` flag): Win by completing any of the nine boards (simplified winning condition)

## Available AI Agents

- **Random**: Makes random legal moves
- **Minimax**: Various depths (4, 6, 8) with two evaluation functions
- **MCTS**: Monte Carlo Tree Search with configurable time limits

## Data Analysis

After running competitions, you can analyze the results using the included data analysis script.

### Prerequisites

- Ensure you have a CSV file containing match results
- The CSV should have player names in the first column
- Subsequent columns represent matchups against other players
- Each cell contains win/loss data and timing information

### Usage

Basic analysis:
```bash
python data_analyze.py path/to/your/data.csv
```

With custom number of turns:
```bash
python data_analyze.py path/to/your/data.csv --num_turns 200
```

The script will generate:
- Performance charts and graphs
- Statistical analysis of AI effectiveness
- Comparative win rates and timing data
