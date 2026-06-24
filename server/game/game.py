from game.gamemap import *
import json, os
stats_filename = os.path.join(os.path.dirname(__file__), "stats.json")

class Game:
    def __init__(self, log, playerIDlist, game_map_config):
        self.map = Map(game_map_config)
        self.log = log
        self.playerIDlist = playerIDlist
        self.alive_players = {i:True for i in playerIDlist}

        self.log("Game.__init__: Loading stats.json...")
        with open(stats_filename, "r") as f:
            self.stats = json.load(f)
        self.log("Game.__init__: Loaded stats succesfully...")

    def executeTurn(self, turns, player_id) -> None:
        # Move logic
        if not (player_id in self.alive_players and self.alive_players[player_id]):
            return
        return
    def parse(self, playerID) -> str:
        """
            Returns game state in json format (string)
            If playerID is None, all data will be returned
            If playerID is valid ID, data visible to the player will be returned
        """
        if playerID == None: # Print data to observer - get data from ALL players, IMPORTANT: make sure no playerID is None
            map_data = self.map.parseAll()
        else:
            map_data = self.map.parse(playerID)

        json_data = {"map":map_data}
        json_data = json.dumps(json_data)
        return json_data

    def removePlayer(self, playerID) -> None:
        """
        Makes player unable to play (marks as dead, all futher moves will be refused)
        """
        self.alive_players[playerID] = False
        return

    def tick(self) -> None:
        """
        Ticks the board, its entities, updates elixir status, refills avaible cards, etc. 
        Intended use: When all players played their moves and we need to actually make the game run
        """ 
        return

    def should_stop_game(self, round:int) -> bool:
        if not any(list(self.alive_players.values())):
            self.log("No players alive: stopping game...")
            return True
        if round > 20:
            self.log("Stopping after 20th turn for testing prusposes...")
            return True
        return False
    
    def getScore(self) -> dict:
        return {}