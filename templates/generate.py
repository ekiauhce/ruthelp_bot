import docxtpl
import io
from datetime import date
from typing import List
from database import db


def get_genenitve_case(gender, surname, name, middle_name="") -> List[str]:
    """Ставит ФИО в род. падеж, используя запрос к API morphos.io"""
    import requests
    params = {
        "name": f"{surname} {name} {middle_name}",
        "gender": "m" if gender == "Мужской" else "f",
        "format": "json"
    }
    resp = requests.get(
        "http://morphos.io/api/inflect-name",
        params=params
    )
    return resp.json()["cases"][1].split(" ")

def generate_form(category, group_name, gender, surname,
    name, middle_name, phone_number, inn) -> io.BytesIO:
    """
    Генерирует форму в формате docx. Функция возвращает
    байтовый буфер, в котором содержится форма.
    """
    if category == "студент, проживающий в общежитии":
        tpl = docxtpl.DocxTemplate("templates/dorm.docx")
    else:
        tpl = docxtpl.DocxTemplate("templates/common.docx")

    if middle_name == "-":
        middle_name = ""
        surname, name = get_genenitve_case(gender, surname, name)
    else:
        surname, name, middle_name = get_genenitve_case(
            gender, surname, name, middle_name
        )
    
    course = group_name[4]
    context = {
        "gp": "а" if gender == "Мужской" else "ки",
        "gn": group_name,
        "surname": surname,
        "name": name,
        "middle_name": middle_name,
        "inn": inn,
        "phone_number": phone_number,
        "category": category,
        "date": date.today().strftime("%d.%m.%Y"),
        "director": db.get_director(course)
    }
    tpl.render(context)

    #Создание буфера
    buffer = io.BytesIO()
    #Сохраненяем отрендеренный шаблон формы в буфер
    tpl.save(buffer)
    #Возвращаемся в начало буфера
    buffer.seek(0)
    return buffer
