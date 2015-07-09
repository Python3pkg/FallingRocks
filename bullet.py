class Bullet:
    def __init__(self):
        # self.shape = RockShape.no_shape
        # self.color = RockColor.white
        # self.speed = 90
        self.__speed = 50

        # self.ui = RockUI()

    # def shape(self):
    #     return self.pieceShape

    # def x(self):
    #     return self.position[0]

    # def y(self):
    #     return self.position[1]

    def set_speed(self, new_speed):
        self.__speed = new_speed

    @property
    def bullet_speed(self):
        return self.__speed
