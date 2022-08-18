from view.LoginView.login import LoginController
from view.VideoView.video import MainWinController


class ViewController:
    def __init__(self, w):
        self.w = w

    def loadLoginView(self):
        self.viewlogin = LoginController()
        self.viewlogin.loginSignal.connect(self.loadVideoView)
        self.viewlogin.show()

    def loadVideoView(self, str):
        self.viewVideo = MainWinController(self.w)
        self.viewVideo.play()
        self.viewVideo.showMaximized()
        self.viewVideo.show()
