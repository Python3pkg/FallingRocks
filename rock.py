from enum import Enum
# from gui import RockUI


class RockShape(Enum):
    no_shape = 0
    vertical_rock = 1
    horizontal_rock = 2
    big_rock = 3


# class RockColor(Enum):
#     white = 0
#     grey = 1
#     black = 2


class Rock:
    def __init__(self):
        self.shape = RockShape.no_shape
        # self.color = RockColor.white
        self.speed = 90
        # self.ui = RockUI()

    def shape(self):
        return self.pieceShape

    def set_shape(self, shape):
        pass

    def set_random_shape(self):
        pass

    def set_random_color(self):
        pass

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def fall_down(self):
        pass

    @property
    def rock_speed(self):
        return self.speed
