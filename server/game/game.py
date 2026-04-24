from game.gamemap import *
import json

class Game:
    def __init__(self, log, playerIDlist, game_map_config):
        self.map = Map(game_map_config)
        self.log = log
        self.playerIDlist = playerIDlist
        self.alive_players = {i:True for i in range(len(playerIDlist))}
    def executeTurn(self, turns, player_id):
        # Move logic
        return
    def parse(self, playerID):
        """
            Returns game state in json format (string)
        """
        if playerID == None: # Print data to observer - get data from ALL players, IMPORTANT: make sure no playerID is None
            map_data = self.map.parseAll()
        else:
            map_data = self.map.parse(playerID)

        json_data = {"map":map_data}
        json_data = json.dumps(json_data)
        return json_data

    def removePlayer(self, playerID):
        self.alive_players[playerID] = False
        return

    def should_stop_game(self, round:int):
        if not any(list(self.alive_players.values())):
            self.log("No players alive: stopping game...")
            return True
        if round > 20:
            self.log("Stopping after 20th turn for testing prusposes...")
            return True
        return False
    
    def getScore(self):
        return {}