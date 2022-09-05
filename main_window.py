import csv
import json
import sys
import time

import cv2
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog

from device.cms50ew import CMS50EW
from device.neuroPy3 import NeuroPy
from device.real_time_video import Emotion
from threads.egg_thread import EggThread
from threads.emotion_thread import EmotionThread
from threads.oxi_thread import LiveThread
from view.device_dialog import DeviceDialog
from view.main_widget import MainWidget
from view.session_dialog import SessionDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.oxi = CMS50EW()
        self.emotion = Emotion()
        self.egg = NeuroPy()

        with open("para.json", 'r', encoding='UTF-8') as f:
            self.parameter = json.load(f)

        self.information = {}

        # 设置任务栏的四个按钮链接
        self.openSessAction = QAction(QtGui.QIcon('icons/document-open-symbolic.svg'),
                                      'Open CSV session file', self)
        self.openSessAction.triggered.connect(self.on_openSessAction)  # 把第一个图标链接到“打开数据文件”函数

        self.serDialogAction = QAction(QtGui.QIcon('icons/usb.svg'), '设备参数设置', self)
        self.serDialogAction.triggered.connect(self.onSerDialogAction)  # 把第二个图标链接到“设置参数”函数

        self.liveRunAction = QAction(QtGui.QIcon('icons/media-playback-start-symbolic.svg'), 'Retrieve live data', self)
        self.liveRunAction.setEnabled(False)  # 先把该按钮禁用（等到登录成功后才能用）
        self.liveRunAction.triggered.connect(self.on_liveRunAction)  # 把第三个图标链接到“查看实时数据”函数
        self.live_running = False  # 定义一个变量记录当前是否正在实时记录

        self.plotStoredDataAction = QAction(QtGui.QIcon('icons/appointment-new.svg'),
                                            'Retrieve recorded data', self)
        self.plotStoredDataAction.setEnabled(False)  # 先把该按钮禁用（等到登录成功后才能用）
        self.plotStoredDataAction.triggered.connect(self.on_plotStoredDataAction)  # 把第四个图标链接到“回放记录的数据”函数

        # 设置任务栏的界面
        toolBar = self.addToolBar('Toolbar')
        toolBar.setMovable(False)
        toolBar.addAction(self.openSessAction)
        toolBar.addAction(self.serDialogAction)
        toolBar.addAction(self.liveRunAction)
        toolBar.addAction(self.plotStoredDataAction)
        toolBar.setIconSize(QtCore.QSize(32, 32))

        self.setWindowTitle('Singal Capture')
        self.setWindowIcon(QtGui.QIcon('icons/pulse.svg'))

        self.adjustSize()
        self.resize(800, 600)

        # 首先显示登陆页面
        self.cw = MainWidget(self)  # 创建主页面窗口（姓名学号那些）
        self.setCentralWidget(self.cw)
        self.pw = None

        self.show()

    def on_openSessAction(self):
        filename = QFileDialog.getOpenFileName(self)[0]  # 返回用户所选择文件的名称，并打开该文件

        if filename:
            self.oxi.open_csv(filename)  # 利用cms50ew里的函数打开csv文件
            sessDialog = SessionDialog(self)  # csv必须不为空才能正常查看数据
            sessDialog.exec_()

    def onSerDialogAction(self):
        self.devDialog = DeviceDialog(self)
        self.devDialog.exec_()

    def on_liveRunAction(self):

        if not self.live_running:  # 若当前不是实时监测状态，则开启该状态

            self.live_running = True
            self.liveThread = LiveThread(self.oxi, self)  # 开启一个血氧脉搏监测线程
            self.liveThread.start()
            time.sleep(0.2)  # ？？？

            self.emotionThread = EmotionThread(self.emotion, self, self.parameter['camera']['index'])
            self.emotionThread.start()

            self.eggThread = EggThread(self.egg, self)
            self.eggThread.start()

            time.sleep(0.2)  # ？？？

            self.liveRunAction.setIcon(QtGui.QIcon('icons/media-playback-stop-symbolic.svg'))
            self.liveRunAction.setEnabled(True)
            self.statusBar.showMessage('Status: Initiating live stream ...')
        else:  # 此时说明是结束实时监测操作
            self.live_running = False
            time.sleep(0.2)  # Give threads the chance to end itself

            self.write()

            self.emotionThread.camera.release()
            self.emotionThread.out.release()
            cv2.destroyAllWindows()

            frame = cv2.imread("icons/placeholder.png")
            frame, _ = pg.makeARGB(frame, None, None, None, False)
            self.img = pg.ImageItem(frame, axisOrder='row-major')
            self.img.show()
            self.pw.ui.vb.addItem(self.img)

            # self.liveRunAction.setIcon(QtGui.QIcon('icons/media-playback-start-symbolic.svg'))
            self.liveRunAction.setEnabled(False)  # 关闭后不能反复打开
            self.statusBar.showMessage('状态：连接关闭')

    def on_plotStoredDataAction(self):
        self.csvThread = LiveThread(self.oxi, self)  # 开启一个csv数据回放线程
        self.csvThread.plotStoredData()

    def openPlotWidget(self):  # 创建曲线图窗口
        if self.pw is None:
            self.pw = pg.PlotWidget(self)
            self.setCentralWidget(self.pw)

        self.plotStoredDataAction.setEnabled(True)

    # def on_plotStoredData(self):

    # time.sleep(1)
    # self.pw.plotStoredData()

    def write(self):
        self.liveThread.oxi.write_csv(self.folder, self.start)
        self.emotionThread.emotion.write_csv(self.folder, self.start)
        self.eggThread.egg.write_csv(self.folder, self.start)
        self.mergeData(self.folder)

        with open(self.folder + '/info.json', "w", encoding="GBK") as f:
            f.write(json.dumps(self.information, ensure_ascii=False, indent=4, separators=(',', ':')))

    def mergeData(self, folder):
        spo2_data = []

        with open(folder + '/spo2.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            total_header = next(csv_reader)

            for row in csv_reader:
                spo2_data.append(row)

        emotion_data = []
        with open(folder + '/emotion.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            total_header.extend(header[2:])
            for row in csv_reader:
                emotion_data.append(row)

        last = 0
        total_length = len(spo2_data)

        for data in emotion_data:
            empty = ['', '', '', '', '', '', '']

            if last > total_length:
                break
            while last < total_length - 1:
                if float(spo2_data[last][1]) - float(data[1]) <= 0 and float(spo2_data[last + 1][1]) - float(
                        data[1]) >= 0:
                    break
                spo2_data[last].extend(empty)
                last = last + 1

            spo2_data[last].extend(data[2:])

        egg_data = []
        with open(folder + '/egg.csv') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            total_header.extend(header[2:])
            for row in csv_reader:
                egg_data.append(row)

        for data in egg_data:
            empty = ['', '', '', '', '', '', '', '', '', '', '', '']

            if last > total_length:
                break
            while last < total_length - 1:
                if float(spo2_data[last][1]) - float(data[1]) <= 0 and float(spo2_data[last + 1][1]) - float(
                        data[1]) >= 0:
                    break
                spo2_data[last].extend(empty)
                last = last + 1

            spo2_data[last].extend(data[2:])

        with open(folder + '/merged.csv', 'w', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(total_header)
            datawriter.writerows(spo2_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()

    app.exec_()
