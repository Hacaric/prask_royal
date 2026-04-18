import entity_type

WIDTH = 11
HEIGHT = 25
class Settings:
    class Map:
        width = WIDTH
        height = HEIGHT
        class Structures:
            towers = [
                {"x":WIDTH//2,    "y":3, "type":entity_type.Tower},
                {"x":WIDTH//4,    "y":5, "type":entity_type.Tower},
                {"x":WIDTH//4*3,  "y":5, "type":entity_type.Tower},
            ]