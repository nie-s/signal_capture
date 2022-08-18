import json

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QFrame, QComboBox, QDialog, QLineEdit
from pygrabber.dshow_graph import FilterGraph

class DeviceDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow
        self.setWindowIcon(QtGui.QIcon('icons/pulse.svg'))
        self.setWindowTitle(str('设备参数设置'))

        with open("para.json", 'r', encoding='UTF-8') as f:
            self.w.parameter = json.load(f)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)

        self.spo2Label = QLabel(self)
        self.spo2Label.setText(str(' 血氧仪参数'))
        self.spo2Label.setStyleSheet('font-weight:bold;margin-top:20px;')

        self.spo2PortTextBoxLabel = QLabel(self)
        self.spo2PortTextBoxLabel.setText('  端口：')
        self.spo2PortTextBoxLabel.setFixedSize(90, 35)
        self.spo2PortTextBox = QLineEdit(self)
        self.spo2PortTextBox.setText(mainWindow.parameter['spo2']['port'])
        self.spo2PortTextBox.setFixedSize(180, 35)

        self.spo2BaudTextBoxLabel = QLabel(self)
        self.spo2BaudTextBoxLabel.setText('  波特率：')
        self.spo2BaudTextBoxLabel.setFixedSize(90, 35)
        self.spo2BaudTextBox = QLineEdit(self)
        self.spo2BaudTextBox.setText(str(mainWindow.parameter['spo2']['baudrate']))
        self.spo2BaudTextBox.setFixedSize(180, 35)

        self.horizontalSpacer = QFrame()
        self.horizontalSpacer.setFrameShape(QFrame.HLine)

        self.eggLabel = QLabel(self)
        self.eggLabel.setText(str(' 脑电仪参数'))
        self.eggLabel.setStyleSheet('font-weight:bold;margin-top:10px;')

        self.eggPortTextBoxLabel = QLabel(self)
        self.eggPortTextBoxLabel.setText('  端口：')
        self.eggPortTextBoxLabel.setFixedSize(90, 35)
        self.eggPortTextBox = QLineEdit(self)
        self.eggPortTextBox.setText(mainWindow.parameter['egg']['port'])
        self.eggPortTextBox.setFixedSize(180, 35)

        self.eggBaudTextBoxLabel = QLabel(self)
        self.eggBaudTextBoxLabel.setText('  波特率：')
        self.eggBaudTextBoxLabel.setFixedSize(90, 35)
        self.eggBaudTextBox = QLineEdit(self)
        self.eggBaudTextBox.setText(str(mainWindow.parameter['egg']['baudrate']))
        self.eggBaudTextBox.setFixedSize(180, 35)

        self.horizontalSpacer_2 = QFrame()
        self.horizontalSpacer_2.setFrameShape(QFrame.HLine)

        self.cameraLabel = QLabel(self)
        self.cameraLabel.setText('摄像头选择')
        self.cameraLabel.setStyleSheet('font-weight:bold;margin-top:10px;')

        self.cameraChooseInput = QComboBox(self)
        self.cameraChooseInput.setFixedSize(180, 35)

        graph = FilterGraph()
        self.cameraChooseInput.addItems(graph.get_input_devices())

        # self.cameraChooseInput.currentIndexChanged[int].connect(self.cho)

        self.confirmButton = QtWidgets.QPushButton(self)
        self.confirmButton.setText("确定")
        self.confirmButton.clicked.connect(self.confirm)
        self.confirmButton.setGeometry(200, 600, 100, 40)

        self.warningText = QtWidgets.QLabel(self)
        self.warningText.setStyleSheet("color:red")
        self.warningText.setGeometry(200, 560, 100, 40)

        self.layout.addWidget(self.spo2Label, 0, 0)
        self.layout.addWidget(self.spo2PortTextBoxLabel, 1, 0)
        self.layout.addWidget(self.spo2PortTextBox, 1, 1)
        self.layout.addWidget(self.spo2BaudTextBoxLabel, 2, 0)
        self.layout.addWidget(self.spo2BaudTextBox, 2, 1)

        self.layout.addWidget(self.horizontalSpacer, 3, 0, 1, 3)
        self.layout.addWidget(self.eggLabel, 4, 0)
        self.layout.addWidget(self.eggPortTextBoxLabel, 5, 0)
        self.layout.addWidget(self.eggPortTextBox, 5, 1)
        self.layout.addWidget(self.eggBaudTextBoxLabel, 6, 0)
        self.layout.addWidget(self.eggBaudTextBox, 6, 1)

        self.layout.addWidget(self.horizontalSpacer_2, 7, 0, 1, 3)
        self.layout.addWidget(self.cameraLabel, 8, 0)
        self.layout.addWidget(self.cameraChooseInput, 8, 1)

        self.setLayout(self.layout)
        self.adjustSize()
        self.resize(500, 680)

    def confirm(self):
        if self.spo2PortTextBox.text() == "" or self.spo2BaudTextBox.text() == "":
            self.warningText.setText("参数不得为空！")
            return

        self.w.parameter = {
            "spo2": {
                "port": self.spo2PortTextBox.text(),
                "baudrate": int(self.spo2BaudTextBox.text()),
            },
            "egg": {
                "port": self.eggPortTextBox.text(),
                "baudrate": int(self.eggBaudTextBox.text()),
            },
            "camera": {
                "index": self.cameraChooseInput.currentIndex(),
            }
        }

        with open("para.json", "w") as f:
            f.write(json.dumps(self.w.parameter, ensure_ascii=False, indent=4, separators=(',', ':')))

        self.close()
