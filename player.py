class Player:
    def __init__(self):
        # self.initial_position = (0, 0)
        # self.current_position = self.initial_position
        self.__is_invincible = False
        # self.invincibility_time = 300
        self.__speed = 10

    # def move_left(self, speed):
    #     pass

    # def move_right(self, speed):
    #     pass

    def set_player_invinciblity(self):
        """Sets the player's invincibility to the opposite of the current
        value.
        """
        self.__is_invincible = not self.__is_invincible

    @property
    def player_speed(self):
        """Gets the player's speed."""
        return self.__speed

    @property
    def is_player_invincible(self):
        """Checks if the player is invincible"""
        return self.__is_invincible
