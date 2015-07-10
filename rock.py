# from enum import Enum
# from gui import RockUI
import random


# class RockShape(Enum):
#     no_shape = 0
#     vertical_rock = 1
#     horizontal_rock = 2
#     big_rock = 3


# class RockColor(Enum):
#     white = 0
#     grey = 1
#     black = 2


class Rock:
    def __init__(self):
        # self.shape = RockShape.no_shape
        # self.color = RockColor.white
        # self.speed = 90
        self.__speed = 50
        # self.__x = 0
        # self.__y = 0

        # self.ui = RockUI()

    # def shape(self):
    #     return self.pieceShape

    def set_random_position(self, max_value):
        """Sets a random number from 10 to max_value which is used for setting
        the position of the rock.
        """
        return random.randint(10, max_value)

    def set_random_shape(self, max_value):
        """Sets a random number from 1 to max_value which is used for setting
        the shape of the rock.
        """
        return random.randint(1, max_value)

    # def set_random_color(self):
    #     pass

    # def x(self):
    #     return self.position[0]

    # def y(self):
    #     return self.position[1]

    # def fall_down(self):
    #     pass

    def set_speed(self, new_speed):
        """Sets the rock's speed to the value of new_speed."""
        self.__speed = new_speed

    @property
    def rock_speed(self):
        """Gets the rock's speed."""
        return self.__speed
