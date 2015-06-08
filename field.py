from player import Player


class Field:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rocks = []
        self.powerups = []
        self.player = Player()
        self.field = []

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
