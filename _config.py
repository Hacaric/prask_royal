class Settings:
    class Map:
        width = 11
        height = 25
        class Structures:
            towers = [
                {"x":super.width//2,    "y":3, "type":0},
                {"x":super.width//4,    "y":5, "type":1},
                {"x":super.width//4*3,  "y":5, "type":1},
            ]