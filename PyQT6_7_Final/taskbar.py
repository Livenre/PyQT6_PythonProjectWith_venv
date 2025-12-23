from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QToolButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor


class TaskbarItem(QToolButton):
    def __init__(self, icon_path: str, window, parent=None):
        super().__init__(parent)
        self.window = window

        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(24, 24))
        self.setFixedSize(36, 36)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        self.setStyleSheet("""
        QToolButton {
            background-color: rgba(255,255,255,90);
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,40);
        }
        QToolButton:hover {
            background-color: rgba(255,255,255,150);
        }
        QToolButton:checked {
            background-color: rgba(0,120,215,160);
            border: 1px solid rgba(0,80,160,200);
        }
        """)

        self.clicked.connect(self.toggle_window)

    def toggle_window(self):
        if self.window is None:
            return

        # никаких try/except — если window умер, мы должны были обнулить ссылку
        if self.window.isVisible():
            self.window.hide()
        else:
            self.window.show()
            self.window.raise_()
            self.window.activateWindow()


class TaskBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ключ: id(window), значение: (item, window)
        self.items = {}

        self.setFixedHeight(44)

        self.setObjectName("taskbar")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
        QWidget#taskbar {
            background-color: rgba(245,245,245,190);
            border-top: 1px solid rgba(255,255,255,120);
        }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, -3)
        shadow.setColor(QColor(0, 0, 0, 140))
        self.setGraphicsEffect(shadow)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 4, 8, 4)
        self.layout.setSpacing(6)

        self.btn_start = QPushButton()
        self.btn_start.setFixedSize(75, 27)
        self.btn_start.setIcon(QIcon("icons/start.png"))
        self.btn_start.setIconSize(QSize(75, 27))
        self.btn_start.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            padding: 0px;
        }
        QPushButton:hover {
            background-color: rgba(0, 0, 0, 40);
            
        }
        QPushButton:pressed {
            background-color: rgba(0, 0, 0, 80);
        }
        """)

        self.layout.addWidget(self.btn_start)
        self.layout.addStretch()

    def add_app(self, window, icon_path: str):
        wid = id(window)

        if wid in self.items:
            return

        item = TaskbarItem(icon_path, window, self)

        # ВАЖНО: никакого insertWidget — просто вставляем перед stretch
        self.layout.insertWidget(self.layout.count() - 1, item)

        self.items[wid] = (item, window)

        # ВАЖНО: удаляем по destroyed, но работаем только с wid (int), без window
        window.destroyed.connect(lambda _=None, w=wid: self.remove_app_by_id(w))

    def remove_app_by_id(self, wid: int):
        pair = self.items.pop(wid, None)
        if not pair:
            return

        item, _window = pair
        item.window = None
        item.deleteLater()
