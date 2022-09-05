import time

from PyQt5 import QtCore


class EggThread(QtCore.QThread):
    def __init__(self, egg, w):
        super().__init__()
        self.egg = egg
        self.w = w
        self.lastStart = 0
        self.lastEnd = 0
        self.is_updating = False

    def run(self):
        # self.w.pw.egg_curve.clear()

        self.egg.currentdatetime = QtCore.QDateTime.currentDateTime()
        self.egg.starttime = time.time()

        while self.w.live_running:
            try:
                self.update_plot()
            except (TypeError):
                if self.w.live_running:
                    print('Something with egg....')
                    self.egg.setup_device()

    def update_plot(self):

        while self.w.live_running:
            self.egg.timer = time.time()
            start = self.getStartTime()

            self.w.pw.attention_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                              self.egg.attention_ydata[start: self.egg.n_data_points])
            self.w.pw.meditation_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                               self.egg.meditation_ydata[start: self.egg.n_data_points])
            self.w.pw.rawValue_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                             self.egg.rawValue_ydata[start: self.egg.n_data_points])
            self.w.pw.delta_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                          self.egg.delta_ydata[start: self.egg.n_data_points])
            # self.w.pw.theta_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
            #                               self.egg.theta_ydata[start: self.egg.n_data_points])
            self.w.pw.lowAlpha_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                             self.egg.lowAlpha_ydata[start: self.egg.n_data_points])
            self.w.pw.highAlpha_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                              self.egg.highAlpha_ydata[start: self.egg.n_data_points])
            self.w.pw.lowBeta_curve.setData(self.egg.egg_xdata[start: self.egg.n_data_points],
                                            self.egg.lowBeta_ydata[start: self.egg.n_data_points])

            self.egg.n_data_points +=1 #仿照oxi_thread修改的

    def getStartTime(self, is_csv=False):
        if is_csv:
            now = self.egg.egg_xdata[self.lastEnd]
        else:
            now = self.egg.egg_xdata[len(self.egg.egg_xdata) - 1]

        if now < 10:
            return 0
        for i in range(0, len(self.egg.egg_xdata)):
            if now - 10 <= self.egg.egg_xdata[i]:
                self.lastStart = self.egg.egg_xdata[i]
                return i
        return 0
