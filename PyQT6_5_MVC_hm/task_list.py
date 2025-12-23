from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

class TaskListModel(QAbstractListModel):
    def __init__(self, tasks=None):
        super().__init__()
        self.tasks = tasks or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.tasks)

    def data(self, index, role):
        if not index.isValid():
            return None

        is_done, text, created_at = self.tasks[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return text

        if role == Qt.ItemDataRole.FontRole and is_done:
            font = QFont()
            font.setStrikeOut(True)
            return font

        if role == Qt.ItemDataRole.BackgroundRole and not is_done:
            try:
                dt_created = datetime.strptime(created_at, "%Y-%m-%d %H:%M")
                age_days = (datetime.now() - dt_created).days
                if age_days >= 3:
                    return QColor("#fff2cc")
            except Exception:
                return None

        return None

    def add_task(self, text):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tasks.append((False, text, created_at))
        self.endInsertRows()

    def remove_task(self, row):
        if 0 <= row < len(self.tasks):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.tasks.pop(row)
            self.endRemoveRows()

    def mark_done(self, row):
        if 0 <= row < len(self.tasks):
            is_done, text, created_at = self.tasks[row]
            self.tasks[row] = (True, text, created_at)
            index = self.index(row)
            self.dataChanged.emit(index, index)
