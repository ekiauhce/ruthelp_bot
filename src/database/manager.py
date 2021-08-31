import psycopg2
import os


class DBManager:
    """Контекстный менеджер, который открывает, закрывает соединение с бд, коммитит изменения"""
    def __init__(self):
        self.path = os.environ.get("DATABASE_URL")
    
    def __enter__(self):
        """
        Метод определяет объект, который будет находиться, например, в переменной var,
        при использовании конструкции with DBManager() as var:
        """
        self.conn = psycopg2.connect(self.path, sslmode="prefer")
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        """Определяет поведение при выходе из контекста"""
        self.conn.commit()
        self.conn.close()
