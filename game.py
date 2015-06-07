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
        self.speed = 1
        self.level = 1
        self.ui = None

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

    def set_speed(self, new_speed):
        self.speed = new_speed

    def level_up(self):
        self.level += 1

    def generate_powerup(self, position):
        pass

    def generate_rock(self, position):
        pass

    def collison_detection(self):
        pass
