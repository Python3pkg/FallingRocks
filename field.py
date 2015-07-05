from player import Player
from rock import Rock


class Field:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rocks = []
        self.powerups = []
        self.player = Player()
        self.field = []
        self.rock = Rock()

    def clear_field(self):
        pass

    def get_object(self, x, y):
        return self.field[(y * self.width) + x]

    def set_rock_at_positon(self, x, y, rock):
        self.field[(y * self.width) + x] = rock

    def generate_powerup(self, position):
        pass

    def generate_rock(self, position):
        pass

    def set_rock_speed(self, new_speed):
        self.rock.set_speed(new_speed)

    @property
    def rock_speed(self):
        return self.rock.rock_speed

    @property
    def player_speed(self):
        return self.player.player_speed
