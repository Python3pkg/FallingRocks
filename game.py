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
        self.state = State.running
        self.speed = 1000
        self.level = 1

    @property
    def dimensions(self):
        return (self.field.width, self.field.height)

    @property
    def is_lost(self):
        return self.state is State.lost

    @property
    def is_paused(self):
        return self.state is State.paused

    @property
    def is_running(self):
        return self.state is State.running

    def pause(self):
        self.state = State.paused

    def unpause(self):
        self.state = State.running

    def set_speed(self, new_speed):
        self.speed = new_speed

    def level_up(self):
        self.level += 1

    def collison_detection(self):
        pass

    @property
    def game_speed(self):
        return self.speed

    @property
    def rock_speed(self):
        return self.field.rock_speed

    @property
    def rocks(self):
        return self.field.rocks
