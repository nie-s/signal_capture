from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from view.LoginView.loginUI import Ui_Form


class LoginController(QWidget, Ui_Form):
    loginSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(LoginController, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btnEnterClicked)

    def btnEnterClicked(self):
        print("enter clicked")

        # 中间可以添加处理逻辑

        self.loginSignal.emit("login")
        self.close()

    def btnExitClicked(self):
        print("Exit clicked")
        self.close()
