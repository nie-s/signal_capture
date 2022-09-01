import datetime

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QComboBox

from view.plot_widget import PlotWidget


class MainWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow

        # Use a grid layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignHCenter)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)

        self.spaceHolderLeft = QtWidgets.QLabel('')
        self.spaceHolderRight = QtWidgets.QLabel('')
        self.spaceHolderRight.setFixedSize(265, 35)

        self.nameTextBoxLabel = QLabel(self)
        self.nameTextBoxLabel.setText(str('姓名:'))
        self.nameTextBoxLabel.setFixedSize(50, 35)

        self.nameTextBox = QLineEdit(self)
        self.nameTextBox.setFixedSize(180, 35)

        self.ageTextBoxLabel = QLabel(self)
        self.ageTextBoxLabel.setText(str('年龄:'))
        self.ageTextBoxLabel.setFixedSize(50, 35)

        self.ageTextBox = QLineEdit(self)
        self.ageTextBox.setFixedSize(180, 35)

        self.sexTextBoxLabel = QLabel(self)
        self.sexTextBoxLabel.setText(str('性别:'))
        self.sexTextBoxLabel.setFixedSize(50, 35)

        self.sexTextBox = QComboBox(self)
        self.sexTextBox.setFixedSize(180, 35)
        self.sexTextBox.addItems(["女", "男", ])

        self.idTextBoxLabel = QLabel(self)
        self.idTextBoxLabel.setText(str('编号:'))
        self.idTextBoxLabel.setFixedSize(50, 35)

        self.idTextBox = QLineEdit(self)
        self.idTextBox.setFixedSize(180, 35)

        self.warningLabel = QLabel(self)
        self.warningLabel.setStyleSheet('color:red')
        self.warningLabel.setFixedSize(180, 35)

        self.confirmButton = QtWidgets.QPushButton(self)
        self.confirmButton.setText('确定')
        self.confirmButton.setGeometry(350, 410, 100, 40)
        self.confirmButton.clicked.connect(self.confirm)

        self.layout.addWidget(self.spaceHolderLeft, 0, 0)
        self.layout.addWidget(self.spaceHolderRight, 0, 3)

        self.layout.addWidget(self.nameTextBoxLabel, 0, 1)
        self.layout.addWidget(self.nameTextBox, 0, 2)

        self.layout.addWidget(self.ageTextBoxLabel, 1, 1)
        self.layout.addWidget(self.ageTextBox, 1, 2)

        self.layout.addWidget(self.sexTextBoxLabel, 2, 1)
        self.layout.addWidget(self.sexTextBox, 2, 2)

        self.layout.addWidget(self.idTextBoxLabel, 3, 1)
        self.layout.addWidget(self.idTextBox, 3, 2)

        self.layout.addWidget(self.warningLabel, 4, 2)

    def confirm(self):
        self.subjectName = self.nameTextBox.text()
        self.subjectAge = self.ageTextBox.text()

        if self.sexTextBox.currentIndex() == 0:
            self.subjectSex = "女"
        else:
            self.subjectSex = "男"

        self.subjectId = self.idTextBox.text()

        if self.subjectName == "" or self.subjectId == "" or self.subjectSex == "" or self.subjectAge == "":
            self.warningLabel.setText("请输入完整信息！")
            return

        self.w.information = {
            'subjectName': self.subjectName,
            'subjectAge': self.subjectAge,
            'subjectSex': self.subjectSex,
            'subjectId': self.subjectId,
        }

        now = datetime.datetime.now()
        self.w.start = str(now.strftime("%Y-%m-%d-%H-%M-%S"))

        self.w.folder = 'data/' + self.w.information['subjectId'] + '-' + self.w.information[
            'subjectName'] + "/" + self.w.start
        self.w.pw = PlotWidget(self.w)
        self.w.setCentralWidget(self.w.pw)
        self.w.pw.checkDevice()
