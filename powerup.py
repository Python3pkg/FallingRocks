from enum import IntEnum
import random


class PowerupType(IntEnum):
    no_powerup = 0
    player_invinciblility = 1
    big_bomb = 2
    slow_down_rocks = 3
    shoot_rocks = 4


class PowerupDuration(IntEnum):
    no_duration = 0
    instant = 10
    small = 10 * 1000
    medium = 20 * 1000
    big = 30 * 1000


class PowerupTimeInterval(IntEnum):
    no_time_interval = 0
    second = 1000
    small = 12413
    medium = 34847
    big = 47093
    very_big = 74051
    huge = 101009


class Powerup:
    def __init__(self, type):
        self.type = type
        self.duration = PowerupDuration.no_duration
        # self.ticker = 0

    def set_duration(self, powerup_type):
        """Sets the duration of powerup types."""
        if powerup_type == PowerupType.invinciblility:
            self.duration = PowerupDuration.small
        elif powerup_type == PowerupType.big_bomb:
            self.duration = PowerupDuration.instant
        elif powerup_type == PowerupType.slow_down_rocks:
            self.duration = PowerupDuration.medium

    def set_random_position(self, max_value):
        """Sets a random number from 10 to max_value which is used for setting
        the position of the powerup.
        """
        return random.randint(10, max_value)
