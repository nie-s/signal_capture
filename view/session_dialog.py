from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem


class SessionDialog(QDialog):
    def __init__(self, w):
        super().__init__()
        self.w = w
        self.lastStart = 0

        self.setWindowTitle('Select stored data')
        self.setWindowIcon(QtGui.QIcon('../icons/pulse.svg'))

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
