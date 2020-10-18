from telegram import ReplyKeyboardMarkup
from database import db

#Разметки клавиатур для выбора 
#категории, пола и верные/неверные данные соотвественно
categories_markup = ReplyKeyboardMarkup(
    [[c] for c in db.get_categories_list()],
    one_time_keyboard=True
)

genders_markup = ReplyKeyboardMarkup(
    [["Мужской"], ["Женский"]],
    one_time_keyboard=True
)

check_markup = ReplyKeyboardMarkup(
    [["Все верно"], ["Заполнить заявку заново"]],
    one_time_keyboard=True
)