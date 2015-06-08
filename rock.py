from enum import Enum


class RockShape(Enum):
    no_shape = 0
    vertical_rock = 1
    horizontal_rock = 2
    big_rock = 3


class Rock:
    def __init__(self, position):
        self.rock_shape = RockShape.no_shape
        self.position = position

    def shape(self):
        return self.pieceShape

    def set_shape(self, shape):
        pass

    def set_random_shape(self):
        pass

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def fall_down(self):
        pass
