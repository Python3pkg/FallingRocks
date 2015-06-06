import sys
from game import State
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget
from PyQt5.QtGui import QIcon


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

        self.com = Communicate()
        self.statusbar = self.statusBar()
        self.com.message_statusbar[str].connect(self.statusbar.showMessage)
        self.com.message_statusbar.emit("New game")

        self.resize(game.dimensions()[0], game.dimensions()[1])
        self.center()
        self.setWindowIcon(QIcon('small_icon.png'))
        self.setWindowTitle('Falling Rocks')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class Communicate(QObject):
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    pause = pyqtSignal()
    message_statusbar = pyqtSignal(str)


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
        if not self.game.is_running():
            return

        key = event.key()

        if key == Qt.Key_P:
            self.game.pause()
            return
        if self.self.game.is_paused():
            return
        elif key == Qt.Key_Left:
            pass
        elif key == Qt.Key_Right:
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
        self.com = Communicate()
        self.com.move_left.connect(self.move_left)
        self.com.move_right.connect(self.move_right)

    def draw(self, position):
        pass

    def move_left(self, speed):
        pass

    def move_right(self, speed):
        pass
