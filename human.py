
class HumanPlayer:
    def __init__(self):
        self.name = None

    def make_decision(self, board):
        if self.name is None:
            self.name = input("Enter your name: ")

        valid_actions = board.actions()
        print("Valid moves:")
        for action in valid_actions:
            print(f"Row: {action[0]}, Column: {action[1]}")
        move = input(f"{self.name} enter your move (row, column): ")
        move = tuple(map(int, move.split(',')))

        return move