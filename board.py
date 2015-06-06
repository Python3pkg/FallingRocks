from enum import Enum


class Board:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rocks = []
        self.powerups = []
        self.player = Player()

    def clear_board(self):
        pass

    def rock_at_positon(self, x, y):
        pass

    def set_rock_at_positon(self, x, y, shape):
        pass

    def generate_rocks(self):
        pass


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


class PowerupTypes(Enum):
    no_powerup = 0
    invinciblility = 1
    big_bomb = 2
    slow_down_rocks = 3


class PowerupDuration(Enum):
    no_duration = 0
    invinciblility = 10
    big_bomb = 1
    slow_down_rocks = 20


class Powerup:
    def __init__(self, type):
        self.type = type
        self.duration = PowerupDuration.no_duration

    def set_duration(self, duration):
        self.duration = duration


class Player:
    def __init__(self):
        self.initial_position = (0, 0)
        self.current_position = self.initial_position
        self.is_invincible = False
        self.speed = 1

    def move(self, direction, speed):
        pass
