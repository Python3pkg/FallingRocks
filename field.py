from player import Player
from rock import Rock
from powerup import Powerup, PowerupType
from bullet import Bullet


class Field:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rocks = []
        self.powerups = []
        self.bullets = []
        self.__player = Player()
        # self.field = []
        self.__rock = Rock()
        self.__powerup = Powerup(PowerupType.no_powerup)
        self.__bullet = Bullet()

    def clear_field(self):
        pass

    def get_object(self, x, y):
        return self.field[(y * self.width) + x]

    # def set_rock_at_positon(self, x, y, rock):
    #     self.field[(y * self.width) + x] = rock

    def generate_powerup(self, position):
        pass

    def generate_rock(self, position):
        pass

    def set_rock_speed(self, new_speed):
        self.rock.set_speed(new_speed)

    @property
    def rock_speed(self):
        return self.__rock.rock_speed

    @property
    def player_speed(self):
        return self.__player.player_speed

    @property
    def player(self):
        return self.__player

    @property
    def rock(self):
        return self.__rock

    @property
    def powerup(self):
        return self.__powerup

    @property
    def bullet(self):
        return self.__bullet

    @property
    def bullet_speed(self):
        return self.__bullet.bullet_speed

    @property
    def player_invincibility_time(self):
        return self.__player.player_invincibility_time
