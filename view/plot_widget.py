import cv2
import pyqtgraph as pg
from PyQt5 import uic
from PyQt5.QtChart import QBarSet, QBarSeries, QChart, QBarCategoryAxis, QValueAxis
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from view.video_widget import ViewController


class PlotWidget(QWidget): # 显示各种结果曲线、拍摄视频的页面
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow
        self.ui = uic.loadUi('./view/plot_widget.ui', self)

        # 左,1，心率
        self.ui.pulse_plot.setLabel('left', text='Pulse rate [bpm]')
        self.ui.pulse_plot.setLabel('bottom', text='Time [s]')
        self.pulse_curve = self.ui.pulse_plot.plot(pen=pg.mkPen('r', width=2))

        # 左2，spo2，血氧
        self.ui.spo2_plot.setLabel('left', text='Spo2 [%]')
        self.ui.spo2_plot.setLabel('bottom', text='Time [s]')
        self.spo2_curve = self.ui.spo2_plot.plot(pen=pg.mkPen('r', width=2))

        # 左3，脑电
        self.attention_curve = self.ui.egg_plot.plot(pen=pg.mkPen('r', width=2))
        self.meditation_curve = self.ui.egg_plot.plot(pen=pg.mkPen('g', width=2))
        self.rawValue_curve = self.ui.egg_plot.plot(pen=pg.mkPen('b', width=2))
        self.delta_curve = self.ui.egg_plot.plot(pen=pg.mkPen('c', width=2))
        self.lowAlpha_curve = self.ui.egg_plot.plot(pen=pg.mkPen('m', width=2))
        self.highAlpha_curve = self.ui.egg_plot.plot(pen=pg.mkPen('y', width=2))
        self.lowBeta_curve = self.ui.egg_plot.plot(pen=pg.mkPen('k', width=2))


        self.ui.bar_chart.setChart(self.createBarChart())
        # 拍摄视频显示栏
        self.create_video_player()
        # 开启观看视频任务按钮
        self.ui.video_button.clicked.connect(self.openVideoWindow)

        self.w.statusBar = self.w.statusBar()
        self.w.statusBar.showMessage('状态：未开启')
        self.w.resize(1500, 800)
        screen = QDesktopWidget().screenGeometry()
        size = self.w.geometry()
        self.w.move((screen.width() - size.width()) / 2,
                    (screen.height() - size.height()) / 2)

    def createBarChart(self): # 创建情绪栅模块

        self.barSet = QBarSet('data')
        self.barSet.append([0, 0, 0, 0, 0, 0, 0])
        self.barSeries = QBarSeries()
        self.barSeries.append(self.barSet)

        chart = QChart()
        chart.addSeries(self.barSeries)

        # 设置横向坐标(X轴)
        categories = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        self.barSeries.attachAxis(axisX)

        # 设置纵向坐标(Y轴)
        axisY = QValueAxis()
        axisY.setRange(0, 1)
        chart.addAxis(axisY, Qt.AlignLeft)
        self.barSeries.attachAxis(axisY)

        chart.legend().setVisible(False)
        return chart

    def checkDevice(self): # 检查血氧设备是否正常
        if self.w.oxi.setup_device(self.w.parameter['spo2']['port'], self.w.parameter['spo2']['baudrate']):
            # self.ui.checkDeviceText.setText("血氧仪正常")
            # self.w.liveRunAction.setEnabled(True) # 可以点击按钮进行实时监测
            if self.w.egg.setup_device(self.w.parameter['egg']['port'], self.w.parameter['egg']['baudrate']):
                self.ui.checkDeviceText.setText("血氧仪正常 脑电仪正常")
                self.w.liveRunAction.setEnabled(True)  # 可以点击按钮进行实时监测
            else:
                self.ui.checkDeviceText.setText("血氧仪正常 脑电仪异常")

        else:
            if self.w.egg.setup_device(self.w.parameter['egg']['port'], self.w.parameter['egg']['baudrate']):
                self.ui.checkDeviceText.setText("血氧仪异常 脑电仪正常")
                self.w.liveRunAction.setEnabled(True)  # 可以点击按钮进行实时监测
            else:
                self.ui.checkDeviceText.setText("血氧仪异常 脑电仪异常")

        self.w.liveRunAction.setEnabled(True)

    def create_video_player(self):
        # frame = cv2.imread("../icons/placeholder.png")
        frame = cv2.imread("view/placeholder.png")
        frame, _ = pg.makeARGB(frame, None, None, None, False)
        self.img = pg.ImageItem(frame, axisOrder='row-major')
        self.img.show()
        self.ui.vb.addItem(self.img)

    def openVideoWindow(self):
        self.view = ViewController(self.w)
        self.view.loadLoginView()
