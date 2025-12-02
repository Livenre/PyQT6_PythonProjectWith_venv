import sys
import json
from PyQt6.QtWidgets import QApplication, QListWidgetItem, QMessageBox, QStyle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette, QIcon
from PyQt6 import uic


class MainWindow:
    def __init__(self):
        self.window = uic.loadUi("mainwindow.ui")

        # --- Віджети ---
        self.list_widget = self.window.listWidget
        self.name_input = self.window.lineEdit_3
        self.date_input = self.window.lineEdit_2
        self.prio_input = self.window.lineEdit
        self.form_button = self.window.pushButton

        # --- Actions ---
        self.act_new = self.window.actionNew
        self.act_save = self.window.actionSave
        self.act_delete = self.window.actionDelete
        self.act_exit = self.window.actionExit
        self.act_toggle = self.window.actionToggleTheme

        # --- Сигнали ---
        self.act_new.triggered.connect(self.add_task)
        self.act_delete.triggered.connect(self.delete_task)
        self.act_save.triggered.connect(self.save_to_file)
        self.act_exit.triggered.connect(self.exit_app)
        self.form_button.clicked.connect(self.clear_form)
        self.list_widget.currentItemChanged.connect(self.load_task_into_form)
        self.act_toggle.triggered.connect(self.toggle_theme)

        # --- Іконки ---
        style = self.window.style()
        self.act_new.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        self.act_save.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.act_delete.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton))
        self.window.setWindowIcon(QIcon("icon.jpg"))

        # --- Теми ---
        self.create_palettes()
        self.load_theme()          # Тема при запуске

        # --- завантаження ---
        self.load_tasks_from_file()


    # --- Палітри ---
    def create_palettes(self):
        # dark theme
        self.darkPalette = QPalette()
        self.darkPalette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        self.darkPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        self.darkPalette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
        self.darkPalette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
        self.darkPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.darkPalette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        self.darkPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.darkPalette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        self.darkPalette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

        #light theme
        self.lightPalette = QPalette()
        self.lightPalette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        self.lightPalette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        self.lightPalette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        self.lightPalette.setColor(QPalette.ColorRole.AlternateBase, QColor("#e8e8e8"))
        self.lightPalette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        self.lightPalette.setColor(QPalette.ColorRole.Button, QColor("#e0e0e0"))
        self.lightPalette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        self.lightPalette.setColor(QPalette.ColorRole.Highlight, QColor("#0078d7"))
        self.lightPalette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

    # --- Застосування тем ---
    def apply_dark_theme(self):
        app = QApplication.instance()
        app.setPalette(self.darkPalette)

        with open("dark.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    def apply_light_theme(self):
        app = QApplication.instance()
        app.setPalette(self.lightPalette)

        with open("light.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    def toggle_theme(self):
        self.is_dark = not getattr(self, "is_dark", True)

        if self.is_dark:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

        with open("settings.json", "w") as f:
            json.dump({"dark": self.is_dark}, f)

    def load_theme(self):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                self.is_dark = data.get("dark", True)
        except FileNotFoundError:
            self.is_dark = True

        if self.is_dark:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()


    # --- Логіка ---
    def add_task(self):
        item = QListWidgetItem("Нова задача")
        item.setData(1000, {"name": "", "date": "", "prio": ""})
        self.list_widget.addItem(item)
        self.list_widget.setCurrentItem(item)

    def delete_task(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)
            self.clear_form()

    def load_task_into_form(self, current, previous):
        if current is None:
            return
        data = current.data(1000)
        self.name_input.setText(data["name"])
        self.date_input.setText(data["date"])
        self.prio_input.setText(data["prio"])

    def show_info(self, title, text):
        app = QApplication.instance()

       # Тимчасово вмикаємо стиль Fusion
        old_style = app.style().objectName()
        app.setStyle("Fusion")

        QMessageBox.information(self.window, title, text)

        # Повертаємо стиль
        app.setStyle(old_style)

    def save_to_file(self):
        tasks = []

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            data = item.data(1000)

            if item == self.list_widget.currentItem():
                data["name"] = self.name_input.text()
                data["date"] = self.date_input.text()
                data["prio"] = self.prio_input.text()
                item.setData(1000, data)
                item.setText(f"{data['name']} | {data['date']} | {data['prio']}")

            tasks.append(data)

        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

        self.show_info("Збережено", "Файл tasks.json збережено!")
        #QMessageBox.information(self.window, "Збережено", "Файл tasks.json збережено!")

    def exit_app(self):
        self.window.close()

    def clear_form(self):
        self.name_input.clear()
        self.date_input.clear()
        self.prio_input.clear()

    def load_tasks_from_file(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                tasks = json.load(f)

            for data in tasks:
                item = QListWidgetItem(f"{data['name']} | {data['date']} | {data['prio']}")
                item.setData(1000, data)
                self.list_widget.addItem(item)

        except FileNotFoundError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.window.show()
    sys.exit(app.exec())
