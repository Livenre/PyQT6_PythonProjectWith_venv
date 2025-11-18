import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QFileDialog,
    QToolBar,
    QMessageBox, QColorDialog, QFontDialog
)
from PyQt6.QtGui import QIcon, QAction, QColor
from PyQt6.QtCore import QSize


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Text Editor")
        self.setGeometry(200, 200, 800, 600)

        # Центральне текстове поле
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Створення панелі інструментів
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Дії (Actions)
        open_action = QAction(QIcon(), "Відкрити", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction(QIcon(), "Зберегти", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        # Формати
        font_action = QAction("Шрифт", self)
        font_action.triggered.connect(self.choose_font)
        toolbar.addAction(font_action)

        # Колір
        color_action = QAction("Колір", self)
        color_action.triggered.connect(self.choose_color)
        toolbar.addAction(color_action)

        toolbar.addSeparator()

        exit_action = QAction(QIcon(), "Вихід", self)
        exit_action.triggered.connect(self.close_app)
        toolbar.addAction(exit_action)

        # Меню
        menu = self.menuBar()
        file_menu = menu.addMenu("Файл")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)


        format_menu = menu.addMenu("Формат")
        format_menu.addAction(font_action)
        format_menu.addAction(color_action)


    # Обробники подій
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Відкрити файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                self.text_edit.setText(text)
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося відкрити файл:\n{e}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Зберегти файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.text_edit.toPlainText())
            except Exception as e:
                QMessageBox.warning(self, "Помилка", f"Не вдалося зберегти файл:\n{e}")

    def choose_font(self):
        font, ok = QFontDialog.getFont(self.text_edit.font(), self)
        if ok:
            self.text_edit.setFont(font)

    def choose_color(self):
        color = QColorDialog.getColor(QColor("black"), self, "Виберіть колір тексту")
        if color.isValid():
            self.text_edit.setTextColor(color)

    def close_app(self):
        reply = QMessageBox.question(
            self, "Вихід",
            "Ви дійсно хочете вийти?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    app.exec()
