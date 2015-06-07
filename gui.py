from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget
from PyQt5.QtGui import QIcon


class UserInterface:
    def __init__(self, game):
        self.game = game

    def main_loop(self):
        app = QApplication([])
        self.main_window = MainWindow(self.game)
        app.exec_()


class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.field_ui = FieldUI(self, self.game)

        self.set_dimensions()

        self.init_status_bar()

        self.setWindowIcon(QIcon('small_icon.png'))
        self.setWindowTitle('Falling Rocks')
        self.show()

    def center_window(self):
        self.setCentralWidget(self.field_ui)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def init_status_bar(self):
        self.communicate = Communicate()
        self.statusbar = self.statusBar()
        self.communicate.message_statusbar[str].\
            connect(self.statusbar.showMessage)
        self.communicate.message_statusbar.emit("New game")

    def set_dimensions(self):
        self.height = self.game.dimensions()[0]
        self.width = self.game.dimensions()[1]
        self.resize(self.height, self.width)
        self.center_window()


class Communicate(QObject):
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    pause = pyqtSignal()
    message_statusbar = pyqtSignal(str)


class FieldUI(QFrame):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.width, self.height = self.game.dimensions()
        self.communicate = Communicate()
        self.setFocusPolicy(Qt.StrongFocus)

    def draw(self):
        pass

    def paintEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if not self.game.is_running:
            super(FieldUI, self).keyPressEvent(event)
            return

        key = event.key()
        if key == Qt.Key_P:
            self.game.pause()
            return
        if self.game.is_paused:
            return
        elif key == Qt.Key_Left:
            self.communicate.move_left.emit()
        elif key == Qt.Key_Right:
            self.communicate.move_right.emit()

    def timerEvent(self, event):
        pass


class RockUI:
    def __init__(self, game):
        pass

    def draw(self, position):
        pass

    def fall_down(self):
        pass


class PowerupUI:
    def __init__(self, game):
        pass

    def draw(self, position):
        pass

    def fall_down(self):
        pass


class PlayerUI:
    def __init__(self, game):
        self.communicate = Communicate()
        self.communicate.move_left.connect(self.move_left)
        self.communicate.move_right.connect(self.move_right)

    def draw(self, position):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass
