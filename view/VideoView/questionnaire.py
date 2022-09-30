import csv
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QDialog, QButtonGroup
from view.VideoView.questionUI import Ui_questionnaire
import datetime
import time


class Questionnaire(QDialog, Ui_questionnaire):
    submitSignal = pyqtSignal()

    def __init__(self, w, serial, parent=None):
        super(Questionnaire, self).__init__(parent)
        self.setupUi(self)
        self.w = w
        self.serial = serial  # 记录第几次调用该页面，对应第几个视频
        self.btnGroup1 = QButtonGroup()
        for i in range(1, 10):
            btn_name = 'radioButton_1_' + str(i)
            self.btnGroup1.addButton(eval("self." + btn_name))

        self.btnGroup2 = QButtonGroup()
        for i in range(1, 10):
            btn_name = 'radioButton_2_' + str(i)
            self.btnGroup2.addButton(eval("self." + btn_name))

        self.btnGroup3 = QButtonGroup()
        for i in range(1, 4):
            btn_name = 'radioButton_3_' + str(i)
            self.btnGroup3.addButton(eval("self." + btn_name))

        self.submitButton.clicked.connect(self.submit)

    def submit(self):
        answer1 = self.btnGroup1.checkedButton().text()
        answer2 = self.btnGroup2.checkedButton().text()
        answer3 = self.btnGroup3.checkedButton().text()

        now = datetime.datetime.now()
        nowtimestamp = time.time()
        nowtime = str(now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        print("start record content of questionnaire")
        filename = self.w.folder + '/questionnaire.csv'
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                datawriter = csv.writer(f, delimiter=',')
                datawriter.writerow(['视频序号', 'nowtime', 'nowtimestamp', '效度评分', '唤醒度评分', '是否看过该视频'])

        with open(filename, 'a', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow([self.serial, nowtime, nowtimestamp, answer1, answer2, answer3])

        self.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ques = Questionnaire()
    ques.show()
    app.exec_()
