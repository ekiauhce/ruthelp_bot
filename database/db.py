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
        return [row[0] for row in cur.fetchall()]

def create_applications():
    """Создает таблицу заявок"""
    with DBManager() as cur:
        cur.execute(queries.create_applications_table)

def insert_application(data):
    """Добавляет заявку в базу"""
    with DBManager() as cur:
        cur.execute(queries.insert_application, data)

def create_directors():
    """Создает таблицу зам. декана"""
    with DBManager() as cur:
        cur.execute(queries.create_directors_table)
        cur.execute(queries.insert_directors)

def get_director(course):
    """Возвращает инициалы зам. декана по номеру курса"""
    with DBManager() as cur:
        cur.execute(queries.select_director, course)
        return cur.fetchone()[0]

def init():
    """Создает схему бд, где нужно добавляет данные"""
    create_categories()
    create_applications()
    create_directors()

