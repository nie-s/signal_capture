import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *

from view.VideoView.simple_videoUI import Ui_Form


class MainWinController(QWidget, Ui_Form):
    endSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(MainWinController, self).__init__(parent)
        self.setupUi(self)
        # 播放器
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_player)
        # self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile("10s静音.mp4")))
        self.player.mediaStatusChanged.connect(self.recordTimeInfo)

    def play(self):
        self.player.play()
        t = time.time()
        print("记录开始时间")
        with open('timeInfo.txt', 'w') as f:
            f.write("视频开始时间： " + str(t) + "\n")

        # 在类中定义一个定时器,并在构造函数中设置启动及其信号和槽
        self.timer1 = QTimer(self)
        self.timer2 = QTimer(self)
        self.timer3 = QTimer(self)
        self.timer4 = QTimer(self)
        # 设置计时间隔并设置单词计时(1000ms == 1s)
        self.timer1.setSingleShot(True)
        self.timer2.setSingleShot(True)
        self.timer3.setSingleShot(True)
        self.timer4.setSingleShot(True)

        self.timer1.start(10000)  # 第一段2:59, 3:02s弹出问卷182000
        # self.timer1.start(182000) #第一段2:59, 3:02s弹出问卷182000
        self.timer2.start(430000)  # 第二段3:08, 7:10s弹出问卷
        self.timer3.start(700000)  # 第三段3:29, 11:40s弹出问卷
        self.timer4.start(935000)  # 第四段2:55, 15:35s弹出问卷
        # 计时结束调用timeout_slot()方法,注意不要加（）
        self.timer1.timeout.connect(self.popQues1)
        self.timer2.timeout.connect(self.popQues2)

    def recordTimeInfo(self):
        if self.player.mediaStatus() == 7:
            print("记录结束时间")
            t = time.time()
            with open('timeInfo.txt', 'a') as f:
                f.write("视频结束时间： " + str(t) + "\n")

    def popQues1(self):
        self.quesView = Questionnaire()
        self.quesView.showWidget(1)

    def popQues2(self):
        self.quesView = Questionnaire()
        self.quesView.showWidget(2)


# 弹出窗体类
class Questionnaire(QtWidgets.QWidget):
    def __init__(self):
        super(Questionnaire, self).__init__()

        self.ques1 = QLabel('<a href="https://www.wenjuan.com/s/UZBZJvF6E0/">请在10s内点击并填写调查问卷')
        self.ques1.setOpenExternalLinks(True)
        self.ques2 = QLabel('<a href="https://www.wenjuan.com/s/r6nM32A/">hello,请在10s内点击并填写调查问卷')
        self.ques2.setOpenExternalLinks(True)
        self.ques3 = QLabel('<a href="https://www.wenjuan.com/s/N7jEVbS/">hello,请在10s内点击并填写调查问卷')
        self.ques3.setOpenExternalLinks(True)
        self.ques4 = QLabel('<a href="https://www.wenjuan.com/s/N7jEVbS/">hello,请在10s内点击并填写调查问卷')
        self.ques4.setOpenExternalLinks(True)

    def showWidget(self, select):
        ques = {
            1: self.ques1,
            2: self.ques2
        }
        # 设置大小
        self.resize(300, 300)
        # 设置标题
        self.setWindowTitle("调查问卷")

        # 垂直布局
        layout = QVBoxLayout()

        layout.addStretch(1)

        # 链接
        layout.addWidget(ques.get(select))

        layout.addStretch(1)

        self.setLayout(layout)
        self.show()

        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.close)  # 计时结束调用operate()方法
        self.timer.setSingleShot(True)
        self.timer.start(10000)  # 设置计时间隔并启动 2s后关闭窗口
