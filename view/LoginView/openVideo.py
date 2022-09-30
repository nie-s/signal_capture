from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from view.LoginView.loginUI import Ui_Form
from view.VideoView.video import VideoPlayer


class OpenVideo(QWidget, Ui_Form):
    loginSignal = pyqtSignal(str)

    def __init__(self, w, parent=None):
        super(OpenVideo, self).__init__(parent)
        self.setupUi(self)
        self.w = w
        self.pushButton.clicked.connect(self.btnEnterClicked)

    def btnEnterClicked(self):
        print("enter clicked")
        self.viewVideo = VideoPlayer(self.w)
        self.viewVideo.play()
        self.viewVideo.showMaximized()
        self.viewVideo.show()
        self.close()

    def btnExitClicked(self):
        print("Exit clicked")
        self.close()
