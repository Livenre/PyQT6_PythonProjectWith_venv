from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import QLabel, QPushButton

COLORS = [
    "#000000", "#141923", "#414168", "#3a7fa7", "#35e3e3",
    "#8fd970", "#5ebb49", "#458352", "#dcd37b", "#fffee5",
    "#ffd035", "#cc9245", "#a15c3e", "#a42f3b", "#f45b7a",
    "#c24998", "#81588d", "#bcb0c2", "#ffffff",
]


class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.setFixedSize(QSize(24, 24))
        self.setStyleSheet(f"background-color: {color}; border: 1px solid #222;")


class Canvas(QLabel):
    def __init__(self):
        super().__init__()

        self._pixmap = QPixmap(600, 300)
        self._pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self._pixmap)

        self.last_position = None
        self.pen_color = QColor("#000000")

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def mouseMoveEvent(self, e):
        pos = e.position()
        if self.last_position is None:
            self.last_position = pos
            return

        painter = QPainter(self._pixmap)
        pen = painter.pen()
        pen.setWidth(4)
        pen.setColor(self.pen_color)
        painter.setPen(pen)

        painter.drawLine(self.last_position, pos)
        painter.end()

        self.setPixmap(self._pixmap)
        self.last_position = pos

    def mouseReleaseEvent(self, e):
        self.last_position = None
