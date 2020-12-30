import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DrawingBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = QLabel(self)
        self.canvas.setGeometry(30, 100, 1220, 590)
        self.penColor = QColor(0, 0, 0)
        self.brushColor = QColor(255, 255, 255)
        self.start = QPoint()
        self.end = QPoint()
        self.erasercolor = QColor(255, 255, 255)
        self.pastx = None
        self.pasty = None
        self.shape = 0
        self.initUI()

    def initUI(self):
        self.setFixedSize(1280, 720)
        self.setWindowTitle('그림판')
        pixmap = QPixmap(self.canvas.width(), self.canvas.height())
        pixmap.fill(Qt.white)
        self.canvas.setPixmap(pixmap)

        # 펜색, 브러쉬색, 배경색, 두께 바꾸기, 지우개, 초기화
        self.pen_color = QLabel("펜", self)
        self.pen_color.setGeometry(35, 45, 100, 40)
        self.pen_button = QPushButton(self)
        self.pen_button.setGeometry(55, 45, 70, 40)
        self.pen_button.setStyleSheet('background-color: rgb(0,0,0)')
        self.pen_button.clicked.connect(self.changecolor)
        self.brush_color = QLabel("브러쉬", self)
        self.brush_color.setGeometry(170, 45, 100, 40)
        self.brush_button = QPushButton(self)
        self.brush_button.setGeometry(220, 45, 70, 40)
        self.brush_button.setStyleSheet('background-color: rgb(255,255,255)')
        self.brush_button.clicked.connect(self.changecolor)
        self.pen_thick = QLabel("두께", self)
        self.pen_thick.setGeometry(335, 45, 100, 40)
        self.thick_change = QComboBox(self)
        self.thick_change.setGeometry(370, 45, 70, 40)
        for i in range(1, 31):
            self.thick_change.addItem(str(i))
        self.eraser_button = QPushButton("지우개", self)
        self.eraser_button.setGeometry(500, 45, 70, 40)
        self.eraser_button.clicked.connect(self.eraser)
        self.bkk_color = QLabel("배경색", self)
        self.bkk_color.setGeometry(620, 45, 100, 40)
        self.bkk_button = QPushButton(self)
        self.bkk_button.setGeometry(670, 45, 70, 40)
        self.bkk_button.setStyleSheet('background-color: rgb(255,255,255)')
        self.bkk_button.clicked.connect(self.changecolor)
        self.reset_button = QPushButton("초기화", self)
        self.reset_button.setGeometry(800, 45, 70, 40)
        self.reset_button.clicked.connect(self.reset)

        # 메뉴바 만들기
        menu = self.menuBar()
        menu_file = menu.addMenu("&파일")
        save_file = QAction('저장', self)
        save_file.setShortcut('Ctrl+S')
        save_file.triggered.connect(self.save)
        menu_file.addAction(save_file)
        open_file = QAction('불러오기', self)
        open_file.setShortcut('Ctrl+A')
        menu_file.addAction(open_file)
        open_file.triggered.connect(self.open)
        close_file = QAction('&나가기', self)
        close_file.setShortcut('Ctrl+Q')
        menu_file.addAction(close_file)
        close_file.triggered.connect(self.close)

        menu_shape = menu.addMenu("&도형")
        pen_shape = QAction('펜', self)
        pen_shape.triggered.connect(lambda: self.shape_change(pen_shape))
        menu_shape.addAction(pen_shape)
        line_shape = QAction('선', self)
        line_shape.triggered.connect(lambda: self.shape_change(line_shape))
        menu_shape.addAction(line_shape)
        triangle_shape = QAction('세모', self)
        triangle_shape.triggered.connect(lambda: self.shape_change(triangle_shape))
        menu_shape.addAction(triangle_shape)
        square_shape = QAction('사각형', self)
        square_shape.triggered.connect(lambda: self.shape_change(square_shape))
        menu_shape.addAction(square_shape)
        circle_shape = QAction('원', self)
        circle_shape.triggered.connect(lambda: self.shape_change(circle_shape))
        menu_shape.addAction(circle_shape)

        self.canvas.mousePressEvent = self.mousePressEvent
        self.canvas.mouseMoveEvent = self.mouseMoveEvent
        self.canvas.mouseReleaseEvent = self.mouseReleaseEvent
        self.show()

    def reset(self):
        pixmap = QPixmap(self.canvas.width(), self.canvas.height())
        self.penColor = QColor(0, 0, 0)
        self.pen_button.setStyleSheet('background-color: rgb(0,0,0)')
        self.brushColor = QColor(255, 255, 255)
        self.brush_button.setStyleSheet('background-color: rgb(255,255,255)')
        pixmap.fill(Qt.white)
        self.erasercolor = QColor(255, 255, 255)
        self.bkk_button.setStyleSheet('background-color: rgb(255,255,255)')
        self.thick_change.setCurrentIndex(0)
        self.canvas.setPixmap(pixmap)

    def eraser(self):
        self.penColor = self.erasercolor
        self.shape = 0

    def changecolor(self):
        pixmap = QPixmap(self.canvas.width(), self.canvas.height())
        color = QColorDialog.getColor()
        sender = self.sender()
        if sender == self.pen_button and color.isValid():
            self.penColor = color
            self.pen_button.setStyleSheet('background-color: {}'.format(color.name()))
        elif sender == self.brush_button and color.isValid():
            self.brushColor = color
            self.brush_button.setStyleSheet('background-color: {}'.format(color.name()))
        elif sender == self.bkk_button and color.isValid():
            pixmap.fill(color)
            self.erasercolor = color
            self.bkk_button.setStyleSheet('background-color: {}'.format(color.name()))
            self.canvas.setPixmap(pixmap)

    def shape_change(self, shape):
        if shape.text() == '펜':
            self.shape = 0
        elif shape.text() == '선':
            self.shape = 1
        elif shape.text() == '세모':
            self.shape = 2
        elif shape.text() == '사각형':
            self.shape = 3
        elif shape.text() == '원':
            self.shape = 4

    def mousePressEvent(self, e):
        self.start = e.pos()
        self.end = e.pos()
        self.canvas.update()

    def mouseMoveEvent(self, e):
        if self.pastx is None:
            self.pastx = e.x()
            self.pasty = e.y()
        else:
            painter = QPainter(self.canvas.pixmap())
            painter.setPen(QPen(self.penColor, self.thick_change.currentIndex()))

            if self.shape == 0:
                painter.drawLine(self.pastx, self.pasty, e.x(), e.y())
                self.pastx = e.x()
                self.pasty = e.y()
            elif self.shape == 1:
                painter.drawLine(QLine(self.start, e.pos()))
            elif self.shape == 2:
                painter.setBrush(QColor(self.brushColor))
                points = QPolygon([
                    QPoint(self.pastx,self.pasty),
                    QPoint(e.x(), e.y()),
                    QPoint(self.pastx * 2, self.pasty * 2)])
                painter.drawPolygon(points)
            elif self.shape == 3:
                painter.setBrush(QColor(self.brushColor))
                painter.drawRect(QRect(self.start, e.pos()))
            elif self.shape == 4:
                painter.setBrush(QColor(self.brushColor))
                painter.drawEllipse(QRect(self.start, e.pos()))
            painter.end()
            self.canvas.repaint()

    def mouseReleaseEvent(self, e):
        painter = QPainter(self.canvas.pixmap())
        painter.setPen(QPen(self.penColor, self.thick_change.currentIndex()))
        if self.shape == 1:
            painter.drawLine(QLine(self.start, e.pos()))
        elif self.shape == 2:
            painter.setBrush(QColor(self.brushColor))
            points = QPolygon([
                QPoint(self.pastx, self.pasty),
                QPoint(e.x(), e.y()),
                QPoint(self.pastx * 2, self.pasty * 2)])
            painter.drawPolygon(points)
        elif self.shape == 3:
            painter.setBrush(QColor(self.brushColor))
            painter.drawRect(QRect(self.start, e.pos()))
        elif self.shape == 4:
            painter.setBrush(QColor(self.brushColor))
            painter.drawEllipse(QRect(self.start, e.pos()))
        painter.end()
        self.pastx = None
        self.pasty = None
        self.canvas.repaint()

    def save(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                               "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        pixmap = self.canvas.pixmap()
        pixmap.save(fpath)

    def open(self):
        fileopen = QFileDialog.getOpenFileName(self, 'Open file', '',
                                               "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        pixmap = QPixmap(self.canvas.width(), self.canvas.height())
        pixmap.load(fileopen[0])
        self.canvas.setPixmap(pixmap)

    def close(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DrawingBoard()
    sys.exit(app.exec_())
