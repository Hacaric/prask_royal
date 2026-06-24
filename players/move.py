import json

class Turn:
    """
    The base class for turn types.

    Can't be used directly, serves as template for turn types.
    
    Other turn types are inherited from the Turn class
    """
    movetype = None
    def __init__(self, *args):
        raise Exception("Cannot create instance of class Turn, this only template. Try using class inherited from it, eg. PlaceTurn, EmptyTurn, ...")
    def parse(self):
        return None
        # This didn't work, because it tried to parse 'self' and who knows what else, im not gonna hardcode it
        return json.dumps({key:val for key, val in vars().items() if not "__" in key})
class PlaceTurn(Turn):
    movetype = "PlaceTurn"
    def __init__(self, x, y, card):
        self.x = x
        self.y = y
        self.card = card
    def parse(self):
        return json.dumps({
            "MOVE":self.movetype,
            "x":self.x,
            "y":self.y,
            "card":self.card
        })
class EmptyTurn(Turn):
    movetype = "EmptyTurn"
    def __init__(self):pass
    def parse(self):return json.dumps({"MOVE":self.movetype})