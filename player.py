class Player:
    def __init__(self):
        self.initial_position = (0, 0)
        self.current_position = self.initial_position
        self.is_invincible = False
        self.speed = 10

    def move_left(self, speed):
        pass

    def move_right(self, speed):
        pass

    @property
    def player_speed(self):
        return self.speed
