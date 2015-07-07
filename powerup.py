from enum import IntEnum
import random


class PowerupType(IntEnum):
    no_powerup = 0
    invinciblility = 1
    big_bomb = 2
    slow_down_rocks = 3


class PowerupDuration(IntEnum):
    no_duration = 0
    instant = 10
    small = 10000
    medium = 20000


class PowerupTimeInterval(IntEnum):
    no_time_interval = 0
    small = 10000
    medium = 15000
    big = 20000
    test = 4000


class Powerup:
    def __init__(self, type):
        self.type = type
        self.duration = PowerupDuration.no_duration

    def set_duration(self, powerup_type):
        # self.duration = new_duration
        if powerup_type == PowerupType.invinciblility:
            self.duration = PowerupDuration.small
        elif powerup_type == PowerupType.big_bomb:
            self.duration = PowerupDuration.instant
        elif powerup_type == PowerupType.slow_down_rocks:
            self.duration = PowerupDuration.medium

    def set_random_position(self, max_value):
        return random.randint(1, max_value)
