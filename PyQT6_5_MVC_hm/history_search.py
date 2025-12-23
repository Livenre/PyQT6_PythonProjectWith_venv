from PyQt6.QtSql import QSqlTableModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from datetime import datetime


class HistorySearch(QSqlTableModel):
    def data(self, index, role):
        value = super().data(index, role)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() == 1:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            if index.column() in (2, 3):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 3:
            completed_at = super().data(index, Qt.ItemDataRole.DisplayRole)
            if completed_at:
                today = datetime.now().strftime("%Y-%m-%d")
                if completed_at.startswith(today):
                    return QColor("light green")

        return value
