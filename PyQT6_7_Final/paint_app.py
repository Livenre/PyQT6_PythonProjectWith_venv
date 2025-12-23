from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPainter, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QLayout,
)


# Палитра цветов (из прошлой работы)
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
        self.setStyleSheet(
            f"background-color: {color}; border: 1px solid #222;"
        )


class Canvas(QLabel):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.setScaledContents(False)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # НАСТОЯЩИЙ ХОЛСТ (НИКОГДА НЕ УМЕНЬШАЕТСЯ)
        self.image = QPixmap(2000, 2000)
        self.image.fill(Qt.GlobalColor.white)

        self.last_position = None
        self.pen_color = QColor("#000000")
        self.drawing = False

        self.update_view()

    def update_view(self):
        """Обновляем только видимую часть"""
        view = QPixmap(self.size())
        view.fill(Qt.GlobalColor.white)

        painter = QPainter(view)
        painter.drawPixmap(0, 0, self.image)
        painter.end()

        self.setPixmap(view)

    def resizeEvent(self, event):
        self.update_view()

    def set_pen_color(self, color):
        self.pen_color = QColor(color)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_position = e.position().toPoint()

    def mouseMoveEvent(self, e):
        if not self.drawing:
            return

        pos = e.position().toPoint()

        painter = QPainter(self.image)
        pen = painter.pen()
        pen.setWidth(4)
        pen.setColor(self.pen_color)
        painter.setPen(pen)

        painter.drawLine(self.last_position, pos)
        painter.end()

        self.last_position = pos
        self.update_view()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.drawing = False
            self.last_position = None

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update_view()



class PaintApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Paint")
        self.resize(900, 550)

        self.canvas = Canvas()
        self.setWindowTitle("Mini Paint")
        self.setWindowIcon(QIcon("icons/paint.jpg"))

        # ---------- ПАЛИТРА ----------
        palette_layout = QHBoxLayout()
        palette_layout.setSpacing(4)

        for color in COLORS:
            btn = QPaletteButton(color)
            btn.clicked.connect(
                lambda _, c=color: self.canvas.set_pen_color(c)
            )
            palette_layout.addWidget(btn)

        # ---------- КНОПКА ОЧИСТКИ ----------
        clear_btn = QPushButton("Очистить")
        clear_btn.clicked.connect(self.canvas.clear)

        # ---------- ОСНОВНОЙ LAYOUT ----------
        layout = QVBoxLayout()

        # КЛЮЧЕВАЯ СТРОКА
        # отключаем автоматическое навязывание minimumSize
        layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        layout.addLayout(palette_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(clear_btn)

        self.setLayout(layout)


