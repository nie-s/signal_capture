import sys

from PyQt5.QtWidgets import *

from view.LoginView.login import LoginController
from view.VideoView.video import MainWinController


class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class ViewController:
    def loadLoginView(self):
        self.viewlogin = LoginController()
        self.viewlogin.loginSignal.connect(self.loadVideoView)
        self.viewlogin.show()

    def loadVideoView(self, str):
        self.viewVideo = MainWinController()
        self.viewVideo.play()
        self.viewVideo.showMaximized()
        self.viewVideo.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ViewController()
    view.loadLoginView()
    sys.exit(app.exec_())
