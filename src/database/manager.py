import sqlite3


class DBManager:
    """Контекстный менеджер, который открывает, закрывает соединение с бд, коммитит изменения"""
    def __init__(self):
        self.path = "database/database.sqlite"
    
    def __enter__(self) -> sqlite3.Cursor:
        """
        Метод определяет объект, который будет находиться, например, в переменной var,
        при использовании конструкции with DBManager() as var:
        """
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Определяет поведение при выходе из контекста"""
        self.conn.commit()
        self.conn.close()
