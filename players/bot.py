from bot_api import run, log
from move import *

class Player:
    def __init__(self):
        self.turn = -1
    def make_turn(self, state):
        self.turn += 1
        if self.turn > 10:
            raise Exception("This is a test")
        turn = EmptyTurn()
        log(f"Sending move: {turn.parse()}")
        return turn


if __name__ == "__main__":
    run(Player())