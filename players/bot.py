from bot_api import run, log
from turn_type import *

class Player:
    """
    This is place to write code of the bot.
    One instace of this class will be created and make_turn will be called when server expects bot input
    Returns: instance of child type of Turn, eg. instance of EmptyTurn or PlaceTurn
    """
    def __init__(self):
        self.turn = -1
    def make_turn(self, state):
        self.turn += 1
        if self.turn > 10:
        #     raise Exception("This is a test")
            return "Example of invalid return value."
        turn = EmptyTurn()
        log(f"Sending move: {turn.parse()}")
        return turn


if __name__ == "__main__":
    run(Player())