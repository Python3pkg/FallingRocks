from enum import Enum


class PowerupTypes(Enum):
    no_powerup = 0
    invinciblility = 1
    big_bomb = 2
    slow_down_rocks = 3


class PowerupDuration(Enum):
    no_duration = 0
    instant = 1
    small = 10
    medium = 20


class Powerup:
    def __init__(self, powerup_type):
        self.type = powerup_type
        self.duration = PowerupDuration.no_duration

    def set_duration(self, duration):
        self.duration = duration
