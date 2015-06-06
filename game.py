from enum import Enum
from board import Board


class State(Enum):
    running = "running"
    won = "won"
    lost = "lost"
    paused = "paused"
    quit = "quit"


class Game:
    def __init__(self, board):
        self.board = board
        self.state = State.running
        self.speed = 1
        self.level = 1

    def dimensions(self):
        return (self.board.width, self.board.height)

    def is_lost(self):
        return self.state is State.lost

    def is_paused(self):
        return self.state is State.paused

    def is_running(self):
        return self.state is State.running

    def pause(self):
        self.state = State.paused

    def set_speed(self, new_speed):
        self.speed = new_speed

    def level_up(self):
        self.level += 1

    def key_press_event(self, event):
        pass

    def generate_powerups(self, position):
        pass

    def generate_rocks(self, position):
        pass

    def collison_detection(self):
        pass
