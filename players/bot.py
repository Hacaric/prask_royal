from bot_api import run, log
from move import *

class Player:
    """
    This is place to write code of the bot.
    One instace of this class will be created and make_turn will be called when server expects bot input
    Returns: object of type Turn or type derived from Turn (such as EmptyTurn or PlaceTurn)
    """
    def __init__(self):
        self.turn = -1
    def make_turn(self, state):
        self.turn += 1
        if self.turn > 10:
        #     raise Exception("This is a test")
            return "string"
        turn = EmptyTurn()
        log(f"Sending move: {turn.parse()}")
        return turn


if __name__ == "__main__":
    run(Player())