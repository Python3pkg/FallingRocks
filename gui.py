from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot, QBasicTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPalette
import subprocess
import sys
import random


class UserInterface:
    main_window = None

    def __init__(self, game):
        self.game = game

    def main_loop(self):
        app = QApplication([])
        UserInterface.main_window = MainWindow(self.game)
        # type(self).main_window = MainWindow(self.game)
        # type(self).init_main_window(self.game)
        # print(UserInterface.__dict__)
        app.exec_()

    # @classmethod
    # def init_main_window(cls, game):
    #     cls.main_window = MainWindow(game)

    # @staticmethod
    # def init_main_window(game):
    #     UserInterface.main_window = MainWindow(game)

    @staticmethod
    def get_main_window():
        return UserInterface.main_window

    # @staticmethod
    # def exit_app():
    #     # QApplication.aboutToQuit()
    #     UserInterface.app.exit()


class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.field_ui = FieldUI(self, self.game)

        self.set_background_color()

        self.set_dimensions()

        self.init_status_bar()

        self.setWindowIcon(QIcon('images/small_icon.png'))
        self.setWindowTitle('Falling Rocks')
        self.show()

    def set_background_color(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)

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
        self.height = self.game.dimensions[0]
        self.width = self.game.dimensions[1]
        self.resize(self.height, self.width)
        self.center_window()

    # @property
    # def rocks(self):
    #     return self.field_ui.rocks


class Communicate(QObject):
    def __init__(self):
        super(Communicate, self).__init__()
        # QObject.__init__(self)
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    pause = pyqtSignal()
    restart = pyqtSignal()
    message_statusbar = pyqtSignal(str)


class FieldUI(QFrame):
    def __init__(self, parent, game):
        super().__init__(parent)
    # def __init__(self, game):
    #     self.main_window = UserInterface.get_main_window()
    #     super().__init__(self.main_window)
    #     self.setParent = self.main_window
        self.main_window = parent
        self.game = game
        self.rocks = self.game.rocks
        self.width, self.height = self.game.dimensions

        self.game_timer = QBasicTimer()
        self.rock_timer = QBasicTimer()
        self.level_timer = QBasicTimer()
        self.start_timers()

        # self.player_ui = PlayerUI(self.main_window, self.game)
        self.player_ui = PlayerUI(self, self.game)
        # self.rock_ui = RockUI(parent, self.game)
        # self.powerup_ui = PowerupUI(self.game)

        self.init_signals()

        # self.communicate = Communicate()
        self.setFocusPolicy(Qt.StrongFocus)

    def start_timers(self):
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        self.level_timer.start(self.game.level_speed, self)

    def stop_timers(self):
        self.game_timer.stop()
        self.rock_timer.stop()
        self.level_timer.stop()

    def init_signals(self):
        self.com = Communicate()
        self.com.move_left.connect(self.player_ui.move_left)
        self.com.move_right.connect(self.player_ui.move_right)
        self.com.restart.connect(self.restart_game)

    def restart_game(self):
        pass
        # self.close()
        # subprocess.call("python" + " falling_rocks.py", shell=True)
        # sys.exit(UserInterface.app.exec_())
        # UserInterface.exit_app()

    def timerEvent(self, event):
        if event.timerId() == self.game_timer.timerId():
            # self.rock_ui = RockUI(self.main_window, self.game)
            self.rock_ui = RockUI(self.game)
            self.rocks.append(self.rock_ui)
            # self.drop_down_rocks()

            # self.rock_ui.drop_down()
            # self.rock_ui.set_random_position()]
        elif event.timerId() == self.rock_timer.timerId():
            self.drop_down_rocks()
        elif event.timerId() == self.level_timer.timerId():
            self.game.level_up()
            self.game_level = self.game.level
            # self.game_speed = self.game.game_speed
            self.game.set_rock_speed(self.game.rock_speed - 5)
            self.game.set_speed(self.game.game_speed - 35)
            self.main_window.communicate.message_statusbar.\
                emit("Level " + str(self.game_level))
            self.start_timers()
        else:
            super(FieldUI, self).timerEvent(event)

    def drop_down_rocks(self):
        temp_rock = None
        for rock in self.rocks:
            if(rock.y >= self.game.dimensions[1] + 5):
                print("die")
                temp_rock = rock
            else:
                rock.drop_down()
        if temp_rock is not None:
            print("now")
            self.rocks.remove(temp_rock)
            temp_rock.remove_shape()

    def keyPressEvent(self, event):
        super(FieldUI, self).keyPressEvent(event)
        # if not self.game.is_running:
        #     super(FieldUI, self).keyPressEvent(event)
        #     return

        key = event.key()
        if key == Qt.Key_P:
            # self.game.pause()
            print("p pressed")
            self.pause()
            return
        if self.game.is_paused:
            return
        elif key == Qt.Key_Left:
            self.com.move_left.emit()
        elif key == Qt.Key_Right:
            self.com.move_right.emit()
        elif key == Qt.Key_R:
            self.com.restart.emit()

    def pause(self):
        # if not self.game.isStarted:
        #     return

        # self.isPaused = not self.isPaused
        if not self.game.is_paused:
            self.game.pause()
            self.stop_timers()
            print("paused")
            # self.msg2Statusbar.emit("paused")
            self.main_window.communicate.message_statusbar.emit("Paused")

        else:
            self.game.unpause()
            print("unpaused")
            self.start_timers()
            # self.msg2Statusbar.emit(str(self.numLinesRemoved))
            self.main_window.communicate.message_statusbar.emit("Running")
        self.update()


