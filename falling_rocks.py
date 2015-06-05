from board import Board
from game import Game
import gui


def main():
    board = Board(1080, 800)
    game = Game(board)
    ui = gui.UserInterface(game)
    ui.main_loop()

if __name__ == '__main__':
    main()
