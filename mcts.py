import math
import random
import time
from game_board import GameState, CellState, NineBoard


class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.score = 0

    def add_child(self, child_board, move):
        child = MCTSNode(child_board, self, move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.score += result

    def fully_expanded(self):
        return len(self.children) == len(self.board.actions())

    def best_child(self, c_param=1.4): # c_param is a constant that balances exploitation and exploration. 2**0.5 for pure UCB1
        choices_weights = [
            (c.score / c.visits) + c_param * ((math.log(self.visits) / c.visits) ** 0.5) # UCB1 formula
            for c in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]


class MCTSPlayer:
    def __init__(self, name, time_limit=1, c_param=1.4):
        self.name = name
        self.time_limit = time_limit
        self.c_param = c_param
        self.root = None

    def make_decision(self, board):
        self.root = MCTSNode(board)
        end_time = time.time() + self.time_limit

        while time.time() < end_time:
            leaf = self.select(self.root)
            child = self.expand(leaf)
            result = self.simulate(child)
            self.backpropagate(child, result)

        return max(self.root.children, key=lambda c: c.visits).move

    def select(self, node):
        while not node.board.terminal():
            if not node.fully_expanded():
                return node
            node = node.best_child(self.c_param)
        return node

    def expand(self, node):
        if node.board.terminal():
            return node
        
        existing_moves = [c.move for c in node.children]
        for action in node.board.actions():
            if action not in existing_moves:
                new_board = node.board.copy()
                new_board.make_move(*action)
                return node.add_child(new_board, action)
        return node  # In case all actions are expanded

    def simulate(self, node):
        board = node.board.copy()
        while not board.terminal():
            action = random.choice(board.actions())
            board.make_move(*action)
        result = board.result()
        
        if result == GameState.DRAW:
            return 0.5
        elif board.current_player == CellState.O and result == GameState.X_WIN or \
            board.current_player == CellState.X and result == GameState.O_WIN:
            return 1
        else:
            return 0

    def backpropagate(self, node, result):
        while node is not None:
            node.update(result)
            node = node.parent
            result = 1 - result  # Flip the result for the opponent 0 -> 1, 1 -> 0


def test_c_values(opponent, duration=1, num_games=100):
    c_values = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
    results = {}

    for c in c_values:
        mcts_player = MCTSPlayer('MCTS', duration, c)
        wins = 0
        x_total_duration = 0
        o_total_duration = 0
        for _ in range(num_games):
            board = NineBoard(lite=True)
            result, x_duration, o_duration = board.play_game(mcts_player, opponent)
            if result == GameState.X_WIN:
                wins += 1
            x_total_duration += x_duration
            o_total_duration += o_duration
        results[c] = wins / num_games
        print(f"MCTS Player {c} wins: {wins}")
        print(f"Average duration for X: {x_total_duration / num_games}")
        print(f"Average duration for O: {o_total_duration / num_games}")

    return results

if __name__ == '__main__':
    from random_player import RandomPlayer
    import matplotlib.pyplot as plt

    random_player = RandomPlayer('Random')
    results = test_c_values(random_player, 0.5, 100)
    print(results)
    # You might want to plot these results

    c_values = list(results.keys())
    win_rates = list(results.values())

    plt.figure(figsize=(10, 6))
    plt.plot(c_values, win_rates, marker='o', linestyle='-', color='b')
    plt.title('Win Rate vs C-Value for MCTS Player')
    plt.xlabel('C-Value')
    plt.ylabel('Win Rate')
    plt.grid(True)
    plt.show()
