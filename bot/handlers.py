from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters
)

from bot import message_text as mt
from bot import keyboard_markups as km
from database import db

#Состояния, в которых может находится диалог
CATEGORY, GROUP_NAME, GENDER, SURNAME, NAME, \
MIDDLE_NAME, PHONE_NUMBER, INN, CHECK = range(9)

#TODO: добавить логирование

def start(update, context):
    """Отвечает на команду /start"""
    update.message.reply_text(mt.start)

def help(update, context):
    """Отвечает на команду /help"""
    #TODO: написать mt.help
    update.message.reply_text(...)

def make(update, context):
    """Отвечает на команду /make, предлагает выбрать категорию из списка"""
    update.message.reply_text(mt.category, reply_markup=km.categories_markup)    
    context.user_data["state"] = CATEGORY
    return CATEGORY

def category(update, context):
    """
    Добавляет категорию в контекст пользователя и предлагает ввести группу.
    Информация, записанная в контексте юзера будет болтаться в рантайме, а
    когда студент подтвердит правильность введенных данных, добавится в бд
    """
    context.user_data[CATEGORY] = update.message.text

    update.message.reply_text(mt.group_name)
    context.user_data["state"] = GROUP_NAME
    return GROUP_NAME

def group_name(update, context):
    """Добавляет группу в контекст пользователя и предлагает ввести пол"""
    context.user_data[GROUP_NAME] = update.message.text

    update.message.reply_text(mt.gender, reply_markup=km.genders_markup)
    context.user_data["state"] = GENDER
    return GENDER

def gender(update, context):
    """Добавляет пол в контекст пользователя и предлагает ввести фамилию"""
    context.user_data[GENDER] = update.message.text

    update.message.reply_text(mt.surname)
    context.user_data["state"] = SURNAME
    return SURNAME

def surname(update, context):
    """Добавляет фамилию в контекст пользователя и предлагает ввести имя"""
    context.user_data[SURNAME] = update.message.text

    update.message.reply_text(mt.name)
    context.user_data["state"] = NAME
    return NAME

def name(update, context):
    """Добавляет имя в контекст пользователя и предлагает ввести отчество"""
    context.user_data[NAME] = update.message.text

    update.message.reply_text(mt.middle_name)
    context.user_data["state"] = MIDDLE_NAME
    return MIDDLE_NAME

def middle_name(update, context):
    """Добавляет отчество в контекст пользователя и предлагает ввести номер телефона"""
    context.user_data[MIDDLE_NAME] = update.message.text

    update.message.reply_text(mt.phone_number)
    context.user_data["state"] = PHONE_NUMBER
    return PHONE_NUMBER

def phone_number(update, context):
    """Добавляет номер телефона в контекст пользователя и предлагает ввести ИНН"""
    context.user_data[PHONE_NUMBER] = update.message.text

    update.message.reply_text(mt.inn)
    context.user_data["state"] = INN
    return INN

def inn(update, context):
    """Добавляет ИНН в контекст пользователя и предлагает подтвердить правильность введенных данных"""
    context.user_data[INN] = update.message.text

    update.message.reply_text(
        mt.check + "{}\n{}\n{}\n{} {} {}\n{}\n{}".format(
            *[context.user_data[k] for k in range(8)]
        ), reply_markup=km.check_markup
    )
    context.user_data["state"] = CHECK
    return CHECK 

def check(update, context):
    """
    Либо выплевывает состояние CATEGORY, отправляя студента в начало диалога,
    либо записывает данные из контекста пользователя в бд и отправляет в чат
    файл заявления
    """
    from templates import generate
    if update.message.text == "Заполнить заявку заново":
        update.message.reply_text(mt.category, reply_markup=km.categories_markup)
        context.user_data["state"] = CATEGORY
        return CATEGORY

    data = [context.user_data[k] for k in range(8)]
    db.insert_application(data)
    
    form_bytes = generate.generate_form(*data)
    update.message.reply_document(
        document=form_bytes,
        filename="application.docx",
        caption="Заявка принята!"
    )
    #Закрываем буфер
    form_bytes.close()
    return ConversationHandler.END

def wrong(update, context):
    """Хендлер обрабатывает любой неверный ввод и возвращает последнее состояние диалога"""
    update.message.reply_text(mt.wrong)
    return context.user_data["state"]


#Создаем хендлеры
start_handler = CommandHandler("start", start)
make_handler = CommandHandler("make", make)
#TODO: добавить регулярки для ФИО
conv_handler = ConversationHandler(
    entry_points=[make_handler],
    states={
        CATEGORY: [MessageHandler(Filters.text(db.get_categories_list()), category)],
        GROUP_NAME: [MessageHandler(Filters.regex(r"^[/А-ЯЁ/u]{3}-[1-5]{2}[1-9]$"), group_name)],
        GENDER: [MessageHandler(Filters.text(["Мужской", "Женский"]), gender)],
        SURNAME: [MessageHandler(Filters.text, surname)],
        NAME: [MessageHandler(Filters.text, name)],
        MIDDLE_NAME: [MessageHandler(Filters.text, middle_name)],
        PHONE_NUMBER: [MessageHandler(Filters.regex(r"^[0-9]{10}$"), phone_number)],
        INN: [MessageHandler(Filters.regex(r"^[0-9]{12}$"), inn)],
        CHECK: [MessageHandler(Filters.text(["Все верно", "Заполнить заявку заново"]), check)]
    },
    fallbacks=[make_handler, MessageHandler(Filters.all, wrong)]
)
