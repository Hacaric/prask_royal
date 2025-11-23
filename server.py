from _config import Settings
from _stats import Stats


class Stucture:
    def __init__(self, type, x, y):
        self.x = x
        self.y = y
        self.type = type
        self.health = self.type.health
        self.base_health = self.type.health
class Map:
    def __init__(self, width = Settings.Map.width, height = Settings.Map.height):
        self.width = width
        self.height = height
        self.map = [[[] for __ in range(height)] for _ in range(width)]
        self.map_structures = [[[] for __ in range(height)] for _ in range(width)]
        self.structures = []
        for tower in Settings.Map.Structures.towers:
            self.structures.append(Stucture(tower["type"], tower["x"], tower["y"]))
            self.map_structures[tower["x"]][tower["y"]] = len(self.structures) - 1
            self.structures.append(Stucture(tower["type"], tower["x"], Settings.Map.height-tower["y"]))
            self.map_structures[tower["x"]][Settings.Map.height-tower["y"]] = len(self.structures) - 1
class Game:
    def __init__(self, map_:Map):
        self.map = map_
    def gameTurn(self, turn1, turn2):
        pass