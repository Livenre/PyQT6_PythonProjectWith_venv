import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QStyle
)
from PyQt6.QtCore import QThreadPool

from paint import Canvas, QPaletteButton, COLORS
from loader import Loader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()
        self.progress = QProgressBar()
        self.start_btn = QPushButton("Запустити завантаження")

        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(self.canvas)

        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        layout.addLayout(palette)

        layout.addWidget(self.progress)
        layout.addWidget(self.start_btn)

        self.setCentralWidget(w)

        self.threadpool = QThreadPool()
        self.start_btn.clicked.connect(self.start_loading)


    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.clicked.connect(lambda _, col=c: self.canvas.set_pen_color(col))
            layout.addWidget(b)

    def start_loading(self):
        loader = Loader()
        loader.signals.progress.connect(self.progress.setValue)
        loader.signals.finished.connect(self.loading_finished)

        self.start_btn.setEnabled(False)
        self.start_btn.setText("Виконується...")

        self.threadpool.start(loader)

    def loading_finished(self):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Запустити знову")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
