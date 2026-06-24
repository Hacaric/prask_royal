import json

class Turn:
    """
    The base class for turn types.

    Can't be used directly, serves as template for turn types.
    
    Other turn types are child types of the Turn class
    """
    movetype = None
    def __init__(self, *args):
        raise Exception("Cannot create instance of class Turn, this only template. Try using class inherited from it, eg. PlaceTurn, EmptyTurn, ...")
    def parse(self):
        return None

class PlaceTurn(Turn):
    """
    Turn of type PlaceTurn places a card of type `card` to coordinates `x` and `y` of the map
    """
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
    """
    Turn of type EmptyTurn informs the server, that the client is alive, but doesn't want to peform any action
    """
    movetype = "EmptyTurn"
    def __init__(self):pass
    def parse(self):return json.dumps({"MOVE":self.movetype})

class EmojiTurn(Turn):
    """
    Turn of type EmojiTurn shows an emoji
    """
    movetype = "EmojiTurn"
    def __init__(self, emoji_id):
        self.emoji_id = emoji_id
    def parse(self):
        return json.dumps({"MOVE":self.movetype, "id":self.emoji_id})