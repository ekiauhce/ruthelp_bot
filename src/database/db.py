from . import queries
from .manager import DBManager
from typing import List, Tuple


def create_categories() -> None:
    """Создает таблицу категорий в базе"""
    with DBManager() as cur:
        cur.execute(queries.create_categories_table)


def get_categories_list() -> List[str]:
    """Возвращает список категорий"""
    with DBManager() as cur:
        cur.execute(queries.select_categories)
        return [row[0] for row in cur.fetchall()]


def get_id_by_category(category: str) -> int:
    """TODO: doc"""
    with DBManager() as cur:
        cur.execute(queries.select_category_id_by_category, ("%" + category + "%", ))
        return cur.fetchone()[0]


def create_documents() -> None:
    """TODO: doc"""
    with DBManager() as cur:
        cur.execute(queries.create_documents_table)


def get_documents_list(category_id: int) -> List[str]:
    """TODO: doc"""
    with DBManager() as cur:
        cur.execute(queries.select_documents, (category_id, ))
        return [row[0] for row in cur.fetchall()]


def insert_application(data) -> None:
    """Добавляет заявку в базу"""
    with DBManager() as cur:
        cur.execute(queries.insert_application, data)



def get_director(course: int) -> str:
    """Возвращает инициалы зам. декана по номеру курса"""
    with DBManager() as cur:
        cur.execute(queries.select_director, (course, ))
        return cur.fetchone()[0]


def get_applications() -> List[Tuple[str]]:
    """Возвращает таблицу заявок"""
    with DBManager() as cur:
        cur.execute(queries.select_applications)
        return cur.fetchall()


def get_applications_field_names() -> List[str]:
    """Возвращает названия полей таблицы applications"""
    with DBManager() as cur:
        cur.execute(queries.select_applications_field_names)
        return [n[0] for n in cur.fetchall()]


def set_application_ok(app_id: int) -> None:
    """Устанавливает значение 1 в столбце ok для заявки с индексом app_id"""
    with DBManager() as cur:
        cur.execute(queries.update_application, (app_id,))


def init_schema() -> None:
    """Иициализация схемы бд"""
    with DBManager() as cur:
        cur.execute(queries.create_categories_table)
        cur.execute(queries.create_applications_table)
        cur.execute(queries.create_directors_table)
        cur.execute(queries.create_documents_table)


def init_data() -> None:
    """Инициализация начальных данных"""
    with DBManager() as cur:
        cur.execute(queries.insert_categories)
        cur.execute(queries.insert_directors)
        cur.execute(queries.insert_documents)