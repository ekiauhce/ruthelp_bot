from docxtpl import DocxTemplate
from io import BytesIO
from datetime import date
from typing import List
from database.db import get_director
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker



def get_genetive_case(gender, surname, name, middle_name="") -> List[str]:
    """Ставит ФИО в род. падеж, используя запрос к API morphos.io"""
    
    gender = Gender.MALE if gender == "Мужской" else Gender.FEMALE
    
    maker = PetrovichDeclinationMaker()
    surname = maker.make(NamePart.LASTNAME, gender, Case.GENITIVE, surname)
    name = maker.make(NamePart.FIRSTNAME, gender, Case.GENITIVE, name)
    middle_name = maker.make(NamePart.MIDDLENAME, gender, Case.GENITIVE, middle_name)

    return [ surname, name, middle_name ]


def generate_form(category, group_name, gender, surname,
                  name, middle_name, phone_number, inn) -> BytesIO:
    """
    Генерирует форму в формате docx. Функция возвращает
    байтовый буфер, в котором содержится форма.
    """
    if category == "студент, проживающий в общежитии":
        tpl = DocxTemplate("dorm.docx")
    else:
        tpl = DocxTemplate("common.docx")

    if middle_name == "-":
        middle_name = ""
        surname, name = get_genetive_case(gender, surname, name)
    else:
        surname, name, middle_name = get_genetive_case(gender, surname, name, middle_name)

    course = int(group_name[4]) if group_name[5] != "5" else int(group_name[4]) + int(group_name[5])
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
        "director": get_director(course)
    }
    tpl.render(context)

    # Создание буфера
    buffer = BytesIO()
    # Сохраненяем отрендеренный шаблон формы в буфер
    tpl.save(buffer)
    # Возвращаемся в начало буфера
    buffer.seek(0)
    return buffer
