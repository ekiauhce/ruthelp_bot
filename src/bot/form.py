from __future__ import annotations

import logging
from enum import Enum
from typing import List

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

import database
from . import keyboards
from . import messages

from templates import generate_form

logger = logging.getLogger(__name__)


# Состояния, в которых может находится диалог
class State(Enum):
    CATEGORY = 1
    GROUP_NAME = 2
    GENDER = 3
    SURNAME = 4
    NAME = 5
    MIDDLE_NAME = 6
    PHONE_NUMBER = 7
    INN = 8
    CHECK = 9

    @classmethod
    def get_form_field_states(cls) -> List[State]:
        return [s for s in State][:-1]


def make(update: Update, context: CallbackContext):
    """Отвечает на команду /make, предлагает выбрать категорию из списка"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /make")

    update.message.reply_text(messages.category, reply_markup=keyboards.categories)
    context.user_data["state"] = State.CATEGORY
    return State.CATEGORY


def category(update: Update, context: CallbackContext):
    """
    Добавляет категорию в контекст пользователя и предлагает ввести группу.
    Информация, записанная в контексте юзера будет болтаться в рантайме, а
    когда студент подтвердит правильность введенных данных, добавится в бд
    """
    logger.info(f"User with chat_id {update.effective_user.id} selected category [{update.message.text}].")

    context.user_data[State.CATEGORY] = update.message.text

    update.message.reply_text(messages.group_name)
    context.user_data["state"] = State.GROUP_NAME
    return State.GROUP_NAME


def group_name(update: Update, context: CallbackContext):
    """Добавляет группу в контекст пользователя и предлагает ввести пол"""
    logger.info(f"User with chat_id {update.effective_user.id} sent group name [{update.message.text}]")

    context.user_data[State.GROUP_NAME] = update.message.text

    update.message.reply_text(messages.gender, reply_markup=keyboards.genders)
    context.user_data["state"] = State.GENDER
    return State.GENDER


def gender(update: Update, context: CallbackContext):
    """Добавляет пол в контекст пользователя и предлагает ввести фамилию"""
    logger.info(f"User with chat_id {update.effective_user.id} selected gender [{update.message.text}]")

    context.user_data[State.GENDER] = update.message.text

    update.message.reply_text(messages.surname)
    context.user_data["state"] = State.SURNAME
    return State.SURNAME


def surname(update: Update, context: CallbackContext):
    """Добавляет фамилию в контекст пользователя и предлагает ввести имя"""
    logger.info(f"User with chat_id {update.effective_user.id} sent surname [{update.message.text}]")

    context.user_data[State.SURNAME] = update.message.text

    update.message.reply_text(messages.name)
    context.user_data["state"] = State.NAME
    return State.NAME


def name(update: Update, context: CallbackContext):
    """Добавляет имя в контекст пользователя и предлагает ввести отчество"""
    logger.info(f"User with chat_id {update.effective_user.id} sent name [{update.message.text}]")

    context.user_data[State.NAME] = update.message.text

    update.message.reply_text(messages.middle_name)
    context.user_data["state"] = State.MIDDLE_NAME
    return State.MIDDLE_NAME


def middle_name(update: Update, context: CallbackContext):
    """Добавляет отчество в контекст пользователя и предлагает ввести номер телефона"""
    logger.info(f"User with chat_id {update.effective_user.id} sent middle name [{update.message.text}]")

    context.user_data[State.MIDDLE_NAME] = update.message.text

    update.message.reply_text(messages.phone_number)
    context.user_data["state"] = State.PHONE_NUMBER
    return State.PHONE_NUMBER


def phone_number(update: Update, context: CallbackContext):
    """Добавляет номер телефона в контекст пользователя и предлагает ввести ИНН"""
    logger.info(f"User with chat_id {update.effective_user.id} sent phone number [{update.message.text}]")

    context.user_data[State.PHONE_NUMBER] = update.message.text

    update.message.reply_text(messages.inn, parse_mode=ParseMode.HTML)
    context.user_data["state"] = State.INN
    return State.INN


def inn(update: Update, context: CallbackContext):
    """
    Добавляет ИНН в контекст пользователя и предлагает подтвердить
    правильность введенных данных
    """
    logger.info(f"User with chat_id {update.effective_user.id} sent INN [{update.message.text}]")

    context.user_data[State.INN] = update.message.text

    update.message.reply_text(
        messages.check + "{}\n{}\n{}\n{} {} {}\n{}\n{}".format(
            *[context.user_data[state] for state in State.get_form_field_states()]
        ),
        reply_markup=keyboards.check
    )
    context.user_data["state"] = State.CHECK
    return State.CHECK


def check(update: Update, context: CallbackContext):
    """Записывает данные из контекста пользователя в бд и отправляет в чат файл заявки"""
    logger.info(f"User with chat_id {update.effective_user.id} selected [{update.message.text}]")

    data = [context.user_data[state] for state in State.get_form_field_states()]
    database.insert_application(data)

    form_bytes = generate_form(*data)
    update.message.reply_document(
        document=form_bytes,
        filename="application.docx",
        caption=messages.success
    )

    group = context.user_data[State.GROUP_NAME]

    course = int(group[4]) if group[5] != "5" else int(group[4]) + int(group[5])
    category_id = database.get_id_by_category(context.user_data[State.CATEGORY])

    update.message.reply_text(
        messages.prepare_documents +
        "\n".join(["- <i>" + doc + "</i>" for doc in database.get_documents_list(category_id)]),
        ParseMode.HTML
    )

    is_dorm = context.user_data[State.CATEGORY] == "студент, проживающий в общежитии"

    update.message.reply_text(
        messages.sign_documents +
        "\n".join(["%d. " % i + step for i, step in
                   enumerate(messages.print_and_sign + (messages.signs_for_dorm if is_dorm else []) + messages.bring_to_head, 1)]) +
        messages.other_signs_not_needed,
        ParseMode.HTML
    )

    update.message.reply_text(messages.your_head % database.get_director(course).strip(" "), ParseMode.HTML)
    update.message.reply_text(messages.bring_it_to, ParseMode.HTML)
    update.message.reply_text(messages.acceptance_period, ParseMode.HTML)
    update.message.reply_text(messages.show_faq)

    # Закрываем буфер
    form_bytes.close()
    return ConversationHandler.END


def again(update: Update, context: CallbackContext):
    """Возвращает состояние CATEGORY, отправляя студента в начало диалога"""
    logger.info(f"User with chat_id {update.effective_user.id} selected [{update.message.text}]")

    context.user_data["state"] = State.CATEGORY
    update.message.reply_text(messages.category, reply_markup=keyboards.categories)

    return State.CATEGORY


def stop(update: Update, context: CallbackContext):
    """Позволяет выйти из диалога"""
    logger.info(f"User with chat_id {update.effective_user.id} stopped dialog")

    update.message.reply_text(messages.stop)

    return ConversationHandler.END


def wrong(update: Update, context: CallbackContext):
    """Хендлер обрабатывает любой неверный ввод и возвращает последнее состояние диалога"""
    logger.info(f"User with chat_id {update.effective_user.id} "
                f"sent wrong input [{update.message.text}] on state [{context.user_data['state']}]")

    update.message.reply_text(messages.wrong)
    return context.user_data["state"]


make_handler = CommandHandler("make", make)

conversation_handler = ConversationHandler(
    entry_points=[make_handler],
    states={
        State.CATEGORY:     [MessageHandler(Filters.text(database.get_categories_list()), category)],
        State.GROUP_NAME:   [MessageHandler(Filters.regex(r"^[А-ЯЁ]{3}-[1-5]{2}[1-9]$"), group_name)],
        State.GENDER:       [MessageHandler(Filters.text(["Мужской", "Женский"]), gender)],
        State.SURNAME:      [MessageHandler(Filters.regex(r"^[а-яёА-ЯЁ-]{1,20}$"), surname)],
        State.NAME:         [MessageHandler(Filters.regex(r"^[а-яёА-ЯЁ-]{1,20}$"), name)],
        State.MIDDLE_NAME:  [MessageHandler(Filters.regex(r"^[а-яёА-ЯЁ-]{1,20}$"), middle_name)],
        State.PHONE_NUMBER: [MessageHandler(Filters.regex(r"^[0-9]{10}$"), phone_number)],
        State.INN:          [MessageHandler(Filters.regex(r"^[0-9]{10,13}$"), inn)],
        State.CHECK:        [
            MessageHandler(Filters.text(["Заполнить заявку заново"]), again),
            MessageHandler(Filters.text(["Все верно"]), check)
        ]
    },
    fallbacks=[
        make_handler,
        CommandHandler("stop", stop),
        MessageHandler(Filters.all, wrong)
    ]
)
