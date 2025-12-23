import sys
import csv
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QListView, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableView, QTabWidget,
    QFileDialog, QMessageBox
)

from task_list import TaskListModel
from db import init_db
from history_search import HistorySearch


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер завдань")
        self.resize(640, 480)

        self.model = TaskListModel()

        self.history_model = HistorySearch(self)
        self.history_model.setTable("history")
        self.history_model.setSort(3, Qt.SortOrder.DescendingOrder)  # сортування за completed_at
        self.history_model.select()

        # Таблиця історії
        self.history_view = QTableView()
        self.history_view.setModel(self.history_model)
        self.history_view.setSortingEnabled(True)
        self.history_view.setColumnHidden(0, True)  # приховуємо id
        self.history_view.horizontalHeader().setStretchLastSection(True)

        # Список задач
        self.list_view = QListView()
        self.list_view.setModel(self.model)

        # Поле додавання
        self.input = QLineEdit()

        self.btn_add = QPushButton("Додати")
        self.btn_remove = QPushButton("Видалити")
        self.btn_done = QPushButton("Виконано")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addWidget(self.btn_done)

        tasks_layout = QVBoxLayout()
        tasks_layout.addWidget(self.list_view)
        tasks_layout.addWidget(self.input)
        tasks_layout.addLayout(btn_layout)


        tasks_widget = QWidget()
        tasks_widget.setLayout(tasks_layout)

        # Експорт CSV
        self.history_search = QLineEdit()
        self.btn_export_csv = QPushButton("Експорт CSV")

        # Історія
        history_top = QHBoxLayout()
        history_top.addWidget(self.history_search)
        history_top.addWidget(self.btn_export_csv)

        history_layout = QVBoxLayout()
        history_layout.addLayout(history_top)
        history_layout.addWidget(self.history_view)

        history_widget = QWidget()
        history_widget.setLayout(history_layout)

        # Кнопки задачі та історії
        self.tabs = QTabWidget()
        self.tabs.addTab(tasks_widget, "Задачі")
        self.tabs.addTab(history_widget, "Історія")
        self.setCentralWidget(self.tabs)


        self.btn_add.clicked.connect(self.add_task)
        self.btn_remove.clicked.connect(self.remove_task)
        self.btn_done.clicked.connect(self.mark_done)

        self.history_search.textChanged.connect(self.apply_history_filter)
        self.btn_export_csv.clicked.connect(self.export_history_csv)


    def add_task(self):
        text = self.input.text().strip()
        if text:
            self.model.add_task(text)
            self.input.clear()

    def remove_task(self):
        index = self.list_view.currentIndex()
        if index.isValid():
            self.model.remove_task(index.row())

    def mark_done(self):
        index = self.list_view.currentIndex()
        if not index.isValid():
            return

        row = index.row()
        is_done, text, created_at = self.model.tasks[row]

        if is_done:
            return

        self.model.mark_done(row)

        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")

        query = QSqlQuery()
        query.prepare(
            "INSERT INTO history (task_text, created_at, completed_at) VALUES (?, ?, ?)"
        )
        query.addBindValue(text)
        query.addBindValue(created_at)
        query.addBindValue(completed_at)

        ok = query.exec()
        if not ok:
            QMessageBox.warning(self, "Помилка", query.lastError().text())

        self.history_model.select()

    def apply_history_filter(self, text: str):
        t = text.strip()
        if not t:
            self.history_model.setFilter("")
            self.history_model.select()
            return

        t = t.replace("'", "''")

        flt = (
            "task_text LIKE '%{t}%' OR "
            "created_at LIKE '%{t}%' OR "
            "completed_at LIKE '%{t}%'"
        ).format(t=t)

        self.history_model.setFilter(flt)
        self.history_model.select()

    def export_history_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Експорт історії у CSV",
            "history.csv",
            "CSV (*.csv)"
        )
        if not path:
            return

        query = QSqlQuery()
        query.exec("SELECT task_text, created_at, completed_at FROM history ORDER BY completed_at DESC")

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["task_text", "created_at", "completed_at"])

                while query.next():
                    task_text = query.value(0)
                    created_at = query.value(1)
                    completed_at = query.value(2)
                    writer.writerow([task_text, created_at, completed_at])

            QMessageBox.information(self, "Готово", "CSV файл збережено.")
        except Exception as e:
            QMessageBox.warning(self, "Помилка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    init_db()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
