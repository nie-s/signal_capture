from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QTableWidget, QTableWidgetItem, QLineEdit, \
    QLabel, QSpacerItem, QSizePolicy, QFrame, QAction, QProgressDialog, QFileDialog, QMessageBox
import pyqtgraph as pg
import time
import datetime
import sys

from cms50ew import CMS50EW
from oxi_Thread import LiveThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.oxi = CMS50EW()

        self.parameter = {
            'spo2': {
                'port': 'COM3',
                'baudrate': 115200,
            }
        }

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
            self.live_running = True
            self.liveThread = LiveThread(self.oxi, self)
            self.liveThread.start()
            time.sleep(0.2)

            self.liveRunAction.setIcon(QtGui.QIcon('icons/media-playback-stop-symbolic.svg'))
            self.liveRunAction.setEnabled(True)
            self.statusBar.showMessage('Status: Initiating live stream ...')
        else:
            self.live_running = False
            time.sleep(0.2)  # Give thread the chance to end itself

            now = datetime.datetime.now()
            string = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
            self.liveThread.oxi.write_csv(string)

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
            self.pw = PlotWidget(self)
            self.setCentralWidget(self.pw)

        self.plotStoredDataAction.setEnabled(True)

    # def on_plotStoredData(self):

    # time.sleep(1)
    # self.pw.plotStoredData()


class MainWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow

        # Use a grid layout
        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(Qt.AlignHCenter)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)

        self.spaceHolderLeft = QtWidgets.QLabel('')
        self.spaceHolderRight = QtWidgets.QLabel('')
        self.spaceHolderRight.setFixedSize(265, 35)

        self.nameTextBoxLabel = QLabel(self)
        self.nameTextBoxLabel.setText(str('姓名:'))
        self.nameTextBoxLabel.setFixedSize(50, 35)

        self.nameTextBox = QLineEdit(self)
        self.nameTextBox.setFixedSize(180, 35)

        self.ageTextBoxLabel = QLabel(self)
        self.ageTextBoxLabel.setText(str('年龄:'))
        self.ageTextBoxLabel.setFixedSize(50, 35)

        self.ageTextBox = QLineEdit(self)
        self.ageTextBox.setFixedSize(180, 35)

        self.sexTextBoxLabel = QLabel(self)
        self.sexTextBoxLabel.setText(str('性别:'))
        self.sexTextBoxLabel.setFixedSize(50, 35)

        self.sexTextBox = QLineEdit(self)
        self.sexTextBox.setFixedSize(180, 35)

        self.idTextBoxLabel = QLabel(self)
        self.idTextBoxLabel.setText(str('编号:'))
        self.idTextBoxLabel.setFixedSize(50, 35)

        self.idTextBox = QLineEdit(self)
        self.idTextBox.setFixedSize(180, 35)

        self.warningLabel = QLabel(self)
        self.warningLabel.setStyleSheet('color:red')
        self.warningLabel.setFixedSize(180, 35)

        self.confirmButton = QtWidgets.QPushButton(self)
        self.confirmButton.setText('确定')
        self.confirmButton.setGeometry(350, 410, 100, 40)
        self.confirmButton.clicked.connect(self.confirm)

        self.layout.addWidget(self.spaceHolderLeft, 0, 0)
        self.layout.addWidget(self.spaceHolderRight, 0, 3)

        self.layout.addWidget(self.nameTextBoxLabel, 0, 1)
        self.layout.addWidget(self.nameTextBox, 0, 2)

        self.layout.addWidget(self.ageTextBoxLabel, 1, 1)
        self.layout.addWidget(self.ageTextBox, 1, 2)

        self.layout.addWidget(self.sexTextBoxLabel, 2, 1)
        self.layout.addWidget(self.sexTextBox, 2, 2)

        self.layout.addWidget(self.idTextBoxLabel, 3, 1)
        self.layout.addWidget(self.idTextBox, 3, 2)

        self.layout.addWidget(self.warningLabel, 4, 2)

    def confirm(self):
        self.subjectName = self.nameTextBox.text()
        self.subjectAge = self.ageTextBox.text()
        self.subjectSex = self.sexTextBox.text()
        self.subjectId = self.idTextBox.text()

        if self.subjectName == "" or self.subjectId == "" or self.subjectSex == "" or self.subjectAge == "":
            self.warningLabel.setText("请输入完整信息！")
            return

        self.w.information = {
            'subjectName': self.subjectName,
            'subjectAge': self.subjectAge,
            'subjectSex': self.subjectSex,
            'subjectId': self.subjectId,
        }

        self.w.pw = PlotWidget(self.w)
        self.w.setCentralWidget(self.w.pw)
        self.w.pw.checkDevice()


class PlotWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow

        # Use a grid layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        # self.checkDevicesButton = QtWidgets.QPushButton(self)
        # self.checkDevicesButton.setText('检查设备状态')
        # self.checkDevicesButton.setFixedSize(120, 35)
        # self.checkDevicesButton.clicked.connect(self.checkDevice)

        self.checkDeviceText = QtWidgets.QLabel(self)

        pulse_plot = pg.PlotWidget(background='w', )
        pulse_plot.setLabel('left', text='Pulse rate [bpm]')
        pulse_plot.setLabel('bottom', text='Time [s]')

        self.pulse_curve = pulse_plot.plot(pen=pg.mkPen('r', width=2))

        spo2_plot = pg.PlotWidget(background='w')
        spo2_plot.setLabel('left', text='Spo2 [%]')
        spo2_plot.setLabel('bottom', text='Time [s]')

        self.spo2_curve = spo2_plot.plot(pen=pg.mkPen('r', width=2))

        # self.layout.addWidget(self.checkDevicesButton, 0, 0, 1, 1)
        self.layout.addWidget(self.checkDeviceText, 0, 0)
        self.layout.addWidget(pulse_plot, 1, 0, 2, 2)
        self.layout.addWidget(spo2_plot, 3, 0, 2, 2)

        self.w.statusBar = self.w.statusBar()
        self.w.statusBar.showMessage('状态：未开启')
        self.w.resize(1000, 750)

    def checkDevice(self):
        if self.w.oxi.setup_device(self.w.parameter['spo2']['port'], self.w.parameter['spo2']['baudrate']):
            self.checkDeviceText.setText("血氧仪正常")
            self.w.liveRunAction.setEnabled(True)
        else:
            self.checkDeviceText.setText("设备连接异常")


class DeviceDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        self.w = mainWindow
        self.setWindowIcon(QtGui.QIcon('icons/pulse.svg'))
        self.setWindowTitle(str('设备参数设置'))

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

        self.eyeLabel = QLabel(self)
        self.eyeLabel.setText(str(' 眼动仪参数'))
        self.eyeLabel.setStyleSheet('font-weight:bold;margin-top:10px;')

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
        self.layout.addWidget(self.eyeLabel, 4, 0)

        self.setLayout(self.layout)
        self.adjustSize()
        self.resize(500, 680)

    def confirm(self):
        if self.spo2PortTextBox.text() == "" or self.spo2BaudTextBox.text() == "":
            self.warningText.setText("参数不得为空！")
            return

        self.w.parameter = {
            'spo2': {
                'port': self.spo2PortTextBox.text(),
                'baudrate': int(self.spo2BaudTextBox.text()),
            }
        }

        self.close()


class SessionDialog(QDialog):
    def __init__(self, w):
        super().__init__()
        self.w = w
        self.lastStart = 0

        self.setWindowTitle('Select stored data')
        self.setWindowIcon(QtGui.QIcon('icons/pulse.svg'))

        self.sessionTable = QTableWidget()
        # Make the table uneditable
        self.sessionTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.sessionTable.setRowCount(4)
        self.sessionTable.setColumnCount(1)
        self.sessionTable.setHorizontalHeaderLabels(['数据信息'])
        self.sessionTable.setVerticalHeaderLabels(
            ['数据存储', '用户', '时长', '数据点:'])
        self.sessionTable.horizontalHeader().setStretchLastSection(True)

        self.sessionTable.setItem(0, 0, QTableWidgetItem(w.oxi.sess_available))
        self.sessionTable.setItem(1, 0, QTableWidgetItem('n/a from CSV file'))
        self.sessionTable.setItem(2, 0, QTableWidgetItem(str(w.oxi.sess_duration)))
        self.sessionTable.setItem(3, 0, QTableWidgetItem(str(len(w.oxi.stored_data))))

        self.plotButton = QtWidgets.QPushButton(self)
        self.plotButton.setText('绘图')
        self.plotButton.clicked.connect(self.on_plotData)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.sessionTable)
        self.verticalLayout.addWidget(self.plotButton)
        self.resize(600, 500)

    def on_plotData(self):
        # Reset plot data and rendered plot
        self.close()
        self.w.openPlotWidget()
        # self.w.on_plotStoredData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()

    app.exec_()
