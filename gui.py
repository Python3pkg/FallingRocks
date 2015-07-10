import subprocess
from PyQt5.QtCore import QObject, Qt, pyqtSignal, pyqtSlot, QBasicTimer, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPalette
from powerup import PowerupType, PowerupTimeInterval
# import sys


class UserInterface:
    main_window = None

    def __init__(self, game):
        self.game = game

    def main_loop(self):
        """Initializes the app and the main window of the game and starts the
        main loop of the game.
        """
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
        """Gets the main windows object of the game."""
        return UserInterface.main_window

    @staticmethod
    def get_app():
        """Gets the game application object."""
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

        self.center_window()

        self.init_status_bar()

        self.setWindowIcon(QIcon('images/small_icon.png'))
        self.setWindowTitle('Falling Rocks')
        self.show()

    def set_background_color(self):
        """Sets the background color of the main window."""
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)

    def center_window(self):
        """Puts the field widget in the center of the main window."""
        self.setCentralWidget(self.field_ui)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def init_status_bar(self):
        """Initializes the status bar of the game and shows a New game message
        to the user.
        """
        self.communicate = Communicate()
        self.statusbar = self.statusBar()
        self.communicate.message_statusbar[str].\
            connect(self.statusbar.showMessage)
        self.communicate.message_statusbar.emit("New game")

    def set_dimensions(self):
        """Sets the dimensions of the main window."""
        self.height = self.game.dimensions[0]
        self.width = self.game.dimensions[1]
        self.resize(self.height, self.width)

    def restart_game(self):
        """Restarts the game and opens a new game application."""
        # self.close()
        # sys.exit(UserInterface.app.exec_())

        # UserInterface.app.exec_()
        self.game.reset_game_values()
        self.exit_game()
        subprocess.call("python" + " falling_rocks.py", shell=True)

    def exit_game(self):
        """Exits the game and closes the game application."""
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
        self.bullets = self.game.bullets
        self.width, self.height = self.game.dimensions

        self.init_timers()

        self.start_timers()

        # self.player_ui = PlayerUI(self.main_window, self.game)
        self.player_ui = PlayerUI(self, self.game)
        # self.bullet_ui = BulletUI(self, self.game, self.player_ui)
        # self.rock_ui = RockUI(parent, self.game)
        # self.powerup_ui = PowerupUI(self, self.game, 1)

        self.init_signals()

        # self.communicate = Communicate()
        self.setFocusPolicy(Qt.StrongFocus)

    def init_timers(self):
        """Initializes the timers in the game."""
        self.game_timer = QBasicTimer()
        self.rock_timer = QBasicTimer()
        self.level_timer = QBasicTimer()
        self.powerup_timer = QBasicTimer()
        self.ticker_timer = QBasicTimer()
        self.bullet_timer = QBasicTimer()

        self.player_invincibility_timer = QBasicTimer()
        self.big_bomb_timer = QBasicTimer()
        self.slow_down_rocks_timer = QBasicTimer()
        self.shoot_rocks_timer = QBasicTimer()

        self.powerup_duration_timer = QTimer()

    def start_timers(self):
        """Starts the timers in the game."""
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        self.level_timer.start(self.game.level_speed, self)
        # print(type(PowerupTimeInterval.medium))
        self.powerup_timer.start(self.game.rock_speed, self)
        self.player_invincibility_timer.start(int(PowerupTimeInterval.medium),
                                              self)
        self.big_bomb_timer.start(int(PowerupTimeInterval.big), self)
        self.slow_down_rocks_timer.start(int(PowerupTimeInterval.
                                         medium), self)
        self.shoot_rocks_timer.start(int(PowerupTimeInterval.
                                     medium), self)
        self.bullet_timer.start(self.game.bullet_speed, self)
        # if self.game.is_paused:
        #     pass
        # self.powerup_duration_timer.stop()

    def stop_timers(self):
        """Stops the timers in the game."""
        self.game_timer.stop()
        self.rock_timer.stop()
        self.level_timer.stop()
        self.powerup_timer.stop()
        self.ticker_timer.stop()
        self.bullet_timer.stop()

        self.player_invincibility_timer.stop()
        self.big_bomb_timer.stop()
        self.slow_down_rocks_timer.stop()
        self.shoot_rocks_timer.stop()

        self.powerup_duration_timer.stop()

    def init_signals(self):
        """Initializes the signals in the game that connect to a method and
        calls it after the singnals are emitted.
        """
        self.com = Communicate()
        self.com.move_left.connect(self.player_ui.move_left)
        self.com.move_right.connect(self.player_ui.move_right)
        self.com.restart.connect(self.main_window.restart_game)
        self.com.exit.connect(self.main_window.exit_game)

    # def restart_game(self):
    #     self.game.reset_game_values()
    #     # self.close()
    #     # sys.exit(UserInterface.app.exec_())
    #     # UserInterface.app.exec_()
    #     subprocess.call("python" + " falling_rocks.py", shell=True)

    def timerEvent(self, event):
        """Gets the emitted events from the timers and calls the appropriate
        methods for each of them.
        """
        self.powerups_timer_events(event)
        self.gameplay_timer_events(event)
        if event.timerId() == self.ticker_timer.timerId():
            self.ticker["value"] -= 1
            print("ticker ", self.ticker)
            if self.ticker["type"] == "player_invincibility":
                self.show_player_invincibility_info(self.ticker["value"])
            if self.ticker["type"] == "slow_down_rocks":
                self.show_slow_down_rocks_info(self.ticker["value"])
            if self.ticker["type"] == "shoot_rocks":
                self.show_shoot_rocks_info(self.ticker["value"])
                self.bullet_ui = BulletUI(self, self.game, self.player_ui)
                self.bullets.append(self.bullet_ui)
            # self.show_slow_down_rocks_info(self.ticker)
        else:
            super(FieldUI, self).timerEvent(event)

    def gameplay_timer_events(self, event):
        """Gets the emitted events from the timers related to the gameplay and
        calls the appropriate methods and initializes the appropriate objects
        for each of them.
        """
        if event.timerId() == self.game_timer.timerId():
            # self.rock_ui = RockUI(self.main_window, self.game)
            self.rock_ui = RockUI(self, self.game)
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
            self.game.set_speed(self.game.game_speed - 40)
            self.main_window.communicate.message_statusbar.\
                emit("Level " + str(self.game_level))
            # self.start_timers()
            self.game_timer.start(self.game.game_speed, self)
            self.rock_timer.start(self.game.rock_speed, self)
        elif event.timerId() == self.bullet_timer.timerId():
            if self.bullets.count != 0:
                self.shoot_bullets()

    def powerups_timer_events(self, event):
        """Gets the emitted events from the timers related to the powerups and
        calls the appropriate methods and initializes the appropriate objects
        for each of them.
        """
        if event.timerId() == self.player_invincibility_timer.timerId():
            # self.powerup_duration_timer.start(int(PowerupDuration.medium))
            # self.powerup_duration_timer.timeout.connect(self.
            #                                             stop_powerup_timer)
            # self.powerup_duration_timer.setSingleShot(True)
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game, PowerupType.
                                        player_invinciblility)

            self.powerups.append(self.powerup_ui)
            # print("powerup")
        elif event.timerId() == self.big_bomb_timer.timerId():
            # self.remove_all_rocks()
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game, PowerupType.big_bomb)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.slow_down_rocks_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game,
                                        PowerupType.slow_down_rocks)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.shoot_rocks_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game,
                                        PowerupType.shoot_rocks)
            self.powerups.append(self.powerup_ui)

    def drop_down_powerups(self):
        """Moves the powerups down and check if the move is out of the game
        field. If that is true the powerups are removed from the field.
        """
        temp_powerup = None
        for powerup in self.powerups:
            if(powerup.y >= self.game.dimensions[1] - powerup.height):
                # print("die")
                temp_powerup = powerup
            else:
                powerup.drop_down()
            self.check_collision_between_player_and_powerup(powerup)
        if temp_powerup is not None:
            self.remove_powerup_from_field(temp_powerup)

    def check_collision_between_player_and_powerup(self, powerup):
        """Checks for a collision between the player and the powerups. If that
        is true initializes the powerups' effect according to their type.
        """
        if(self.game.collision_detected(self.player_ui, powerup)):
            print("powerup_collision_detected")
            # self.stop_timers(
            print(powerup.type)
            if powerup.type == PowerupType.player_invinciblility:
                print(self.player_ui.is_player_invincible)
                self.init_player_invincibility(powerup)
            elif powerup.type == PowerupType.big_bomb:
                self.init_big_bomb()
            elif powerup.type == PowerupType.slow_down_rocks:
                self.init_slow_down_rocks(powerup)
            elif powerup.type == PowerupType.shoot_rocks:
                self.init_shoot_rocks(powerup)

    def init_slow_down_rocks(self, powerup):
        """Initializes the powerup slow_down_rocks and it's effect of the
        game."""
        self.game.set_rock_speed(self.game.rock_speed + 3)
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)

        # self.main_window.communicate.message_statusbar.\
        #     emit("The rock are slowed down for " +
        #          str(int(PowerupDuration.medium) // 1000) +
        #          " seconds")

        # self.ticker = {"type": "slow_down_rocks",
        #                "value": int(PowerupDuration.small) // 1000}
        self.ticker = {"type": "slow_down_rocks",
                       "value": powerup.duration // 1000}

        self.show_slow_down_rocks_info(self.ticker["value"])
        self.ticker_timer.start(PowerupTimeInterval.second, self)

        # self.powerup_duration_timer.start(int(PowerupDuration.
        #                                   medium))
        # self.powerup_duration_timer.timeout.\
        #     connect(self.stop_slow_down_rocks)
        self.powerup_duration_timer.setSingleShot(True)
        self.powerup_duration_timer.singleShot(powerup.duration,
                                               self.stop_slow_down_rocks)

    def show_slow_down_rocks_info(self, value):
        """Shows information about the powerup slow_down_rocks to the
        player.
        """
        # value = value // 1000
        self.main_window.communicate.message_statusbar.\
            emit("The rock are slowed down for " + str(value) + " seconds")

    def stop_slow_down_rocks(self):
        """Stops the effect of the powerup slow_down_rocks and shows a message
        to the player.
        """
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        self.game.set_rock_speed(self.game.rock_speed - 3)
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        print("again")
        # print(self.player_ui.is_player_invincible)
        self.main_window.communicate.message_statusbar.\
            emit("The rock are no longer slowed down. Be careful!")

    def shoot_bullets(self):
        """Moves the bullets up (to the target) and check if the move is out of
        the game field. If that is true the bullets are removed from the field.
        """
        temp_bullet = None
        for bullet in self.bullets:
            if(bullet.y <= 1):
                # print("die")
                temp_bullet = bullet
            else:
                bullet.move_to_target()
                self.check_collision_between_bullet_and_rock(bullet)
        if temp_bullet is not None:
            self.remove_bullet_from_field(temp_bullet)
            # self.remove_rock_from_field(temp_rock)

    def check_collision_between_bullet_and_rock(self, bullet):
        """Checks for a collision between the bullets and the rocks. If that
        is true removes the rocks from the game field.
        """
        for rock in self.rocks:
            if self.game.collision_detected(bullet, rock):
                self.remove_rock_from_field(rock)
                print("bullet_collision_detected")

    def init_shoot_rocks(self, powerup):
        """Initializes the powerup shoot_rocks and it's effect of the game."""
        # some method
        # self.bullet_timer.start(self.game.bullet_speed, self)

        self.ticker = {"type": "shoot_rocks",
                       "value": powerup.duration // 1000}
        self.show_slow_down_rocks_info(self.ticker["value"])
        self.ticker_timer.start(PowerupTimeInterval.second, self)

        self.powerup_duration_timer.setSingleShot(True)
        self.powerup_duration_timer.singleShot(powerup.duration,
                                               self.stop_shoot_rocks)

    def show_shoot_rocks_info(self, value):
        """Shows information about the powerup shoot_rocks to the player."""
        # value = value // 1000
        self.main_window.communicate.message_statusbar.\
            emit("You have bullets for " + str(value) + " seconds")

    def stop_shoot_rocks(self):
        """Stops the effect of the powerup shoot_rocks and shows a message
        to the player.
        """
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        # self.bullet_timer.stop()
        self.main_window.communicate.message_statusbar.\
            emit("No more bullets!")

    def init_big_bomb(self):
        """Initializes the powerup big_bomb and it's effect of the game."""
        # del self.rocks[:]
        temp_rocks = self.rocks[:]
        for temp_rock in temp_rocks:
            self.remove_rock_from_field(temp_rock)
        self.main_window.communicate.message_statusbar.\
            emit("BOOM! The blast totally destroyed everything on the field!")

    def init_player_invincibility(self, powerup):
        """Initializes the powerup player_invincibility and it's effect
        of the game.
        """
        if not self.player_ui.is_player_invincible:
            self.player_ui.set_player_invinciblity()
            print("init player", self.player_ui.is_player_invincible)
            # self.main_window.communicate.message_statusbar.\
            #     emit("The player is invincible for " +
            #          str(int(PowerupDuration.small) // 1000) +
            #          " seconds")
            self.ticker = {"type": "slow_down_rocks",
                           "value": powerup.duration // 1000}
            self.show_slow_down_rocks_info(self.ticker["value"])
            self.ticker_timer.start(PowerupTimeInterval.second, self)
            # self.powerup_duration_timer.start(int(PowerupDuration.
            #                                   small))
            # self.powerup_duration_timer.timeout.\
            #     connect(self.stop_player_invincibility_timer)
            self.powerup_duration_timer.setSingleShot(True)
            self.powerup_duration_timer.singleShot(
                powerup.duration, self.stop_player_invincibility
            )

    def stop_player_invincibility(self):
        """Stops the effect of the powerup player_invincibility and shows a
        message to the player.
        """
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        self.player_ui.set_player_invinciblity()
        print("again")
        print(self.player_ui.is_player_invincible)
        self.main_window.communicate.message_statusbar.\
            emit("The player's invinciblility is off. You are mortal again!")

    def show_player_invincibility_info(self, value):
        """Shows information about the powerup player_invincibility_info to the
        player.
        """
        # value = value // 1000
        self.main_window.communicate.message_statusbar.\
            emit("The player is invincible for " + str(value) + " seconds")

    def remove_powerup_from_field(self, powerup):
        """Removes a powerup from the game field."""
        print("powerup died")
        self.powerups.remove(powerup)
        powerup.remove_shape()
        if(self.powerups.count == 0):
            self.powerup_timer.stop()

    def remove_bullet_from_field(self, bullet):
        """Removes a bullet from the game field."""
        print("bullet died")
        self.bullets.remove(bullet)
        bullet.remove_shape()
        if(self.bullets.count == 0):
            self.bullet_timer.stop()

    def remove_rock_from_field(self, rock):
        """Removes a rock from the game field."""
        self.rocks.remove(rock)
        rock.remove_shape()

    def drop_down_rocks(self):
        """Moves the rocks down and check if the move is out of the game
        field. If that is true the rocks are removed from the field.
        """
        temp_rock = None
        for rock in self.rocks:
            if(rock.y >= self.game.dimensions[1] - rock.height - 15):
                # print("die")
                temp_rock = rock
            else:
                rock.drop_down()
            self.check_collision_between_rock_and_player(rock)
        if temp_rock is not None:
            self.remove_rock_from_field(temp_rock)
            # print("now")
            # self.rocks.remove(temp_rock)
            # temp_rock.remove_shape()

    def check_collision_between_rock_and_player(self, rock):
        """Checks for a collision between the rock and the player. If that is
        true the game is over.
        """
        if(not self.player_ui.is_player_invincible and
           self.game.collision_detected(self.player_ui, rock)):
            print("rock_collision_detected",
                  self.player_ui.is_player_invincible)
            self.stop_timers()
            self.game.lose()
            self.main_window.communicate.message_statusbar.\
                emit("Game Over")

    def keyPressEvent(self, event):
        """Gets the events emitted when the player presses a key on the
        keyboard and calls the appropriate method.
        """
        super(FieldUI, self).keyPressEvent(event)
        # if not self.game.is_running:
        #     super(FieldUI, self).keyPressEvent(event)
        #     return

        key = event.key()
        if key == Qt.Key_Escape:
            self.com.exit.emit()
        elif key == Qt.Key_R:
            self.com.restart.emit()
        elif self.game.is_lost:
            return
        elif key == Qt.Key_P:
            # self.game.pause()
            print("p pressed")
            if self.game.is_running:
                self.pause_game()
            else:
                self.resume_game()
            return
        if self.game.is_paused:
            return
        elif key == Qt.Key_Left:
            self.com.move_left.emit()
        elif key == Qt.Key_Right:
            self.com.move_right.emit()

    def pause_game(self):
        """Pauses the game and shows a message to the player."""
        if self.game.is_running:
            self.game.pause()
            self.stop_timers()
            print("paused")
            # self.msg2Statusbar.emit("paused")
            self.main_window.communicate.message_statusbar.emit("Paused")

    def resume_game(self):
        """Resumes the game and shows a message to the player."""
        if self.game.is_paused:
            self.game.resume()
            print("unpaused")
            self.start_timers()
            # self.msg2Statusbar.emit(str(self.numLinesRemoved))
            self.main_window.communicate.message_statusbar.emit("Running")
        self.update()


class ShapeUI(QWidget):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.main_window = parent
        self.image_height_fix = 0
        self.shape = None

        self.field_width = self.game.dimensions[0]
        self.field_height = self.game.dimensions[1]

    def set_shape_size(self):
        """Set the size of the shape to be the same size as the it's image."""
        self.label = QLabel(self)
        self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
                                                 Qt.KeepAspectRatio)
        self.label.setPixmap(self.myScaledPixmap)
        self.image_size = (self.pixmap.width(), self.pixmap.height())
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()
        # print(self.width, self.height, type(self.width))
        # print(self.image_size)
        self.label.setFixedHeight(self.image_size[1] - self.image_height_fix)
        self.label.setFixedWidth(self.image_size[0])
        self.label.setScaledContents(True)

    # def set_shape_size(self):
    #     self.label = QLabel(self)
    #     self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
    #                                              Qt.KeepAspectRatio)
    #     self.label.setPixmap(self.pixmap)
    #     self.image_size = (self.pixmap.width(), self.pixmap.height())
    #     self.width = self.pixmap.width()
    #     self.height = self.pixmap.height()
    #     # print(self.width, self.height, type(self.width))
    #     # print(self.image_size)
    #     self.label.setFixedHeight(self.image_size[1] - 10)
    #     self.label.setFixedWidth(self.image_size[0])
    #     self.label.setScaledContents(True)

    def set_random_position(self):
        """Sets a random position of the shape and moves the shape there."""
        # self.random_coords = random.randint(1, self.field_width - 1)
        self.random_coords = self.shape.\
            set_random_position(self.field_width - 15)
        # for rock in self.game.rocks:
        #     if rock

        # print(self.random_coords)
        self.x = self.random_coords + 1
        # self.curY = self.field_height - 1 + self.image_size[1]
        self.y = 1

        self.move(self.x, self.y)
        # self.drop_down()
        self.update()

    def remove_shape(self):
        """Removes the shape from the field and destroys the shape object."""
        self.hide()
        self.destroy()


class BulletUI(ShapeUI):
    # def __init__(self, game, player_ui):
    #     self.main_window = UserInterface.get_main_window()
    #     super().__init__(self.main_window)
    #     self.setParent = self.main_window
    def __init__(self, parent, game, player_ui):
        super().__init__(parent, game)
        self.game = game
        # self.main_window = parent
        # self.bullet = self.game.bullet
        self.player_ui = player_ui
        # self.field_width = self.game.dimensions[0]
        # self.field_height = self.game.dimensions[1]
        self.image_height_fix = 5

        self.pixmap = QPixmap("images/bullet.png")

        self.set_shape_size()

        # self.move(200, 2)
        # self.move(self.position[0], self.position[1])
        self.set_initial_position()
        self.show()

    # def set_shape_size(self):
    #     self.label = QLabel(self)
    #     self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
    #                                              Qt.KeepAspectRatio)
    #     self.label.setPixmap(self.pixmap)
    #     self.image_size = (self.pixmap.width(), self.pixmap.height())
    #     self.width = self.pixmap.width()
    #     self.height = self.pixmap.height()
    #     # print(self.width, self.height, type(self.width))
    #     # print(self.image_size)
    #     self.label.setFixedHeight(self.image_size[1] - 5)
    #     self.label.setFixedWidth(self.image_size[0])
    #     self.label.setScaledContents(True)

    def set_initial_position(self):
        """Set the initial position of the bullet and moves the bullet
        there.
        """
        # self.x = self.random_coords + 1
        # self.y = 1

        self.x = self.player_ui.x + self.player_ui.width / 2 - 15
        self.y = self.player_ui.y - self.player_ui.height / 2 + 15

        self.move(self.x, self.y)

        self.update()

    def move_to_target(self):
        """Moves the bullet up (to the tagrget)."""
        self.y -= 5
        self.move(self.x, self.y)

    # def remove_shape(self):
    #     self.hide()
    #     self.destroy()


class RockUI(ShapeUI):
    def __init__(self, parent, game):
        super().__init__(parent, game)

    # def __init__(self, game):
    #     self.main_window = UserInterface.get_main_window()
    #     super().__init__(self.main_window)
    #     self.setParent = self.main_window
        self.rock_shape_number = 8
        self.image_height_fix = 10
        # self.game = game
        # self.main_window = parent
        self.rock = self.game.rock
        self.shape = self.rock
        # self.field_width = self.game.dimensions[0]
        # self.field_height = self.game.dimensions[1]

        self.set_random_shape()
        # self.pixmap = QPixmap("images/rock5.png")

        self.set_shape_size()

        # self.move(200, 2)
        # self.move(self.position[0], self.position[1])
        self.set_random_position()
        self.show()

    # def set_shape_size(self):
    #     self.label = QLabel(self)
    #     self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
    #                                              Qt.KeepAspectRatio)
    #     self.label.setPixmap(self.pixmap)
    #     self.image_size = (self.pixmap.width(), self.pixmap.height())
    #     self.width = self.pixmap.width()
    #     self.height = self.pixmap.height()
    #     # print(self.width, self.height, type(self.width))
    #     # print(self.image_size)
    #     self.label.setFixedHeight(self.image_size[1] - 10)
    #     self.label.setFixedWidth(self.image_size[0])
    #     self.label.setScaledContents(True)

        # hbox.addWidget(lbl)

        # self.main_window = UserInterface.main_window
        # print(self.main_window)
        # self.setLayout(self.main_window)

    def set_random_shape(self):
        """Sets a random shape of the rock."""
        # self.random_shape = random.randint(1, self.rock_shape_number)
        self.random_shape = self.rock.\
            set_random_shape(self.rock_shape_number)
        self.pixmap = QPixmap("images/rock" + str(self.random_shape) + ".png")

    # def set_random_position(self):
    #     # self.random_coords = random.randint(1, self.field_width - 1)
    #     self.random_coords = self.rock.\
    #         set_random_position(self.field_width - 5)
    #     # for rock in self.game.rocks:
    #     #     if rock

    #     # print(self.random_coords)
    #     self.x = self.random_coords + 1
    #     # self.curY = self.field_height - 1 + self.image_size[1]
    #     self.y = 1

    #     self.move(self.x, self.y)
    #     # self.drop_down()
    #     self.update()

    def drop_down(self):
        """Moves the rock down."""
        self.y += 5
        self.move(self.x, self.y)

    # def remove_shape(self):
    #     self.hide()
    #     self.destroy()


class PowerupUI(ShapeUI):
    # def __init__(self, game, type):
    #     self.main_window = UserInterface.get_main_window()
    #     super().__init__(self.main_window)
    #     self.setParent = self.main_window
    def __init__(self, parent, game, type):
        # super().__init__(parent)
        super().__init__(parent, game)
        # self.main_window = parent
        # self.game = game
        self.type = type
        self.image_height_fix = 5
        print(self.type)
        # self.field_width = self.game.dimensions[0]
        # self.field_height = self.game.dimensions[1]
        self.powerup = self.game.powerup
        self.shape = self.powerup

        self.set_duration()

        # self.pixmap = QPixmap("images/smile3.png")
        self.set_shape(self.type)

        # print(self.width, self.height, type(self.width))

        self.set_shape_size()

        # self.set_initial_position()

        self.set_random_position()
        # print("powerup ui")
        self.show()

    def set_shape(self, type):
        """Sets the shape of the powerup according to it's type."""
        if type == PowerupType.player_invinciblility:
            self.pixmap = QPixmap("images/invinciblility.png")
        elif type == PowerupType.big_bomb:
            self.pixmap = QPixmap("images/big_bomb.png")
        elif type == PowerupType.slow_down_rocks:
            self.pixmap = QPixmap("images/slow_down_rocks.png")
        elif type == PowerupType.shoot_rocks:
            self.pixmap = QPixmap("images/shoot_rocks.png")
            # print("powerup shape set")

    # def set_random_position(self):
    #     # self.random_coords = random.randint(1, self.field_width - 1)
    #     self.random_coords = self.powerup.\
    #         set_random_position(self.field_width - 1)
    #     # for rock in self.game.rocks:
    #     #     if rock

    #     # print(self.random_coords)
    #     self.x = self.random_coords + 1
    #     # self.curY = self.field_height - 1 + self.image_size[1]
    #     self.y = 1

    #     self.move(self.x, self.y)
    #     # self.drop_down()
    #     self.update()
    #     # print("powerup position set", self.x, self.y)

    def drop_down(self):
        """Moves the powerup down."""
        self.y += 5
        self.move(self.x, self.y)
        # print("powerup moved")

    def set_duration(self):
        print(self.type)
        self.powerup.set_duration(self.type)

    @property
    def duration(self):
        return self.powerup.powerup_duration

    # def remove_shape(self):
    #     self.hide()
    #     self.destroy()

    # def set_initial_position(self):
    #     self.x = self.field_width / 2 - self.image_size[0]
    #     self.y = self.field_height - 50
    #     self.move(self.x, self.y)

    # def set_shape_size(self):
    #     self.label = QLabel(self)
    #     # self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
    #     #                                          Qt.KeepAspectRatio)
    #     self.label.setPixmap(self.pixmap)
    #     self.image_size = (self.pixmap.width(), self.pixmap.height())
    #     self.width = self.pixmap.width()
    #     self.height = self.pixmap.height()
    #     # print(self.width, self.height, type(self.width))
    #     # print(self.image_size)
    #     self.label.setFixedHeight(self.image_size[1] - 5)
    #     self.label.setFixedWidth(self.image_size[0])
    #     # self.label.setScaledContents(True)


class PlayerUI(ShapeUI):
    def __init__(self, parent, game):
        super().__init__(parent, game)
        # self.main_window = parent
        # self.game = game
        self.player = game.player
        self.speed = game.player_speed
        # self.field_width = self.game.dimensions[0]
        # self.field_height = self.game.dimensions[1]

        self.pixmap = QPixmap("images/smile3.png")
        self.image_height_fix = 48  # 48
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
        """Set the initial position of the player and moves the player
        there.
        """
        # self.move(200, 200)
        # self.position = [self.field_width / 2 - self.image_size[0],
        #                  self.field_height - 50]
        # self.move(self.position[0], self.position[1])
        self.x = (self.field_width - self.image_size[0]) / 2
        self.y = self.field_height - 50
        self.move(self.x, self.y)

    # def set_shape_size(self):
    #     self.label = QLabel(self)
    #     self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
    #                                              Qt.KeepAspectRatio)
    #     self.label.setPixmap(self.myScaledPixmap)
    #     self.image_size = (self.pixmap.width(), self.pixmap.height())
    #     # print(self.image_size)
    #     self.label.setFixedHeight(self.image_size[1] - 48)
    #     self.label.setFixedWidth(self.image_size[0])
    #     self.label.setScaledContents(True)

        # hbox.addWidget(lbl)

        # self.main_window = UserInterface.main_window
        # print(self.main_window)
        # self.setLayout(self.main_window)
        # print(self.game.dimensions[0])

    @property
    def is_player_invincible(self):
        """Checks if the player is invincible"""
        return self.player.is_player_invincible

    def set_player_invinciblity(self):
        """Sets the player's invincibility to the opposite of the current
        value.
        """
        self.player.set_player_invinciblity()

    @pyqtSlot()
    def move_left(self):
        """Moves the player to the left and checks if the move is valid
        (if the move is out of the game field).
        """
        print("left")
        if(self.x - self.speed > 0):
            self.x -= self.speed
            self.move(self.x, self.y)

    @pyqtSlot()
    def move_right(self):
        """Moves the player to the right and checks if the move is valid
        (if the move is out of the game field).
        """
        print("right")
        if(self.x + self.speed < self.field_width -
           self.image_size[0]):
            self.x += self.speed
            self.move(self.x, self.y)
