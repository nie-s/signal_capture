import json
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QFrame, QComboBox, QDialog, QLineEdit, QWidget, QScrollArea, QApplication, \
    QScrollBar
from pygrabber.dshow_graph import FilterGraph


class DeviceDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow
        self.setWindowIcon(QtGui.QIcon('icons/pulse.svg'))
        self.setWindowTitle(str('设备参数设置'))

        # 把para.json里的参数导入（作为默认初始参数）
        with open("para.json", 'r', encoding='UTF-8') as f:
            self.w.parameter = json.load(f)

        # 一系列ui设计
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)

        # 滚轮
        # self.qscrollbar = QScrollBar()
        # self.qscrollbar.setRange(0,2000)
        # self.qscrollbar.sliderMoved.connect(self.slidermove)
        # 滚动条
        self.scrollFiller = QWidget()
        self.scrollFiller.setMinimumSize(400, 680)

        self.spo2Label = QLabel(self.scrollFiller)
        self.spo2Label.setText(str(' 血氧仪参数'))
        self.spo2Label.setStyleSheet('font-weight:bold;margin-top:20px;')

        self.spo2PortTextBoxLabel = QLabel(self.scrollFiller)
        self.spo2PortTextBoxLabel.setText('  端口：')
        self.spo2PortTextBoxLabel.setFixedSize(90, 35)
        self.spo2PortTextBox = QLineEdit(self.scrollFiller)
        self.spo2PortTextBox.setText(mainWindow.parameter['spo2']['port'])
        self.spo2PortTextBox.setFixedSize(180, 35)

        self.spo2BaudTextBoxLabel = QLabel(self.scrollFiller)
        self.spo2BaudTextBoxLabel.setText('  波特率：')
        self.spo2BaudTextBoxLabel.setFixedSize(90, 35)
        self.spo2BaudTextBox = QLineEdit(self.scrollFiller)
        self.spo2BaudTextBox.setText(str(mainWindow.parameter['spo2']['baudrate']))
        self.spo2BaudTextBox.setFixedSize(180, 35)

        self.horizontalSpacer = QFrame()
        self.horizontalSpacer.setFrameShape(QFrame.HLine)

        self.eggLabel = QLabel(self.scrollFiller)
        self.eggLabel.setText(str(' 脑电仪参数'))
        self.eggLabel.setStyleSheet('font-weight:bold;margin-top:10px;')

        self.eggPortTextBoxLabel = QLabel(self.scrollFiller)
        self.eggPortTextBoxLabel.setText('  端口：')
        self.eggPortTextBoxLabel.setFixedSize(90, 35)
        self.eggPortTextBox = QLineEdit(self.scrollFiller)
        self.eggPortTextBox.setText(mainWindow.parameter['egg']['port'])
        self.eggPortTextBox.setFixedSize(180, 35)

        self.eggBaudTextBoxLabel = QLabel(self.scrollFiller)
        self.eggBaudTextBoxLabel.setText('  波特率：')
        self.eggBaudTextBoxLabel.setFixedSize(90, 35)
        self.eggBaudTextBox = QLineEdit(self.scrollFiller)
        self.eggBaudTextBox.setText(str(mainWindow.parameter['egg']['baudrate']))
        self.eggBaudTextBox.setFixedSize(180, 35)

        self.horizontalSpacer_2 = QFrame()
        self.horizontalSpacer_2.setFrameShape(QFrame.HLine)

        self.cameraLabel = QLabel(self.scrollFiller)
        self.cameraLabel.setText('摄像头选择')
        self.cameraLabel.setStyleSheet('font-weight:bold;margin-top:10px;')

        self.cameraChooseInput = QComboBox(self.scrollFiller)
        self.cameraChooseInput.setFixedSize(180, 35)

        graph = FilterGraph()
        self.cameraChooseInput.addItems(graph.get_input_devices())

        # self.cameraChooseInput.currentIndexChanged[int].connect(self.cho)
        # --------------------------------------------------------------
        '''
        self.horizontalSpacer_3 = QFrame()
        self.horizontalSpacer_3.setFrameShape(QFrame.HLine)

        self.videoLabel = QLabel(self.scrollFiller)
        self.videoLabel.setText(str(' 视频相关参数'))
        self.videoLabel.setStyleSheet('font-weight:bold;margin-top:20px;')

        self.videoTextBoxLabel = QLabel(self.scrollFiller)
        self.videoTextBoxLabel.setText('  视频地址  ')
        self.videoTextBoxLabel.setFixedSize(90, 35)
        self.videoTextBox = QLineEdit(self.scrollFiller)
        self.videoTextBox.setText(mainWindow.parameter['video_info']['video'])
        self.videoTextBox.setFixedSize(180, 35)

        self.videoNumTextBoxLabel = QLabel(self.scrollFiller)
        self.videoNumTextBoxLabel.setText('  片段数量：')
        self.videoNumTextBoxLabel.setFixedSize(90, 35)
        self.videoNumTextBox = QLineEdit(self.scrollFiller)
        self.videoNumTextBox.setText(str(mainWindow.parameter['video_info']['num']))
        self.videoNumTextBox.setFixedSize(180, 35)

        self.time1TextBoxLabel = QLabel(self.scrollFiller)
        self.time1TextBoxLabel.setText('视频时长1(ms):')
        self.time1TextBoxLabel.setFixedSize(90, 35)
        self.time1TextBox = QLineEdit(self.scrollFiller)
        self.time1TextBox.setText(str(mainWindow.parameter['video_info']['time1']))
        self.time1TextBox.setFixedSize(180, 35)

        self.link1TextBoxLabel = QLabel(self.scrollFiller)
        self.link1TextBoxLabel.setText('问卷链接1:')
        self.link1TextBoxLabel.setFixedSize(90, 35)
        self.link1TextBox = QLineEdit(self.scrollFiller)
        self.link1TextBox.setText(str(mainWindow.parameter['video_info']['link1']))
        self.link1TextBox.setFixedSize(180, 35)

        self.time2TextBoxLabel = QLabel(self.scrollFiller)
        self.time2TextBoxLabel.setText('视频时长2(ms):')
        self.time2TextBoxLabel.setFixedSize(90, 35)
        self.time2TextBox = QLineEdit(self.scrollFiller)
        self.time2TextBox.setText(str(mainWindow.parameter['video_info']['time2']))
        self.time2TextBox.setFixedSize(180, 35)

        self.link2TextBoxLabel = QLabel(self.scrollFiller)
        self.link2TextBoxLabel.setText('问卷链接2:')
        self.link2TextBoxLabel.setFixedSize(90, 35)
        self.link2TextBox = QLineEdit(self.scrollFiller)
        self.link2TextBox.setText(str(mainWindow.parameter['video_info']['link2']))
        self.link2TextBox.setFixedSize(180, 35)

        self.time3TextBoxLabel = QLabel(self.scrollFiller)
        self.time3TextBoxLabel.setText('视频时长3(ms):')
        self.time3TextBoxLabel.setFixedSize(90, 35)
        self.time3TextBox = QLineEdit(self.scrollFiller)
        self.time3TextBox.setText(str(mainWindow.parameter['video_info']['time3']))
        self.time3TextBox.setFixedSize(180, 35)

        self.link3TextBoxLabel = QLabel(self.scrollFiller)
        self.link3TextBoxLabel.setText('问卷链接3:')
        self.link3TextBoxLabel.setFixedSize(90, 35)
        self.link3TextBox = QLineEdit(self.scrollFiller)
        self.link3TextBox.setText(str(mainWindow.parameter['video_info']['link3']))
        self.link3TextBox.setFixedSize(180, 35)

        self.time4TextBoxLabel = QLabel(self.scrollFiller)
        self.time4TextBoxLabel.setText('视频时长4(ms):')
        self.time4TextBoxLabel.setFixedSize(90, 35)
        self.time4TextBox = QLineEdit(self.scrollFiller)
        self.time4TextBox.setText(str(mainWindow.parameter['video_info']['time4']))
        self.time4TextBox.setFixedSize(180, 35)

        self.link4TextBoxLabel = QLabel(self.scrollFiller)
        self.link4TextBoxLabel.setText('问卷链接4:')
        self.link4TextBoxLabel.setFixedSize(90, 35)
        self.link4TextBox = QLineEdit(self.scrollFiller)
        self.link4TextBox.setText(str(mainWindow.parameter['video_info']['link4']))
        self.link4TextBox.setFixedSize(180, 35)
'''
        self.confirmButton = QtWidgets.QPushButton(self)
        self.confirmButton.setText("确定")
        self.confirmButton.clicked.connect(self.confirm)  # 链接确定按钮到 “确定"函数
        self.confirmButton.setGeometry(200, 1200, 100, 40)

        self.warningText = QtWidgets.QLabel(self)
        self.warningText.setStyleSheet("color:red")
        self.warningText.setGeometry(200, 560, 100, 40)

        # -----------------------------------------------------------------------------
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

        '''
        self.layout.addWidget(self.horizontalSpacer_3, 9, 0, 1, 3)
        self.layout.addWidget(self.videoLabel, 10, 0)
        self.layout.addWidget(self.videoTextBoxLabel, 11, 0)
        self.layout.addWidget(self.videoTextBox, 11, 1)
        self.layout.addWidget(self.videoNumTextBoxLabel, 12, 0)
        self.layout.addWidget(self.videoNumTextBox, 12, 1)
        self.layout.addWidget(self.time1TextBoxLabel, 13, 0)
        self.layout.addWidget(self.time1TextBox, 13, 1)
        self.layout.addWidget(self.link1TextBoxLabel, 14, 0)
        self.layout.addWidget(self.link1TextBox, 14, 1)
        self.layout.addWidget(self.time2TextBoxLabel, 15, 0)
        self.layout.addWidget(self.time2TextBox, 15, 1)
        self.layout.addWidget(self.link2TextBoxLabel, 16, 0)
        self.layout.addWidget(self.link2TextBox, 16, 1)
        self.layout.addWidget(self.time3TextBoxLabel, 17, 0)
        self.layout.addWidget(self.time3TextBox, 17, 1)
        self.layout.addWidget(self.link3TextBoxLabel, 18, 0)
        self.layout.addWidget(self.link3TextBox, 18, 1)
        self.layout.addWidget(self.time4TextBoxLabel, 19, 0)
        self.layout.addWidget(self.time4TextBox, 19, 1)
        self.layout.addWidget(self.link4TextBoxLabel, 20, 0)
        self.layout.addWidget(self.link4TextBox, 20, 1)
        '''
        self.scrollFiller.setLayout(self.layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.scrollFiller)

        self.overallLayout = QtWidgets.QGridLayout()
        self.overallLayout.addWidget(self.scroll)
        self.overallLayout.addWidget(self.confirmButton)
        self.overallLayout.addWidget(self.warningText)
        self.setLayout(self.overallLayout)
        self.adjustSize()
        self.resize(500, 680)

    def confirm(self):
        if self.spo2PortTextBox.text() == "" or self.spo2BaudTextBox.text() == "":
            self.warningText.setText("参数不得为空！")
            return

        self.w.parameter = {  # 根据用户的输入更新端口和波特率等参数
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
            },
            "video_info": [
                # "video": self.videoTextBox.text(),
                # "num": int(self.videoNumTextBox.text()),
                # "time1": int(self.time1TextBox.text()),
                # "link1": self.link1TextBox.text(),
                # "time2": int(self.time2TextBox.text()),
                # "link2": self.link2TextBox.text(),
                # "time3": int(self.time3TextBox.text()),
                # "link3": self.link3TextBox.text(),
                # "time4": int(self.time4TextBox.text()),
                # "link4": self.link4TextBox.text()
                self.w.parameter["video_info"]
            ]
        }

        # 将用户更新的参数记录下来，作为下一次的默认初始参数
        with open("para.json", "w") as f:
            f.write(json.dumps(self.w.parameter, ensure_ascii=False, indent=4, separators=(',', ':')))

        self.close()
