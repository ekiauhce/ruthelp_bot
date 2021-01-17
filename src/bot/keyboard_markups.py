from telegram import ReplyKeyboardMarkup
from database import get_categories_list

# Разметки клавиатур для выбора
# категории, пола и верные/неверные данные соотвественно
categories_markup = ReplyKeyboardMarkup(
    [[c] for c in get_categories_list()],
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
