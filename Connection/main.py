import sys

from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from splash_screen import SplashScreen

import images


def except_exceptions(*args):
    sys.__excepthook__(*args)


class MainWidnow(QMainWindow):

    player = QMediaPlayer()

    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.title.mouseMoveEvent = self.move_window

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.close_window_system.clicked.connect(self.close)

        self.close_button.clicked.connect(lambda: self.close())

        self.player.setMedia(QMediaContent(QUrl.fromLocalFile('sounds/error.wav')))
        self.player.play()

    def move_window(self, event) -> None:
        """Function making window able to be moved"""
        if "drag_position" in self.__dict__:
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_position)
                self.drag_position = event.globalPos()
                event.accept()

    def mousePressEvent(self, event) -> None:
        """Event activating when a mouse button getting pressed"""
        self.drag_position = event.globalPos()


if __name__ == '__main__':
    sys.excepthook = except_exceptions
    window = QApplication(sys.argv)
    app = SplashScreen(MainWidnow)
    app.show()
    sys.exit(window.exec())