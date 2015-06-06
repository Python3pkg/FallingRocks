import sys
from game import State
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget


class UserInterface:
    def __init__(self, game):
        self.game = game

    def main_loop(self):
        app = QApplication(sys.argv)
        self.main_window = MainWindow(self.game)
        app.exec_()


class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.board = Board(self, self.game)

        self.setCentralWidget(self.board)

        self.resize(game.dimensions()[0], game.dimensions()[1])
        self.center()
        self.setWindowTitle('Falling Rocks')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class Communicate(QObject):
    pass


class Board(QFrame):
    def __init__(self, parent, game):
        super().__init__()
        self.game = game
        self.width, self.height = self.game.dimensions()

    def draw(self):
        pass

    def paintEvent(self, event):
        pass

    def keyPressEvent(self, event):
        pass

    def timerEvent(self, event):
        pass


class Rock:
    def __init__(self):
        pass

    def draw(self, position):
        pass

    def fall_down(self):
        pass


class Powerup:
    def __init__(self):
        pass

    def draw(self, position):
        pass

    def fall_down(self):
        pass


class Player:
    def __init__(self):
        pass

    def draw(self, position):
        pass
