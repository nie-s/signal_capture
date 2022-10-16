import csv
import datetime
import os
import time
import functools

from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *

from view.end_dialog import EndDialog


class VideoPlayer(QWidget):
    endSignal = pyqtSignal()

    def __init__(self, w, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.w = w
        # self.setupUi(self)
        self.stage_count = 0

        # 界面
        self.layout1 = QBoxLayout(QBoxLayout.TopToBottom)
        self.layout2 = QBoxLayout(QBoxLayout.TopToBottom)
        self.closeButton = QtWidgets.QPushButton(self)
        self.wgt_player = QVideoWidget(self)
        self.layout2.addWidget(self.closeButton)
        self.layout1.addWidget(self.wgt_player)
        self.layout2.addWidget(self.wgt_player)

        # 播放器
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_player)

        self.wgt_player.setFullScreen(True)

        self.setLayout(self.layout1)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # 隐藏边框和任务栏
        self.showFullScreen()

        # self.player.mediaStatusChanged.connect(self.recordEndTime)
        self.closeButton.clicked.connect(self.closeEvent)

    # def play_with_our_ques(self):
    #     self.player.play()
    #
    #     if not os.path.isdir(self.w.folder):
    #         os.makedirs(self.w.folder)
    #
    #     now = datetime.datetime.now()
    #     nowtimestamp = time.time()
    #     nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    #
    #     print("记录开始时间")
    #     with open(self.w.folder + '/actions.csv', 'a') as f:
    #         datawriter = csv.writer(f, delimiter=',')
    #         datawriter.writerow([nowtime, nowtimestamp, '点击开始'])
    #
    #     # 在类中定义一个定时器,并在构造函数中设置启动及其信号和槽
    #     self.timer1 = QTimer(self)
    #     self.timer2 = QTimer(self)
    #     self.timer3 = QTimer(self)
    #     self.timer4 = QTimer(self)
    #     # 设置计时间隔并设置单词计时(1000ms == 1s)
    #     self.timer1.setSingleShot(True)
    #     self.timer2.setSingleShot(True)
    #     self.timer3.setSingleShot(True)
    #     self.timer4.setSingleShot(True)
    #
    #     self.timer1.start(10)  # 第一段2:59, 3:02s弹出问卷182000
    #     # self.timer1.start(182000) #第一段2:59, 3:02s弹出问卷182000
    #     self.timer2.start(10000)  # 第二段3:08, 7:10s弹出问卷
    #     self.timer3.start(700000)  # 第三段3:29, 11:40s弹出问卷
    #     self.timer4.start(935000)  # 第四段2:55, 15:35s弹出问卷
    #     # 计时结束调用timeout_slot()方法,注意不要加（）
    #     self.timer1.timeout.connect(lambda: self.popQues(1))
    #     self.timer2.timeout.connect(lambda: self.popQues(2))
    #     self.timer3.timeout.connect(lambda: self.popQues(3))
    #     self.timer4.timeout.connect(lambda: self.popQues(4))

    def play(self):
        if (self.player.mediaStatus() != 7) and self.stage_count > 0: return

        if self.stage_count >= self.w.parameter['stage_num']:
            self.recordEndTime()
            return

        item = self.w.parameter["video_info"][self.stage_count]

        if "video" in item.keys():
            path = self.w.parameter["video_info"][self.stage_count]["video"]
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.player.play()
            self.player.mediaStatusChanged.connect(self.play)

        elif "link" in item.keys():
            self.popQues(self.w.parameter["video_info"][self.stage_count]["link"])
            # self.timer.start(2000)
            # self.timer.setSingleShot(True)
            # self.timer.timeout.connect(
            #     functools.partial(self.popQues, self.w.parameter["video_info"][self.video_count]["link"]))
        else:
            raise Exception("wrong json!")

        self.stage_count = self.stage_count + 1


    # for i in range(1, video_num + 1):
    #     start_time += self.w.parameter["video_info"]["time" + str(i)]
    #     self.timer[i].setSingleShot(True)  # 设置计时间隔并设置单词计时(1000ms == 1s)
    #     self.timer[i].start(start_time + 2000)  # 弹出问卷
    #     start_time += 60000  # 设置计时间隔并设置单词计时(1000ms == 1s)
    #     print(self.w.parameter["video_info"]["link" + str(i)])
    #     self.timer[i].timeout.connect(
    #         functools.partial(self.popQues, self.w.parameter["video_info"]["link" + str(i)]))

    def recordStartTime(self, num):
        if not os.path.isdir(self.w.folder):
            os.makedirs(self.w.folder)

        now = datetime.datetime.now()
        nowtimestamp = time.time()
        nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        print("记录开始时间")
        with open(self.w.folder + '/actions.csv', 'a') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow([nowtime, nowtimestamp, '视频' + str(num) + '开始'])

    def recordEndTime(self):
        if self.player.mediaStatus() == 7:
            self.wgt_player.setFullScreen(False)
            self.endDialog = EndDialog(self.w, self)
            self.endDialog.exec_()

            print("记录结束时间")
            now = datetime.datetime.now()
            nowtimestamp = time.time()
            nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

            with open(self.w.folder + '/actions.csv', 'a') as f:
                datawriter = csv.writer(f, delimiter=',')
                datawriter.writerow([nowtime, nowtimestamp, '视频结束'])

    # def popQues(self, serial):
    #     self.quesView = Questionnaire_self(self.w, serial)
    #     self.quesView.show()
    def popQues(self, link):
        self.quesView = Questionnaire(link)
        self.quesView.closeQuesSig.connect(self.play)
        self.quesView.show()

    def closeEvent(self):  # 重写关闭函数
        print("Exit clicked")
        self.player.stop()
        print(self)
        self.close()

    # def mouseMoveEvent(self): # 重写鼠标移动事件
    #     self.setLayout(self.layout2)


# 弹出窗体类
class Questionnaire(QtWidgets.QWidget):
    closeQuesSig = pyqtSignal()

    def __init__(self, link):
        super(Questionnaire, self).__init__()

        # 设置大小
        self.resize(300, 300)
        # 设置标题
        self.setWindowTitle("调查问卷")
        self.vbox = QBoxLayout(QBoxLayout.TopToBottom)
        self.vbox.addStretch(1)
        self.ques = QLabel("<a href=\"" + str(link) + "\">请在10s内点击并填写调查问卷")
        self.ques.setOpenExternalLinks(True)
        self.vbox.addWidget(self.ques)
        self.vbox.addStretch(1)
        self.closeButton = QtWidgets.QPushButton(self)
        self.closeButton.setText('已填完问卷，继续')
        self.vbox.addWidget(self.closeButton)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)
        self.closeButton.clicked.connect(self.closeQues)

    def closeQues(self):
        print("closeQues button clicked!")
        self.closeQuesSig.emit()
        self.close()
