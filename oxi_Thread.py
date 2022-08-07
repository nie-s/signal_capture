import datetime
import time

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QTimer


class LiveThread(QtCore.QThread):
    def __init__(self, oxi, w):
        super().__init__()
        self.oxi = oxi
        self.w = w
        self.lastStart = 0
        self.lastEnd = 0
        self.is_updating = False

    def run(self):
        self.w.pw.pulse_curve.clear()

        self.oxi.initiate_device()
        self.oxi.send_cmd(self.oxi.cmd_get_live_data)
        self.oxi.currentdatetime = QtCore.QDateTime.currentDateTime()
        self.oxi.starttime = time.time()
        while self.w.live_running:
            try:
                self.update_plot()
            except (TypeError):
                # except (TypeError, bluetooth.btcommon.BluetoothError):
                # The following if condition prevents printing the restarting message
                # if oxi.close_device is called while thread is running
                if self.w.live_running:
                    print('Something happened.\nRestarting live feed ...')
                    self.oxi.initiate_device()
                    self.oxi.send_cmd(self.oxi.cmd_get_live_data)

    def append_plot_data(self, now_time, pulse_rate, spo2):
        self.oxi.pulse_xdata.append(now_time - self.oxi.starttime)
        self.oxi.pulse_ydata.append(pulse_rate)
        self.oxi.spo2_xdata.append(now_time - self.oxi.starttime)
        self.oxi.spo2_ydata.append(spo2)

    def update_plot(self):
        finger_out = False
        counter = 0

        while self.w.live_running:
            self.oxi.timer = time.time()

            data = self.w.oxi.process_data()
            finger = data[2]
            pulse_rate = data[3]
            spo2 = data[4]
            localtime = data[1]

            self.oxi.stored_data.append(data)

            if finger == 'Y':
                # The counter > n condition serves to suppress hiccups where
                # the oximeter reports "Finger out" when it isn't.
                if not finger_out and counter > 20:
                    self.append_plot_data(localtime, 0, 0)
                    finger_out = True
                    counter = 0
                elif not finger_out and counter < 21:
                    self.append_plot_data(localtime, self.oxi.pulse_ydata[-1], self.oxi.spo2_ydata[-1])
                    counter += 1
            elif (pulse_rate == 0) or (spo2 == 0):
                self.append_plot_data(localtime, 0, 0)
                finger_out = False
            else:
                self.append_plot_data(localtime, pulse_rate, spo2)
                finger_out = False

            if (self.oxi.n_data_points % 31) == 0:
                start = self.getStartTime()
                self.w.pw.pulse_curve.setData(self.oxi.pulse_xdata[start: self.oxi.n_data_points],
                                              self.oxi.pulse_ydata[start: self.oxi.n_data_points])

                self.w.pw.spo2_curve.setData(self.oxi.spo2_xdata[start: self.oxi.n_data_points],
                                             self.oxi.spo2_ydata[start: self.oxi.n_data_points])

            self.oxi.n_data_points += 1

    def getStartTime(self, is_csv=False):
        if is_csv:
            now = self.oxi.pulse_xdata[self.lastEnd]
        else:
            now = self.oxi.pulse_xdata[len(self.oxi.pulse_xdata) - 1]

        if now < 10:
            return 0
        for i in range(0, len(self.oxi.pulse_xdata)):
            if now - 10 <= self.oxi.pulse_xdata[i]:
                self.lastStart = self.oxi.pulse_xdata[i]
                return i
        return 0

    def plotStoredData(self):
        self.oxi.pulse_xdata = []
        self.oxi.pulse_ydata = []
        self.w.pw.pulse_curve.clear()

        for data in self.oxi.stored_data:
            self.oxi.pulse_ydata.append(data[2])
            self.oxi.pulse_xdata.append(data[0])
            self.oxi.spo2_ydata.append(data[2])
            self.oxi.spo2_xdata.append(data[0])

        self.csv_timer = QTimer(self)
        self.csv_timer.start(1000)
        self.csv_timer.timeout.connect(self.updateCsvPlot)

    def updateCsvPlot(self):

        length = len(self.w.oxi.stored_data)
        # while not ending:
        start = self.getStartTime(True)
        self.lastEnd = min(self.lastEnd + 60, length)
        self.w.pw.pulse_curve.setData(self.w.oxi.pulse_xdata[start: self.lastEnd],
                                      self.w.oxi.pulse_ydata[start: self.lastEnd])

        self.w.pw.spo2_curve.setData(self.w.oxi.spo2_xdata[start: self.lastEnd],
                                      self.w.oxi.spo2_ydata[start: self.lastEnd])

        if length <= self.lastEnd:
            self.csv_timer.stop()
            self.w.statusBar.showMessage('状态：已结束')
