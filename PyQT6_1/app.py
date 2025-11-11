import sys

from PyQT6_0.layout_colorwidget import Color

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QStackedLayout,
    QPushButton,
    QFormLayout, QLineEdit
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6_1 Complex Layout Example")

        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(Color("light pink"))
        header_layout.addWidget(Color("yellow"))
        header_layout.addWidget(Color("black"))

        # Обртаєм Header в QWidget, щоб задать высоту
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setFixedHeight(50)
        main_layout.addWidget(header_widget)

        # Центральна частина
        center_layout = QVBoxLayout()
        main_layout.addLayout(center_layout)

        # Кнопки навігації
        buttons_layout = QHBoxLayout()
        center_layout.addLayout(buttons_layout)

        btn_grid = QPushButton("Grid page")
        btn_grid.pressed.connect(self.activate_tab_1)
        buttons_layout.addWidget(btn_grid)

        btn_form = QPushButton("Form page")
        btn_form.pressed.connect(self.activate_tab_2)
        buttons_layout.addWidget(btn_form)

        btn_mixed = QPushButton("Mixed page")
        btn_mixed.pressed.connect(self.activate_tab_3)
        buttons_layout.addWidget(btn_mixed)

        # Робоча зона зі сторінками
        self.stacklayout = QStackedLayout()
        center_layout.addLayout(self.stacklayout)

        # Grid page
        grid_page = QWidget()
        grid_layout = QGridLayout()
        grid_layout.addWidget(Color("orange"), 0, 0)
        grid_layout.addWidget(Color("red"), 0, 1)
        grid_layout.addWidget(Color("purple"), 1, 0)
        grid_layout.addWidget(Color("gray"), 1, 1)
        grid_page.setLayout(grid_layout)
        self.stacklayout.addWidget(grid_page)

        # Form page
        form_page = QWidget()
        form_layout = QFormLayout()
        form_layout.addRow("Name:", QLineEdit())
        form_layout.addRow("Email:", QLineEdit())
        form_layout.addRow("Address:", QLineEdit())
        form_page.setLayout(form_layout)
        self.stacklayout.addWidget(form_page)

        # Mixed page
        mixed_page = QWidget()
        mixed_outer = QVBoxLayout()

        top_row = QHBoxLayout()
        top_row.addWidget(Color("brown"))
        top_row.addWidget(Color("light blue"))

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(Color("light green"))
        bottom_row.addWidget(Color("light gray"))

        mixed_outer.addLayout(top_row)
        mixed_outer.addLayout(bottom_row)
        mixed_page.setLayout(mixed_outer)
        self.stacklayout.addWidget(mixed_page)

        # Завершення
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # Функції
    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

# if __name__ == "__main__":
app = QApplication(sys.argv)

window = MainWindow()
window.resize(600, 600)
window.show()

app.exec()
