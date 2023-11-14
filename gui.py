import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QProgressBar, QPushButton, QSizePolicy
from PyQt6.QtGui import QIcon, QPainter, QColor, QPixmap, QPen, QBrush, QLinearGradient, QImage, QPainterPath
from PyQt6.QtCore import Qt, QSize, QRect, QPointF, QRectF, QEvent, QTimer

from functools import partial

def clamp(n, l, h): 
    return max(l, min(n, h))

class Timer(QLabel):
    def __init__(self):
        super().__init__("0:00")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background: rgb(20, 20, 20);
                border-radius: 10px;
                font-size: 18px;
                font-weight: 700;
                padding: 8px;
            }
        """)

                # background: rgb(10,10,10);
                # border-radius: 10px;
                # font-size: 24px;
                # font-weight: 700;
                # padding: 10px;

class Health(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setValue(10)
#                 background: rgb(19, 70, 158);
#                 background: rgb(145, 25, 12);
        self.setStyleSheet("""
            QProgressBar {
                font-weight: 700;
                background: rgb(20, 20, 20);
                border-radius: 10px;
                text-align: center;
                margin: 4px;
                height: 30px;
            }
                           
            QProgressBar::chunk {
                background: rgb(19, 70, 158);
                border-radius: 10px;
            }
        """)
        ## save: 8, 57, 140
#                 background: rgb(180,10,10);
class TopBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.layout = QHBoxLayout()
        self.layout.addWidget(Timer())
        self.layout.addStretch()
        self.layout.addWidget(Health())
        # self.layout.addStretch()

        self.setLayout(self.layout)

        self.setFixedHeight(50)
        #                 background: rgb(30, 84, 176);
        self.setStyleSheet("""
            QWidget {
                background: rgb(30, 30, 30);
            }
        """)

class Item(QPushButton):
    def __init__(self, path, damage):
        super().__init__()
        self.path = path
        self.damage = damage

        self.setFixedSize(100,100)

        self.setIcon(QIcon(path))
        self.setIconSize(QSize(100, 100))
#                 background: rgb(30,30,30);
#                 background: rgb(8, 57, 140);
#                 background: rgb(19, 70, 158);
        self.setStyleSheet("""
            QPushButton {
                background: rgb(20, 20, 20);
                border-radius: 10px;
            }
                           
            QPushButton::hover {
                background: rgb(30, 30, 30);
                border-radius: 10px;
            }
        """)

        # print("hi")
        # self.setSizePolicy(self.sizePolicy().setRetainSizeWhenHidden(True))

# class Window(QScrollArea):
#     def __init__(self):
#         super(Window, self).__init__()
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.setAlignment(Qt.AlignTop)
#         for index in range(100):
#             layout.addWidget(QLabel('Label %02d' % index))
#         self.setWidget(widget)
#         self.setWidgetResizable(True)

class SideBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # self.setStyleSheet("background: red")
        self.parent = parent
        self.layout = QVBoxLayout()
        # self.layout.setAlignment(Qt.AlignmentFlag)
        from random import randint
        for _ in range(3):
            item = Item(f"belt{randint(2,6)}.jpeg", 100)
            self.layout.addWidget(item)

            item.clicked.connect(partial(self.item_event, item))
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        # self.layout.addWidget(Box())
        self.layout.addStretch()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20,20,20,20)
        self.setLayout(self.layout)
        # ok = Box()
        # ok.show()
        print("idiot")
        # ok.move(100,100)

        # self.setFixedHeight(140)
        self.setFixedWidth(140)
        # self.setStyleSheet("""
        #     QWidget {
        #         background: rgb(20,20,20);
        #     }
        # """)

    def item_event(self, item):
        self.parent.current_image = item.path
        print(self.parent.current_image)
        # x = QPushButton()
        item.setVisible(False)
        # print(c.icon().pixmap(c.icon().availableSizes()[0]).toImage().text("FilePath"))
        # self.parent 

