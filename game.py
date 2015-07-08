from enum import Enum
from math import sqrt


class State(Enum):
    running = "running"
    won = "won"
    lost = "lost"
    paused = "paused"
    quit = "quit"


class Game:
    def __init__(self, field):
        self.field = field
        self.__state = State.running
        self.__game_speed = 630
        self.__level_speed = 30000
        self.__level = 1

    @property
    def dimensions(self):
        return (self.field.width, self.field.height)

    @property
    def is_lost(self):
        return self.__state is State.lost

    @property
    def is_paused(self):
        return self.__state is State.paused

    @property
    def is_running(self):
        return self.__state is State.running

    def pause(self):
        self.__state = State.paused

    def unpause(self):
        self.__state = State.running

    def set_speed(self, new_speed):
        self.__game_speed = new_speed

    def level_up(self):
        self.__level += 1

    def collision_detected(self, rect1, rect2):
        dx = (rect1.x + rect1.width / 2) - (rect2.x + rect2.width / 2)
        dy = (rect1.y + rect1.height / 2) - (rect2.y + rect2.height / 2)
        distance = sqrt(dx * dx + dy * dy)
        return distance < (rect1.width + rect2.width) / 2 - 4 or \
            distance < (rect1.height + rect2.height) / 2 - 10

        # cond1 = (abs(object1.x - object2.x) * 2 < (object1.width +
        #          object2.width))
        # cond2 = (abs(object1.y - object2.y) * 2 <
        #          (object1.height + object2.height - 10))
        # print(cond1, cond2)
        # return (abs(object1.x - object2.x) * 2 < (object1.width +
        #         object2.width)) and (abs(object1.y - object2.y) * 2 <
        #                              (object1.height + object2.height - 10))

        # return (rect1.x < rect2.x + rect2.width - 10 and
        #         rect1.x + rect1.width > rect2.x and
        #         rect1.y < rect2.y + rect2.height - 10 and
        #         rect1.height + rect1.y > rect2.y)

    @property
    def game_speed(self):
        return self.__game_speed

    @property
    def rock_speed(self):
        return self.field.rock_speed

    @property
    def player_speed(self):
        return self.field.player_speed

    @property
    def rocks(self):
        return self.field.rocks

    @property
    def level_speed(self):
        return self.__level_speed

    @property
    def level(self):
        return self.__level

    def set_rock_speed(self, new_speed):
        self.field.set_rock_speed(new_speed)

    @property
    def rock(self):
        return self.field.rock

    @property
    def player(self):
        return self.field.player

    @property
    def powerup(self):
        return self.field.powerup

    @property
    def player_invincibility_time(self):
        return self.field.player_invincibility_time

    @property
    def powerups(self):
        return self.field.powerups

    @property
    def bullet(self):
        return self.field.bullet

    @property
    def bullets(self):
        return self.field.bullets

    @property
    def bullet_speed(self):
        return self.field.bullet_speed
