from bot_api import run, log
from move import *

class Player:
    def make_turn(self, state):
        turn = EmptyTurn()
        log(f"Sending move: {turn.parse()}")
        return turn


if __name__ == "__main__":
    run(Player())