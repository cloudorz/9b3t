import random

class RandomPlayer:
    def __init__(self, name):
        self.name = name

    def make_decision(self, board):
        actions = board.actions()
        if actions:
            return random.choice(actions)
        else:
            return None
