import docxtpl
from datetime import date
from database import db
import io

def generate_form(category, group_name, gender, surname,
    name, middle_name, phone_number, inn) -> io.BytesIO:
    """
    Генерирует форму в формате docx. Функция возвращает
    file-like object формы.
    """
    if category == "студент, проживающий в общежитии":
        tpl = docxtpl.DocxTemplate("templates/dorm.docx")
    else:
        tpl = docxtpl.DocxTemplate("templates/common.docx")
    #TODO: фио в род. падеже
    course = group_name[4]
    context = {
        "gp": "а" if gender == "Мужской" else "ки",
        "gn": group_name,
        "surname": surname,
        "name": name,
        "middle_name": "" if middle_name == "-" else middle_name,
        "inn": inn,
        "phone_number": phone_number,
        "category": category,
        "date": date.today().strftime("%d.%m.%Y"),
        "director": db.get_director(course)
    }
    tpl.render(context)
    
    buffer = io.BytesIO()
    tpl.save(buffer)
    buffer.seek(0)
    return buffer