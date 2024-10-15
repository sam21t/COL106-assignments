from enum import Enum

class Color(Enum):
    BLUE = 1
    YELLOW = 2
    RED = 3
    GREEN = 4
    

class Object:
    def __init__(self, object_id, size, color, bin_id = None):
        self.id = object_id
        self.capacity = size
        self.color = color
        self.storage = bin_id