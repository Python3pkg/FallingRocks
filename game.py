from enum import Enum


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
        self.__level_speed = 35000
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

    def collison_detection(self):
        pass

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
