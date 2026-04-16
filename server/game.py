class Game:
    def __init__(self, map_:Map, log, playerIDlist):
        self.map = map_
        self.log = log
        self.playerIDlist = playerIDlist
    def executeTurn(self, turns, player_id):
        # for playerID, turn in enumerate(turns):
            if self.validateTurn(playerID, turn):
                self.executeTurn(playerID, turn)
            else:
                self.log(f"Invalid turn from player: {playerID}")
    def parse(self):
        return self.map.parse()
    def removePlayer(self, playerID):
        pass #TODO