class RockUI(QWidget):
    # def __init__(self, parent, game):
    #     super().__init__(parent)
    def __init__(self, game):
        self.main_window = UserInterface.get_main_window()
        super().__init__(self.main_window)
        self.setParent = self.main_window
        self.game = game
        self.field_width = self.game.dimensions[0]
        self.field_height = self.game.dimensions[1]

        self.set_random_shape()
        # self.pixmap = QPixmap("images/rock5.png")

        self.set_shape_size()

        # self.move(200, 2)
        # self.move(self.position[0], self.position[1])
        self.set_random_position()
        self.show()

    def set_shape_size(self):
        self.label = QLabel(self)
        self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
                                                 Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.image_size = (self.pixmap.width(), self.pixmap.height())
        # print(self.image_size)
        self.label.setFixedHeight(self.image_size[1] - 10)
        self.label.setFixedWidth(self.image_size[0])
        self.label.setScaledContents(True)

        # hbox.addWidget(lbl)

        # self.main_window = UserInterface.main_window
        # print(self.main_window)
        # self.setLayout(self.main_window)

    def set_random_shape(self):
        self.random_shape = random.randint(1, 8)
        self.pixmap = QPixmap("images/rock" + str(self.random_shape) + ".png")

    def set_random_position(self):

        self.random_coords = random.randint(1, self.field_width - 1)
        # for rock in self.game.rocks:
        #     if rock

        # to check the position  of the rocks !!!

        # print(self.random_coords)
        self.x = self.random_coords + 1
        # self.curY = self.field_height - 1 + self.image_size[1]
        self.y = 1

        self.move(self.x, self.y)
        # self.drop_down()
        self.update()

    def drop_down(self):
        self.y += 5
        self.move(self.x, self.y)

    def remove_shape(self):
        self.hide()
        self.destroy()


class PowerupUI:
    def __init__(self, game):
        pass

    def draw(self, position):
        pass

    def fall_down(self):
        pass


class PlayerUI(QWidget):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.speed = game.player_speed
        self.field_width = self.game.dimensions[0]
        self.field_height = self.game.dimensions[1]

        self.pixmap = QPixmap("images/smile3.png")
        # self.pixmap = QPixmap("smile2.jpg")

        self.set_player_shape_size()

        self.set_initial_position()
        # print("werwe")
        self.show()
        # print("fsddf")

    # def __init__(self, game):
    #     super().__init__()
    #     # self.communicate = Communicate()

    #     # Communicate.move_left.connect(self.move_left)
    #     # Communicate.move_right.connect(self.move_right)

    def set_initial_position(self):
        # self.move(200, 200)
        # self.position = [self.field_width / 2 - self.image_size[0],
        #                  self.field_height - 50]
        # self.move(self.position[0], self.position[1])
        self.x = self.field_width / 2 - self.image_size[0]
        self.y = self.field_height - 50
        self.move(self.x, self.y)

    def set_player_shape_size(self):
        self.label = QLabel(self)
        self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
                                                 Qt.KeepAspectRatio)
        self.label.setPixmap(self.myScaledPixmap)
        self.image_size = (self.pixmap.width(), self.pixmap.height())
        # print(self.image_size)
        self.label.setFixedHeight(self.image_size[1] - 48)
        self.label.setFixedWidth(self.image_size[0])
        self.label.setScaledContents(True)

        # hbox.addWidget(lbl)

        # self.main_window = UserInterface.main_window
        # print(self.main_window)
        # self.setLayout(self.main_window)
        # print(self.game.dimensions[0])

    @pyqtSlot()
    def move_left(self):
        print("left")
        if(self.x, - self.speed > 0):
            self.x -= self.speed
            self.move(self.x, self.y)

    @pyqtSlot()
    def move_right(self):
        print("right")
        if(self.x + self.speed < self.field_width -
           self.image_size[0]):
            self.x += self.speed
            self.move(self.x, self.y)