# class FireButton(QPushButton):
#     def __init__(self):
#         super().__init__("FIRE")
#         self.setFixedSize(50,50)
#         self.setStyleSheet("background: red")
#         # self.move(800, 500)
#         # self.setVisible(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setFixedSize(1000, 600)

        self.setStyleSheet("""
            QMainWindow {
                background: white;
            }
        """)

        self.x = 1000
        self.y = 1000

        self.current_image = None

        self.top_bar = TopBar()
        self.side_bar = SideBar(self)
        # self.fire = FireButton()

        self.bottom_half = QWidget()
        self.bottom_half.layout = QHBoxLayout()
        self.bottom_half.layout.addWidget(self.side_bar)
        # self.bottom_half.layout.addWidget(self.fire)
        self.bottom_half.layout.addStretch()
        self.bottom_half.layout.setContentsMargins(0,0,0,0)
        self.bottom_half.setLayout(self.bottom_half.layout)
        # self.bottom_bar = BottomBar()
        # self.bottom_bar.move(100, 10)

        # central widget
        self.frame = QWidget()
        # self.frame.setStyleSheet("background: rgb(40,40,40)")
        self.frame.layout = QVBoxLayout()

        self.frame.layout.addWidget(self.top_bar)
        # self.frame.layout.addStretch()
        self.frame.layout.addWidget(self.bottom_half, 1)

        self.frame.layout.setContentsMargins(0,0,0,0)
        self.frame.layout.setSpacing(0)
        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

        # x = QTimer()
        # x.thread = self.repaint
        # x.start(100)
        # import time
        # while True:
        #     self.repaint()
        #     time.sleep(0.1)

    # def __calc_rect_from_center(x, y, w, h):
    #     retu



    def paintEvent(self, e):
        print("run")
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.PenStyle.NoPen)

        # painter.setBrush(QColor("white"))
        # painter.drawRect(0, 0, 1000, 500)

        # gradient = QLinearGradient(300, 300, 500, 500)
        # gradient.setColorAt(0, QColor(100, 20, 20))
        # gradient.setColorAt(1, QColor(70, 15, 15))

        # painter.setBrush(gradient)
        # painter.drawRoundedRect(QRectF(400, 200, 200, 200), 20, 20)

        # painter.setBrush(QColor("black"))
        # painter.drawRoundedRect(QRectF(425, 225, 150, 150), 10, 10)
        # painter.setBrush(QColor("lightgray"))
        # painter.drawEllipse(QPointF(500, 300), 40, 40)
        # painter.setBrush(QColor(140,20,20))
        # painter.drawEllipse(QPointF(490, 300), 15, 15)

        # from PIL import Image
        # from PIL.ImageQt import ImageQt
        # image2 = Image.open('belt.jpeg')
        # qimage = ImageQt(image2)

        # # x = QPixmap.fromImage("belt.jpeg")



        image = QImage("robot-3.png").scaled(450,450)
        painter.drawImage(QPointF(375, 200), image)

        offset_x = clamp(self.x, 160, 1000) / 50 - 10
        offset_y = clamp(self.y, 140, 600) / 30 - 10

        painter.setBrush(QColor("lightgray"))
        painter.drawEllipse(QPointF(550+offset_x, 310+offset_y), 20, 20)
        painter.drawEllipse(QPointF(650+offset_x, 310+offset_y), 20, 20)
        # painter.setBrush(QColor(140,20,20))
        # painter.drawEllipse(QPointF(490, 300), 15, 15)




        # painter.setBrush(QColor("black"))
        pen = QPen(QColor(100, 100, 100), 4)  # Set color to blue and thickness to 2
        painter.setBrush(Qt.GlobalColor.transparent)
        painter.setPen(pen)

        # Define the starting and ending points of the curved line
        start_point = QPointF(900, 500)
        end_point = QPointF(self.x, self.y)
        control_point = QPointF((start_point.x() + end_point.x()) / 2 + 100, (start_point.y() + end_point.y()) / 2 - 100)
        
        path = QPainterPath()
        path.moveTo(start_point)
        path.cubicTo(start_point, control_point, end_point)

        # Draw the curved line
        painter.drawPath(path)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(20,20,20))
        painter.drawRect(0, 0, 160, 600)
        # x = QPixmap("belt6.jpeg")
        # b = QBrush(x)
        painter.setBrush(QBrush(QPixmap("belt9.png")))
        painter.drawRect(0, 0, 140, 600)

        # angle = 90
        # painter.translate(1000, 450) #400, 200
        # painter.rotate(angle)
        # image = QImage("cannon-2.png").scaled(200,200)
        # painter.drawImage(QPointF(0,0), image)

        image = QImage("cannon.png").scaled(200,200)
        painter.drawImage(QPointF(900, 500), image)

        # painter.setPen(QPen(QColor("lightgray"), 10))
        # painter.drawLine(600, 600, self.x, self.y)
        
        # x = QPixmap.fromImage(qimage)
        # painter.setBrush(x)
        # x = QPixmap("belt3.jpeg")
        # b = QBrush(x)
        # painter.setBrush(b)
        # # x = QPixmap.fromImage(qimage)
        # # painter.setBrush(x)
        # painter.fillRect(0, 550, 1500, 50, b)

        # painter.setBrush(QColor(100,100,100))
        # painter.drawRect(0, 520, 1000, 80)

        # painter.setBrush(QColor(50,50,50))
        # for i in range(0, 1000, 50):
        #     print(i)
        #     # painter.setBrush(QColor(140,140,140))
        #     painter.drawRect(i, 520, 25, 80)

        # painter.setBrush(QColor(100,100,200,50))
        # painter.drawEllipse(QPointF(500, 300), 150, 150)

        # painter.setBrush(QColor("white"))
        # painter.drawEllipse(QPointF(self.x, self.y), 6, 6)
        # painter.drawPixmap(QRect(550, 110, 320, 180), QPixmap("okok.gif"))

        painter.end()

    # def mouse
    # def mouse(self, e):
    #     print(e.pos())
    #     # pass

    # def eventFilter(self, a, e):
    #     print(a.type())
    #     if e.type() == QEvent.Type.HoverMove:
    #         print("hi")
    #         # print(e.pos())

    #     return QMainWindow.eventFilter(self, a, e)

    def mouseMoveEvent(self, e):
        self.x = e.pos().x()
        self.y = e.pos().y()
        self.repaint()
        # print(e.pos().x(), e.pos().y())

    # def mouseReleaseEvent(self, e):
    #     self.x = 0
    #     self.y = 0

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key.Key_W:
    #         self.y -= 5

    #         self.repaint()

    # def hover

    # def event(self, e):
    #     print(e.type())
    #     return super().event(e)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    app.exec()

    # while True:
    #     print(window.getm