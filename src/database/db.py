from . import queries
from .manager import DBManager
from typing import List, Tuple


def create_categories() -> None:
    """Создает таблицу категорий в базе"""
    with DBManager() as cur:
        cur.execute(queries.create_categories_table)
        cur.execute(queries.insert_categories)


def get_categories_list() -> List[str]:
    """Возвращает список категорий"""
    with DBManager() as cur:
        cur.execute(queries.select_categories)
        return [row[0] for row in cur.fetchall()]


def create_applications() -> None:
    """Создает таблицу заявок"""
    with DBManager() as cur:
        cur.execute(queries.create_applications_table)


def insert_application(data) -> None:
    """Добавляет заявку в базу"""
    with DBManager() as cur:
        cur.execute(queries.insert_application, data)


def create_directors() -> None:
    """Создает таблицу зам. декана"""
    with DBManager() as cur:
        cur.execute(queries.create_directors_table)
        cur.execute(queries.insert_directors)


def get_director(course) -> str:
    """Возвращает инициалы зам. декана по номеру курса"""
    with DBManager() as cur:
        cur.execute(queries.select_director, course)
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


def create_admins() -> None:
    """Создает таблицу админов и добавляет туда автора"""
    with DBManager() as cur:
        cur.execute(queries.create_admins_table)
        cur.execute(queries.insert_author_to_admins)


def get_admins() -> List[int]:
    """Возвращает список админов"""
    with DBManager() as cur:
        cur.execute(queries.select_admins)
        return [row[0] for row in cur.fetchall()]


def insert_admin(chat_id: int) -> bool:
    """Добавляет пользователя в админы"""
    with DBManager() as cur:
        cur.execute(queries.insert_admin, (chat_id,))
        return False if cur.rowcount == 0 else True


def delete_admin(chat_id: int) -> bool:
    """Удаляет пользователя из админов"""
    with DBManager() as cur:
        cur.execute(queries.delete_admin, (chat_id, ))
        return False if cur.rowcount == 0 else True


def init() -> None:
    """Создает схему бд, где нужно добавляет данные. Функция переписывает данные в бд!!!"""
    create_categories()
    create_applications()
    create_directors()
    create_admins()
