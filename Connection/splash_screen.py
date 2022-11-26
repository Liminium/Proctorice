import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

import random

from circular_progress import CircularProgress


INFO = [u"<strong>Connecting</strong> web-camera...", u"<strong>Connection </strong> microphone...",
             u"<strong>Reading</strong> system info...", u"<strong>Logging</strong> keyboard..."]


class SplashScreen(QMainWindow):

    counter = 0
    transparency_degree = 255

    def __init__(self, main_window):
        super().__init__()
        uic.loadUi("splash_interface.ui", self)

        self.data_message.setText(INFO.pop(random.randrange(0, len(INFO))))

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.titles_count = 1
        self.multiplier = 1

        # Creating Progress Bar
        self.progress = CircularProgress(0, width=400, height=400, progress_width=12, is_rounded=True, font_size=35,
                                         color_of_progress=(24, 222, 177),
                                         text_color=(14, 222, 128), bg_color=(99, 99, 99, 199))

        # Moving / resizing
        self.progress.move(25, 13)
        self.progress.setParent(self.centralwidget)

        self.progress.show()

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(25)

        # Timer to make title invisible
        self.timer_ = QTimer()
        self.timer_.timeout.connect(self.make_transparent)
        self.timer_.start(7)

        self.main_window = main_window

    def make_transparent(self):
        """Изменение надписей на SplashScreen"""
        if self.transparency_degree <= 0 or self.transparency_degree >= 255:
            if self.transparency_degree <= 0:
                if self.titles_count == 3:
                    self.data_message.setText(u"<strong>Done.</strong>")
                else:
                    self.data_message.setText(INFO.pop(random.randrange(0, len(INFO))))
                    self.titles_count += 1
            self.multiplier *= -1

        if self.data_message.text() == u"<strong>Done.</strong>" and self.transparency_degree >= 255:
            self.timer_.stop()

        self.transparency_degree += 3 * self.multiplier
        self.data_message.setStyleSheet(f"color: rgb(245, 245, 245, {self.transparency_degree})")

    def update(self):
        """Обновление шкалы ProgressBar'а"""
        # Set value to progress bar

        self.visible_counter = self.counter

        # Wait some seconds after timer reaches 100
        if self.counter > 100:
            self.visible_counter = 100

        self.progress.set_value(self.visible_counter)

        # Close welcome screen and open main app
        if self.counter > 125:
            # Stop timer
            self.timer.stop()

            # Show main window
            self.window_ = self.main_window()
            self.window_.show()

            # Close splash screen
            self.close()

        self.counter += 1
