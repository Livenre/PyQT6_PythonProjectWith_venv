from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def init_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("tasks.sqlite")

    if not db.open():
        print("DB open error")
        return False

    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT,
            created_at TEXT,
            completed_at TEXT
        )
    """)

    return True
