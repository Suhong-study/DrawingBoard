import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Labeling(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_list = []
        self.num = 0
        self.start = QPoint()
        self.end = QPoint()
        self.pencolor = QColor(0, 0, 0)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1000, 600)
        self.setWindowTitle('레이블링프로그램-1')
        self.setStyleSheet('background-color: white;')
        self.directory_button = QPushButton("디렉터리 선택", self)
        self.directory_button.setFont(QFont("굴림", 15))
        self.directory_button.setGeometry(30, 500, 200, 70)
        self.directory_button.setStyleSheet('background-color: white; border-style: outset;'
                                            ' border-width: 5px; border-color: black;')
        self.directory_button.clicked.connect(self.open)
        self.imagesetting = QLabel(self)
        self.imagesetting.setGeometry(30, 30, 800, 450)
        self.imagesetting.setStyleSheet('background-color: white; border-style: outset; '
                                        'border-width: 5px; border-color: black;')
        self.pathsetting = QLabel(self)
        self.pathsetting.setGeometry(250, 500, 500, 70)
        self.pathsetting.setFont(QFont("굴림", 11))
        self.pathsetting.setStyleSheet('background-color: white; border-style: outset; '
                                       'border-width: 5px; border-color: black;')
        self.left_button = QPushButton("<",self)
        self.left_button.setFont(QFont("굴림", 20))
        self.left_button.setGeometry(770, 500, 90, 70)
        self.left_button.setStyleSheet('background-color: white; border-style: outset; '
                                       'border-width: 5px; border-color: black;')
        self.left_button.clicked.connect(self.preimage)
        self.right_button = QPushButton(">", self)
        self.right_button.setFont(QFont("굴림", 20))
        self.right_button.setGeometry(880, 500, 90, 70)
        self.right_button.setStyleSheet('background-color: white; border-style: outset;'
                                        'border-width: 5px; border-color: black;')
        self.right_button.clicked.connect(self.nextimage)
        self.dog_radio = QRadioButton("Dog", self)
        self.dog_radio.setGeometry(850, 20, 70, 50)
        self.dog_radio.setFont(QFont("굴림", 15))
        self.dog_radio.clicked.connect(self.boundingbox)
        self.cat_radio = QRadioButton("Cat", self)
        self.cat_radio.setGeometry(850, 60, 70, 50)
        self.cat_radio.setFont(QFont("굴림", 15))
        self.cat_radio.clicked.connect(self.boundingbox)
        self.dog_color = QLabel(self)
        self.dog_color.setGeometry(936, 32, 25, 25)
        self.dog_color.setStyleSheet('background-color: red;')
        self.cat_color = QLabel(self)
        self.cat_color.setGeometry(936, 72, 25, 25)
        self.cat_color.setStyleSheet('background-color: blue;')
        self.imagesetting.mousePressEvent = self.mousePressEvent
        self.imagesetting.mouseMoveEvent = self.mouseMoveEvent
        self.imagesetting.mouseReleaseEvent = self.mouseReleaseEvent
        self.show()

    def open(self):
        self.folder_open = QFileDialog.getExistingDirectory()
        self.folder_open = os.path.realpath(self.folder_open)
        print(self.folder_open)
        self.image_list = os.listdir(self.folder_open)
        print(self.image_list)
        self.pathsetting.setText(self.folder_open)
        self.pixmap = QPixmap(self.imagesetting.width(), self.imagesetting.height())
        self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[0]))
        self.num = 0
        self.imagesetting.setPixmap(self.pixmap)

    def preimage(self):
        self.num = self.num-1
        if self.num < 0:
            QMessageBox.about(self, "알림", "첫번째 이미지입니다.")
        else:
            self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[self.num]))
            self.imagesetting.setPixmap(self.pixmap)

    def nextimage(self):
        self.num = self.num + 1
        if not self.num <= (len(self.image_list) - 1):
            QMessageBox.about(self, "알림", "마지막 이미지입니다.")
        else:
            self.pixmap.load("{0}\{1}".format(self.folder_open, self.image_list[self.num]))
            self.imagesetting.setPixmap(self.pixmap)

    def boundingbox(self):
        sender = self.sender()
        if sender == self.cat_radio:
            self.pencolor = QColor(0, 0, 255)
        elif sender == self.dog_radio:
            self.pencolor = QColor(255, 0, 0)

    def mousePressEvent(self, e):
        self.start = e.pos()
        self.end = e.pos()
        self.imagesetting.update()

    def mouseMoveEvent(self, e):
        painter = QPainter(self.imagesetting.pixmap())
        painter.setPen(QPen(self.penColor, 5))
        painter.drawRect(QRect(self.start, e.pos()))
        painter.end()
        self.imagesetting.repaint()

    def mouseReleaseEvent(self, e):
        painter = QPainter(self.imagesetting.pixmap())
        painter.setPen(QPen(self.penColor, 5))
        painter.drawRect(QRect(self.start, e.pos()))
        self.imagesetting.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Labeling()
    sys.exit(app.exec_())