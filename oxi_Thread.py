import datetime
import time

from PyQt5 import QtGui, QtCore, QtWidgets


class LiveThread(QtCore.QThread):
    def __init__(self, oxi, w):
        super().__init__()
        self.oxi = oxi
        self.w = w
        self.lastStart = 0

    def run(self):
        """
        Initiates live data feed and keeps it alive as long as our main QWidget is running.
        """
        # self.w.cw.pulse_curve.clear()
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

    def append_plot_data(self, time, pulse_rate):
        """
        Helper function for self.update_plot() to append the actual live
        data to the lists which get plotted eventually.
        """
        # Pulse rate and finger can be supplied as arguments to support appending
        # 'Finger out' and 'Low signal quality' events; see self.update_plot()
        # for more details
        self.oxi.pulse_xdata.append(time - self.oxi.starttime)
        self.oxi.pulse_ydata.append(pulse_rate)

    def update_plot(self):
        finger_out = False
        counter = 0

        while self.w.live_running:
            data = self.w.oxi.process_data()
            finger = data[2]
            pulse_rate = data[3]
            spo2 = data[4]
            time = data[1]

            self.oxi.timer = time.time()
            self.oxi.stored_data.append(data)

            if finger == 'Y':
                # The counter > n condition serves to suppress hiccups where
                # the oximeter reports "Finger out" when it isn't.
                if not finger_out and counter > 20:
                    self.append_plot_data(time, 0)
                    finger_out = True
                    counter = 0
                elif not finger_out and counter < 21:
                    self.append_plot_data(time, self.oxi.pulse_ydata[-1])
                    counter += 1
            elif (pulse_rate == 0) or (spo2 == 0):
                self.append_plot_data(time, 0)
                finger_out = False
            else:
                self.append_plot_data(time, pulse_rate)
                finger_out = False

            if (self.oxi.n_data_points % 31) == 0:
                start = self.getStartTime()
                self.w.pw.pulse_curve.setData(self.oxi.pulse_xdata[start: self.oxi.n_data_points],
                                              self.oxi.pulse_ydata[start: self.oxi.n_data_points])

            self.oxi.n_data_points += 1

    def getStartTime(self):
        now = self.oxi.pulse_xdata[len(self.oxi.pulse_xdata) - 1]
        if now < 10:
            return 0
        for i in range(0, len(self.oxi.pulse_xdata)):
            if now - 10 <= self.oxi.pulse_xdata[i]:
                self.lastStart = self.oxi.pulse_xdata[i]
                return i
        return 0
