from field import Field
from game import Game
import gui


def main():
    field = Field(1080, 800)
    game = Game(field)
    game.ui = gui.UserInterface(game)
    game.ui.main_loop()

if __name__ == '__main__':
    main()
