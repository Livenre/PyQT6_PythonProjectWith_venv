from PyQt6.QtWidgets import QWidget, QToolButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QEvent
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QMenu
from PyQt6.QtGui import QColor


class DesktopIcon(QWidget):
    activated = pyqtSignal()

    def __init__(self, icon_path: str, text: str, parent=None):
        super().__init__(parent)

        self.setFixedSize(90, 90)

        self.button = QToolButton(self)
        self.button.setIcon(QIcon(icon_path))
        self.button.setIconSize(QSize(64, 64))
        self.button.setFixedSize(64, 64)
        self.button.setStyleSheet("""
        QToolButton {
            background-color: transparent;
            border: none;
            padding: 6px;
        }
        QToolButton:hover {
            background-color: rgba(255, 255, 255, 80);
            border-radius: 3px;
        }
        """)

        self.button.installEventFilter(self)

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label)

        black_down = QGraphicsDropShadowEffect(self)
        black_down.setBlurRadius(2)
        black_down.setOffset(1, 1)
        black_down.setColor(QColor(0, 0, 0, 222))

        self.label.setGraphicsEffect(black_down)

        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setWordWrap(True)

        self._dragging = False
        self._drag_offset = None

    def eventFilter(self, obj, event):
        if obj is self.button:
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._dragging = True
                    self._drag_offset = event.position().toPoint()
                    return True

            if event.type() == QEvent.Type.MouseMove:
                if self._dragging:
                    # new_pos = self.mapToParent(
                    #     event.position().toPoint() - self._drag_offset
                    # )
                    # self.move(new_pos)
                    parent = self.parentWidget()

                    new_pos = self.mapToParent(
                        event.position().toPoint() - self._drag_offset
                    )

                    # границы
                    max_x = parent.width() - self.width()
                    max_y = parent.height() - self.height()

                    new_x = max(0, min(new_pos.x(), max_x))
                    new_y = max(0, min(new_pos.y(), max_y))

                    self.move(new_x, new_y)

                    return True

            if event.type() == QEvent.Type.MouseButtonRelease:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._dragging = False
                    self._drag_offset = None
                    return True

            if event.type() == QEvent.Type.MouseButtonDblClick:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.activated.emit()
                    return True

        return super().eventFilter(obj, event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        open_action = menu.addAction("Открыть")
        # rename_action = menu.addAction("Переименовать")
        delete_action = menu.addAction("Удалить")

        action = menu.exec(event.globalPos())

        if action == open_action:
            self.activated.emit()

        # elif action == rename_action:
        #     print("Переименовать (заглушка)")

        elif action == delete_action:
            self.deleteLater()

