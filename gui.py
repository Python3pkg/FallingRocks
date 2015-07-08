from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot, QBasicTimer, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from powerup import PowerupDuration, PowerupType, PowerupTimeInterval
import subprocess
import sys


class UserInterface:
    main_window = None

    def __init__(self, game):
        self.game = game

    def main_loop(self):
        UserInterface.app = QApplication([])
        UserInterface.main_window = MainWindow(self.game)
        # type(self).main_window = MainWindow(self.game)
        # type(self).init_main_window(self.game)
        # print(UserInterface.__dict__)
        UserInterface.app.exec_()

    # @classmethod
    # def init_main_window(cls, game):
    #     cls.main_window = MainWindow(game)

    # @staticmethod
    # def init_main_window(game):
    #     UserInterface.main_window = MainWindow(game)

    @staticmethod
    def get_main_window():
        return UserInterface.main_window

    @staticmethod
    def get_app():
        return UserInterface.app

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

    def restart_game(self):
        # self.close()
        # sys.exit(UserInterface.app.exec_())

        # UserInterface.app.exec_()
        self.exit_game()
        subprocess.call("python" + " falling_rocks.py", shell=True)

    def exit_game(self):
        UserInterface.app.exit()


class Communicate(QObject):
    def __init__(self):
        super(Communicate, self).__init__()
        # QObject.__init__(self)
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    pause = pyqtSignal()
    restart = pyqtSignal()
    exit = pyqtSignal()
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
        self.powerups = self.game.powerups
        self.width, self.height = self.game.dimensions

        self.init_timers()

        self.start_timers()

        # self.player_ui = PlayerUI(self.main_window, self.game)
        self.player_ui = PlayerUI(self, self.game)
        # self.rock_ui = RockUI(parent, self.game)
        # self.powerup_ui = PowerupUI(self, self.game, 1)

        self.init_signals()

        # self.communicate = Communicate()
        self.setFocusPolicy(Qt.StrongFocus)

    def init_timers(self):
        self.game_timer = QBasicTimer()
        self.rock_timer = QBasicTimer()
        self.level_timer = QBasicTimer()
        self.powerup_timer = QBasicTimer()
        self.ticker_timer = QBasicTimer()

        self.player_invincibility_timer = QBasicTimer()
        self.big_bomb_timer = QBasicTimer()
        self.slow_down_rocks_timer = QBasicTimer()
        self.shoot_rocks_timer = QBasicTimer()
        self.powerup_duration_timer = QTimer()

    def start_timers(self):
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        self.level_timer.start(self.game.level_speed, self)
        # print(type(PowerupTimeInterval.medium))
        self.powerup_timer.start(self.game.rock_speed, self)
        self.player_invincibility_timer.start(int(PowerupTimeInterval.medium),
                                              self)
        self.big_bomb_timer.start(int(PowerupTimeInterval.big), self)
        self.slow_down_rocks_timer.start(int(PowerupTimeInterval.
                                         very_big), self)
        self.shoot_rocks_timer.start(int(PowerupTimeInterval.
                                     huge), self)

    def stop_timers(self):
        self.game_timer.stop()
        self.rock_timer.stop()
        self.level_timer.stop()
        self.powerup_timer.stop()

        self.player_invincibility_timer.stop()
        self.big_bomb_timer.stop()
        self.slow_down_rocks_timer.stop()
        self.shoot_rocks_timer.stop()

    def init_signals(self):
        self.com = Communicate()
        self.com.move_left.connect(self.player_ui.move_left)
        self.com.move_right.connect(self.player_ui.move_right)
        self.com.restart.connect(self.main_window.restart_game)
        self.com.exit.connect(self.main_window.exit_game)

    # def restart_game(self):
    #     pass
    #     # self.close()
    #     # sys.exit(UserInterface.app.exec_())
    #     # UserInterface.app.exec_()
    #     subprocess.call("python" + " falling_rocks.py", shell=True)

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
        elif event.timerId() == self.powerup_timer.timerId():
            self.drop_down_powerups()
        elif event.timerId() == self.level_timer.timerId():
            self.game.level_up()
            self.game_level = self.game.level
            # self.game_speed = self.game.game_speed
            self.game.set_rock_speed(self.game.rock_speed - 5)
            self.game.set_speed(self.game.game_speed - 35)
            self.main_window.communicate.message_statusbar.\
                emit("Level " + str(self.game_level))
            # self.start_timers()
            self.game_timer.start(self.game.game_speed, self)
            self.rock_timer.start(self.game.rock_speed, self)
        elif event.timerId() == self.player_invincibility_timer.timerId():
            # self.powerup_duration_timer.start(int(PowerupDuration.medium))
            # self.powerup_duration_timer.timeout.connect(self.
            #                                             stop_powerup_timer)
            # self.powerup_duration_timer.setSingleShot(True)
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self.game, PowerupType.
                                        player_invinciblility)

            self.powerups.append(self.powerup_ui)
            # print("powerup")
        elif event.timerId() == self.big_bomb_timer.timerId():
            # self.remove_all_rocks()
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self.game, PowerupType.big_bomb)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.slow_down_rocks_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self.game, PowerupType.slow_down_rocks)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.shoot_rocks_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self.game, PowerupType.shoot_rocks)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.ticker_timer.timerId():
            self.ticker["value"] -= 1
            print("ticker ", self.ticker)
            if self.ticker["type"] == "player_invincibility":
                self.show_player_invincibility_info(self.ticker["value"])
            if self.ticker["type"] == "slow_down_rocks":
                self.show_slow_down_rocks_info(self.ticker["value"])
            # self.show_slow_down_rocks_info(self.ticker)

        else:
            super(FieldUI, self).timerEvent(event)

    def drop_down_powerups(self):
        temp_powerup = None
        for powerup in self.powerups:
            if(powerup.y >= self.game.dimensions[1] - powerup.height):
                # print("die")
                temp_powerup = powerup
            else:
                powerup.drop_down()
            if(self.game.collision_detected(self.player_ui, powerup)):
                print("powerup_collision_detected")
                # self.stop_timers(
                print(powerup.type)
                if powerup.type == PowerupType.player_invinciblility:
                    print(self.player_ui.is_player_invincible)
                    self.init_player_invincibility()
                elif powerup.type == PowerupType.big_bomb:
                    self.init_big_bomb()
                elif powerup.type == PowerupType.slow_down_rocks:
                    self.init_slow_down_rocks()
                elif powerup.type == PowerupType.shoot_rocks:
                    self.init_shoot_rocks()
        if temp_powerup is not None:
            self.remove_powerup_from_field(temp_powerup)

    def init_slow_down_rocks(self):
        self.game.set_rock_speed(self.game.rock_speed + 3)
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)

        # self.main_window.communicate.message_statusbar.\
        #     emit("The rock are slowed down for " +
        #          str(int(PowerupDuration.medium) // 1000) +
        #          " seconds")
        self.ticker = {"type": "slow_down_rocks",
                       "value": int(PowerupDuration.medium) // 1000}
        self.show_slow_down_rocks_info(self.ticker["value"])
        self.ticker_timer.start(1000, self)

        # self.powerup_duration_timer.start(int(PowerupDuration.
        #                                   medium))
        # self.powerup_duration_timer.timeout.\
        #     connect(self.stop_slow_down_rocks)
        self.powerup_duration_timer.setSingleShot(True)
        self.powerup_duration_timer.singleShot(
            int(PowerupDuration.medium), self.stop_slow_down_rocks)

    def show_slow_down_rocks_info(self, value):
        # value = value // 1000
        self.main_window.communicate.message_statusbar.\
            emit("The rock are slowed down for " + str(value) + " seconds")

    def stop_slow_down_rocks(self):
        self.powerup_duration_timer.stop()
        self.game.set_rock_speed(self.game.rock_speed - 3)
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        print("again")
        # print(self.player_ui.is_player_invincible)
        self.main_window.communicate.message_statusbar.\
            emit("The rock are no longer slowed down. Be careful!")

    def init_shoot_rocks(self):
        pass

    def init_big_bomb(self):
        # del self.rocks[:]
        temp_rocks = self.rocks[:]
        for temp_rock in temp_rocks:
            self.remove_rock_from_field(temp_rock)

    def init_player_invincibility(self):
        if not self.player_ui.is_player_invincible:
            self.player_ui.set_player_invinciblity()
            print("init player", self.player_ui.is_player_invincible)
            # self.main_window.communicate.message_statusbar.\
            #     emit("The player is invincible for " +
            #          str(int(PowerupDuration.small) // 1000) +
            #          " seconds")
            self.ticker = {"type": "slow_down_rocks",
                           "value": int(PowerupDuration.small) // 1000}
            self.show_slow_down_rocks_info(self.ticker["value"])
            self.ticker_timer.start(1000, self)
            # self.powerup_duration_timer.start(int(PowerupDuration.
            #                                   small))
            # self.powerup_duration_timer.timeout.\
            #     connect(self.stop_player_invincibility_timer)
            self.powerup_duration_timer.setSingleShot(True)
            self.powerup_duration_timer.singleShot(
                int(PowerupDuration.small), self.stop_player_invincibility)

    def stop_player_invincibility(self):
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        self.player_ui.set_player_invinciblity()
        print("again")
        print(self.player_ui.is_player_invincible)
        self.main_window.communicate.message_statusbar.\
            emit("The player's invinciblility is off. You are mortal again!")

    def show_player_invincibility_info(self, value):
        # value = value // 1000
        self.main_window.communicate.message_statusbar.\
            emit("The player is invincible for " + str(value) + " seconds")

    def remove_powerup_from_field(self, powerup):
        print("powerup died")
        self.powerups.remove(powerup)
        powerup.remove_shape()
        if(self.powerups.count == 0):
            self.powerup_timer.stop()

    def drop_down_rocks(self):
        temp_rock = None
        for rock in self.rocks:
            if(rock.y >= self.game.dimensions[1] - rock.height):
                # print("die")
                temp_rock = rock
            else:
                rock.drop_down()
            if(not self.player_ui.is_player_invincible and
               self.game.collision_detected(self.player_ui, rock)):
                print("rock_collision_detected",
                      self.player_ui.is_player_invincible)
                self.stop_timers()
                self.main_window.communicate.message_statusbar.\
                    emit("Game Over")
        if temp_rock is not None:
            self.remove_rock_from_field(temp_rock)
            # print("now")
            # self.rocks.remove(temp_rock)
            # temp_rock.remove_shape()

    def remove_rock_from_field(self, rock):
        self.rocks.remove(rock)
        rock.remove_shape()

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
        elif key == Qt.Key_Escape:
            self.com.exit.emit()

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
        self.rock_shape_number = 8
        self.game = game
        self.rock = self.game.rock
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
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        # print(self.width, self.height, type(self.width))
        # print(self.image_size)
        self.label.setFixedHeight(self.image_size[1] - 10)
        self.label.setFixedWidth(self.image_size[0])
        self.label.setScaledContents(True)

        # hbox.addWidget(lbl)

        # self.main_window = UserInterface.main_window
        # print(self.main_window)
        # self.setLayout(self.main_window)

    def set_random_shape(self):
        # self.random_shape = random.randint(1, self.rock_shape_number)
        self.random_shape = self.rock.\
            set_random_shape(self.rock_shape_number)
        self.pixmap = QPixmap("images/rock" + str(self.random_shape) + ".png")

    def set_random_position(self):
        # self.random_coords = random.randint(1, self.field_width - 1)
        self.random_coords = self.rock.\
            set_random_position(self.field_width - 5)
        # for rock in self.game.rocks:
        #     if rock

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


class PowerupUI(QWidget):
    def __init__(self, game, type):
        self.main_window = UserInterface.get_main_window()
        super().__init__(self.main_window)
        self.setParent = self.main_window
        self.game = game
        self.type = type
        print(self.type)
        self.field_width = self.game.dimensions[0]
        self.field_height = self.game.dimensions[1]
        self.powerup = self.game.powerup

        # self.pixmap = QPixmap("images/smile3.png")
        self.set_shape(self.type)

        # print(self.width, self.height, type(self.width))

        self.set_shape_size()

        # self.set_initial_position()

        self.set_random_position()
        # print("powerup ui")
        self.show()

    def set_shape(self, type):
        if type == PowerupType.player_invinciblility:
            self.pixmap = QPixmap("images/invinciblility.png")
        elif type == PowerupType.big_bomb:
            self.pixmap = QPixmap("images/big_bomb.png")
        elif type == PowerupType.slow_down_rocks:
            self.pixmap = QPixmap("images/slow_down_rocks.png")
        elif type == PowerupType.shoot_rocks:
            self.pixmap = QPixmap("images/shoot_rocks.png")
            # print("powerup shape set")

    def set_random_position(self):
        # self.random_coords = random.randint(1, self.field_width - 1)
        self.random_coords = self.powerup.\
            set_random_position(self.field_width - 1)
        # for rock in self.game.rocks:
        #     if rock

        # print(self.random_coords)
        self.x = self.random_coords + 1
        # self.curY = self.field_height - 1 + self.image_size[1]
        self.y = 1

        self.move(self.x, self.y)
        # self.drop_down()
        self.update()
        # print("powerup position set", self.x, self.y)

    def drop_down(self):
        self.y += 5
        self.move(self.x, self.y)
        # print("powerup moved")

    def remove_shape(self):
        self.hide()
        self.destroy()

    # def set_initial_position(self):
    #     self.x = self.field_width / 2 - self.image_size[0]
    #     self.y = self.field_height - 50
    #     self.move(self.x, self.y)

    def set_shape_size(self):
        self.label = QLabel(self)
        # self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
        #                                          Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.image_size = (self.pixmap.width(), self.pixmap.height())
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        # print(self.width, self.height, type(self.width))
        # print(self.image_size)
        self.label.setFixedHeight(self.image_size[1] - 5)
        self.label.setFixedWidth(self.image_size[0])
        # self.label.setScaledContents(True)


class PlayerUI(QWidget):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.player = game.player
        self.speed = game.player_speed
        self.field_width = self.game.dimensions[0]
        self.field_height = self.game.dimensions[1]

        self.pixmap = QPixmap("images/smile3.png")
        # self.pixmap = QPixmap("smile2.jpg")

        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        # print(self.width, self.height, type(self.width))

        self.set_shape_size()

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

    def set_shape_size(self):
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

    @property
    def is_player_invincible(self):
        return self.player.is_invincible

    def set_player_invinciblity(self):
        self.player.is_invincible = not self.player.is_invincible

    @pyqtSlot()
    def move_left(self):
        print("left")
        if(self.x - self.speed > 0):
            self.x -= self.speed
            self.move(self.x, self.y)

    @pyqtSlot()
    def move_right(self):
        print("right")
        if(self.x + self.speed < self.field_width -
           self.image_size[0]):
            self.x += self.speed
            self.move(self.x, self.y)
