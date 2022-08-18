from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimediaWidgets import QVideoWidget


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("观看视频")
        Form.resize(961, 613)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.wgt_player = QVideoWidget(Form)
        self.wgt_player.setStyleSheet("border-radius:7px;\n"
                                      "background-color: rgb(197, 197, 197);")
        self.wgt_player.setObjectName("wgt_player")
        self.verticalLayout.addWidget(self.wgt_player)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "观看视频"))
