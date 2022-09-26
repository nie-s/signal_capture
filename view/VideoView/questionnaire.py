from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsPixmapItem, QDialog
from PyQt5.QtGui import QImage, QPixmap
import matplotlib.pyplot as plt
from view.VideoView.questionUI import Ui_dialog


class picturezoom(QDialog, Ui_dialog):
    '''
    Ui_Form里的QGraphicsView是这样的：
    self.segpicView = QtWidgets.QGraphicsView(Form)
    self.segpicView.setGeometry(QtCore.QRect(40, 120, 351, 341))
    self.segpicView.setObjectName("segpicView")
    '''


def __init__(self, parent=None):
    """
    Constructor
    @param parent reference to the parent widget
    @type QWidget
    """
    super(picturezoom, self).__init__(parent)
    self.setupUi(self)
    self.ui = uic.loadUi("./questionUI.ui")
    img = plt.imread("./icons.问卷_唤醒度.png")  # 读取图像

    x = img.shape[1]  # 获取图像大小
    y = img.shape[0]

    frame = QImage(img, y, x, x * 3, QImage.Format_RGB888)
    # 此处x*3最好加上，否则图片会出现倾斜
    pix = QPixmap.fromImage(frame)
    item = QGraphicsPixmapItem(pix)  # 创建像素图元

    scene = QGraphicsScene()  # 创建场景
    scene.addItem(item)
    self.graphicsView.setScene(scene)  # 将场景添加至视图


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    piczoom = picturezoom()
    piczoom.show()
    app.exec_()
