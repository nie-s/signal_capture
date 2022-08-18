import csv
import datetime
import json
import os
import sys
import time

import cv2
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog

from device.cms50ew import CMS50EW
from device.real_time_video import Emotion
from session_dialog import SessionDialog
from thread.emotion_thread import EmotionThread
from thread.oxi_thread import LiveThread
from view.device_dialog import DeviceDialog
from view.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.oxi = CMS50EW()
        self.emotion = Emotion()

        with open("para.json", 'r', encoding='UTF-8') as f:
            self.parameter = json.load(f)

        self.information = {}

        self.openSessAction = QAction(QtGui.QIcon('icons/document-open-symbolic.svg'),
                                      'Open CSV session file', self)
        self.openSessAction.triggered.connect(self.on_openSessAction)

        serDialogAction = QAction(QtGui.QIcon('icons/usb.svg'), '设备参数设置', self)
        serDialogAction.triggered.connect(self.onSerDialogAction)

        self.liveRunAction = QAction(QtGui.QIcon('icons/media-playback-start-symbolic.svg'), 'Retrieve live data', self)
        self.liveRunAction.setEnabled(False)
        self.liveRunAction.triggered.connect(self.on_liveRunAction)
        self.live_running = False

        self.plotStoredDataAction = QAction(QtGui.QIcon('icons/appointment-new.svg'),
                                            'Retrieve recorded data', self)
        self.plotStoredDataAction.setEnabled(False)
        self.plotStoredDataAction.triggered.connect(self.on_plotStoredDataAction)

        toolBar = self.addToolBar('Toolbar')
        toolBar.setMovable(False)
        toolBar.addAction(self.openSessAction)
        toolBar.addAction(serDialogAction)

        toolBar.addAction(self.liveRunAction)
        toolBar.addAction(self.plotStoredDataAction)
        toolBar.setIconSize(QtCore.QSize(32, 32))

        self.setWindowTitle('Singal Capture')
        self.setWindowIcon(QtGui.QIcon('icons/pulse.svg'))

        self.adjustSize()
        self.resize(800, 600)

        self.cw = MainWidget(self)
        self.setCentralWidget(self.cw)
        self.pw = None

        self.show()

    def onSerDialogAction(self):
        self.devDialog = DeviceDialog(self)
        self.devDialog.exec_()

    def on_liveRunAction(self):

        if not self.live_running:
            now = datetime.datetime.now()
            self.start = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
            self.folder = 'data/' + self.information['subjectId'] + '-' + self.information[
                'subjectName'] + "/" + self.start

            self.live_running = True
            self.liveThread = LiveThread(self.oxi, self)
            self.liveThread.start()
            time.sleep(0.2)

            self.emotionThread = EmotionThread(self.emotion, self, self.parameter['camera']['index'])
            self.emotionThread.start()
            time.sleep(0.2)

            self.liveRunAction.setIcon(QtGui.QIcon('icons/media-playback-stop-symbolic.svg'))
            self.liveRunAction.setEnabled(True)
            self.statusBar.showMessage('Status: Initiating live stream ...')
        else:
            self.live_running = False
            time.sleep(0.2)  # Give thread the chance to end itself

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
            self.liveRunAction.setEnabled(False)
            self.statusBar.showMessage('状态：连接关闭')

    def on_openSessAction(self):
        filename = QFileDialog.getOpenFileName(self)[0]

        if filename:
            self.oxi.open_csv(filename)
            sessDialog = SessionDialog(self)
            sessDialog.exec_()

    def on_plotStoredDataAction(self):
        self.csvThread = LiveThread(self.oxi, self)
        self.csvThread.plotStoredData()

    def openPlotWidget(self):
        if self.pw is None:
            self.pw = pg.PlotWidget(self)
            self.setCentralWidget(self.pw)

        self.plotStoredDataAction.setEnabled(True)

    # def on_plotStoredData(self):

    # time.sleep(1)
    # self.pw.plotStoredData()

    def write(self):
        if not os.path.isdir(self.folder):
            os.makedirs(self.folder)

        self.liveThread.oxi.write_csv(self.folder, self.start)
        self.emotionThread.emotion.write_csv(self.folder, self.start)
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

        with open(folder + '/merged.csv', 'w', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(total_header)
            datawriter.writerows(spo2_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()

    app.exec_()
