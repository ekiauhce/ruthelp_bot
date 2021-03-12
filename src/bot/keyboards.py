from telegram import ReplyKeyboardMarkup
from database import get_categories_list

# Разметки клавиатур для выбора
# категории, пола и верные/неверные данные соотвественно
categories = ReplyKeyboardMarkup(
    [[c] for c in get_categories_list()],
    one_time_keyboard=True
)

genders = ReplyKeyboardMarkup(
    [["Мужской"], ["Женский"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

check = ReplyKeyboardMarkup(
    [["Все верно"], ["Заполнить заявку заново"]],
    resize_keyboard=True,
    one_time_keyboard=True
)
