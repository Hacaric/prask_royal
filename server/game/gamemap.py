import json
# from game._config import Settings

class Stucture:
    def __init__(self, type, x, y, health=None):
        self.x = x
        self.y = y
        self.type = type
        self.base_health = self.type.BASE_HEALTH
        if health:
            self.health = health
        else:
            self.health = self.type.BASE_HEALTH

    def parse(self):
        return json.dumps({
            'x':self.x,
            'y':self.y,
            'type':self.type.NAME,
            'health':self.health,
        })
def loadStructure(json_data):
    data = json.dumps(json_data)
    return Structure(data['type'], type['x'], type['y'], health=type['health'])

class Map:
    def __init__(self, game_map_config):
        self.width = game_map_config["width"]
        self.height = game_map_config["height"]
        # TODO : load structures from game_map_config
        self.map = [[[] for __ in range(height)] for _ in range(width)]
        self.map_structures = [[[] for __ in range(height)] for _ in range(width)]
        self.structures = []

        # self.structures = structures
        # for i in range(len(structures)):
        #     self.map_structures[struct.x][struct.y] = i
    def parsemap(self):
        return [str(self.width), str(self.height), json.dumps(self.map)]
    def new(self):
        return
        # for tower in Settings.Map.Structures.towers:
        #     self.structures.append(Stucture(tower["type"], tower["x"], tower["y"]))
        #     self.map_structures[tower["x"]][tower["y"]] = len(self.structures) - 1
        #     self.structures.append(Stucture(tower["type"], tower["x"], Settings.Map.height-tower["y"]))
        #     self.map_structures[tower["x"]][Settings.Map.height-tower["y"]] = len(self.structures) - 1
    def parse(self):
        return '\t'.join(self.parsemap() + [struct.parse() for struct in self.structures])
        
def loadMap(string_data):
    json_data = string_data.split('\t')
    width, height = int(json_data[0]), int(json_data[1])
    map_data = json.loads(json_data[2])
    # map_structures_data = json.loads(json_data[3])
    structures = [loadStructure(i) for i in json_data[3:]]
    gamemap = Map(width, height, structures=structures, gamemap=map_data)
