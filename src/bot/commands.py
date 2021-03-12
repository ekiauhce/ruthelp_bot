import logging
from io import BytesIO

from telegram import ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters

import database
from spreadsheet import download_from_db, upload_to_db
from . import messages

from . import filters

logger = logging.getLogger(__name__)


def start(update, context):
    """Отвечает на команду /start"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /start")

    update.message.reply_text(messages.start)


def download(update, context):
    """Отправляет xlsx файл, который содержит все заявки студентов"""
    logger.info(f"User with chat_id {update.effective_user.id} downloaded applications.xlsx")

    spreadsheet_bytes = download_from_db()
    # TODO: caption с инструкцией
    update.message.reply_document(
        document=spreadsheet_bytes,
        filename="applications.xlsx"
    )


def upload(update, context):
    """Обрабатывает загрузку xlsx файлов"""
    logger.info(f"User with chat_id {update.effective_user.id} uploaded applications spreadsheet")

    spreadsheet_bytes = BytesIO()
    update.message.document.get_file().download(
        out=spreadsheet_bytes
    )
    upload_to_db(spreadsheet_bytes)
    update.message.reply_text("База данных успешно обновлена!")


def guide(update, context):
    """Инструкция для админов"""

    logger.info(f"User with chat_id {update.effective_user.id} sent /guide")

    update.message.reply_text(messages.guide, ParseMode.HTML)


def faq(update, context):
    """Показывает список FAQ"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /faq")

    update.message.reply_text(messages.faq, ParseMode.HTML)


def admins(update, context):
    """Возвращает список админов"""
    update.message.reply_text("\n".join(map(str, filters.admins.user_ids)))


def add_admin(update, context):
    """Добавить пользователя в admins_filter и бд"""
    try:
        chat_id = int(context.args[0])
    except ValueError:
        update.message.reply_text("Invalid chat_id! int expected")
    except IndexError:
        update.message.reply_text("Enter chat_id as command argument!")
    else:
        filters.admins.add_user_ids(chat_id)
        if database.insert_admin(chat_id):
            update.message.reply_text(f"User with chat_id {chat_id} has added to admins")
            logger.info(f"User with chat_id {chat_id} added to admins")
        else:
            update.message.reply_text(f"User with chat_id {chat_id} is already an admin!")


def remove_admin(update, context):
    """Удалить пользователя из admins_filter и бд"""
    try:
        chat_id = int(context.args[0])
    except ValueError:
        update.message.reply_text("Invalid chat_id! int expected")
    except IndexError:
        update.message.reply_text("Enter chat_id as command argument!")
    else:
        filters.admins.remove_user_ids(chat_id)
        if database.delete_admin(chat_id):
            update.message.reply_text(f"User with chat_id {chat_id} has removed from admins")
            logger.info(f"User with chat_id {chat_id} removed from admins")
        else:
            update.message.reply_text(f"User with chat_id {chat_id} is not an admin!")


# Создаем хендлеры

handlers_list = [
    CommandHandler("start", start),
    CommandHandler("admins", admins, filters.author),
    CommandHandler("add_admin", add_admin, filters.author),
    CommandHandler("remove_admin", remove_admin, filters.author),
    CommandHandler("download", download, filters.admins),
    CommandHandler("guide", guide, filters.admins),
    CommandHandler("faq", faq),
    MessageHandler(Filters.document.mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                   & filters.admins, upload)
]
