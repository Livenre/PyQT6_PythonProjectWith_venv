import sys

from layout_colorwidget import Color

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QStackedLayout, QPushButton,
)



class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App1")

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout1.setContentsMargins(20, 20, 20, 20)
        layout1.setSpacing(20)

        layout2.addWidget(Color("red"))
        layout2.addWidget(Color("green"))
        layout2.addWidget(Color("blue"))

        layout1.addLayout(layout2)

        layout1.addWidget(Color("pink"))

        layout3.addWidget(Color("orange"))
        layout3.addWidget(Color("purple"))

        layout1.addLayout(layout3)

        # ----------------------------------------------
        layout4 = QGridLayout()

        layout4.addWidget(Color("red"),0, 0)
        layout4.addWidget(Color("purple"),1, 0)
        layout4.addWidget(Color("black"),1, 1)
        layout4.addWidget(Color("yellow"),2, 1)

        layout1.addLayout(layout4)
        # ----------------------------------------------
        # layout5 = QStackedLayout()
        # layout5.addWidget(Color("yellow"))
        # layout5.addWidget(Color("blue"))
        # layout5.addWidget(Color("lightblue"))
        # layout5.addWidget(Color("grey"))
        #
        # layout5.setCurrentIndex(3)
        #
        # layout1.addLayout(layout5)
        # ----------------------------------------------
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

class MainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App2")

        layout1 = QHBoxLayout()

        layout1.setContentsMargins(20, 20, 20, 20)
        layout1.setSpacing(20)

        # ----------------------------------------------
        layout5 = QStackedLayout()
        layout5.addWidget(Color("yellow"))
        layout5.addWidget(Color("blue"))
        layout5.addWidget(Color("lightblue"))
        layout5.addWidget(Color("grey"))

        layout1.addLayout(layout5)
        # ----------------------------------------------

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

class MainWindow3(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App3")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        # ----------------------------------------------
        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        # ----------------------------------------------

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

app = QApplication(sys.argv)

window1 = MainWindow1()
window1.show() # IMPORTANT!!!!! Windows are hidden by default.

window2 = MainWindow2()
window2.show()

window3 = MainWindow3()
window3.show()

app.exec()