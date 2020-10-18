from database import queries
from database.manager import DBManager

def create_categories():
    """Создает таблицу категорий в базе"""
    with DBManager() as cur:
        cur.execute(queries.create_categories_table)
        cur.execute(queries.insert_categories)

def get_categories_list():
    """Возвращает список категорий"""
    with DBManager() as cur:
        cur.execute(queries.select_categories)
        return [c[1] for c in cur.fetchall()]

def create_applications():
    """Создает таблицу заявок"""
    with DBManager() as cur:
        cur.execute(queries.create_applications_table)

def insert_application(data):
    """Добавляет заявку в базу"""
    with DBManager() as cur:
        cur.execute(queries.insert_application, data)

def create_db():
    """Создает схему бд, где нужно добавляет данные"""
    create_categories()
    create_applications()

#При непосредственном запуске файла
if __name__ == "__main__":
    create_db()
