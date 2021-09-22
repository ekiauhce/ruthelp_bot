import logging
from io import BytesIO

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import os

import database
from spreadsheet import download_from_db, upload_to_db
from . import messages

logger = logging.getLogger(__name__)


PASSWORD = os.environ.get("ADMIN_PASS")


def start(update: Update, context: CallbackContext):
    """Отвечает на команду /start"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /start")

    update.message.reply_text(messages.start)


def download(update: Update, context: CallbackContext):
    """Отправляет xlsx файл, который содержит все заявки студентов"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /download")

    if len(context.args) != 1 or context.args[0] != PASSWORD:
        update.message.reply_text("Неверный пароль!")
        logger.info(f"User with chat_id {update.effective_user.id} sent wrong password")
        return


    spreadsheet_bytes = download_from_db()
    # TODO: caption с инструкцией
    update.message.reply_document(
        document=spreadsheet_bytes,
        filename="applications.xlsx"
    )


def upload(update: Update, context: CallbackContext):
    """Обрабатывает загрузку xlsx файлов"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /upload")

    if len(context.args) != 1 or context.args[0] != PASSWORD:
        update.message.reply_text("Неверный пароль!")
        logger.info(f"User with chat_id {update.effective_user.id} sent wrong password")
        return

    update.message.reply_text("Отправь файл с таблицей:")
    

    return 1


def upload_file(update: Update, context: CallbackContext):
    
    spreadsheet_bytes = BytesIO()
    update.message.document.get_file().download(
        out=spreadsheet_bytes
    )
    upload_to_db(spreadsheet_bytes)
    update.message.reply_text("База данных успешно обновлена!")

    return ConversationHandler.END


def upload_fallback(update: Update, context: CallbackContext):
    update.message.reply_text("Неверное расширение файла!")

    return ConversationHandler.END
    

def guide(update: Update, context: CallbackContext):
    """Инструкция для админов"""

    logger.info(f"User with chat_id {update.effective_user.id} sent /guide")

    if len(context.args) != 1 or context.args[0] != PASSWORD:
        update.message.reply_text("Неверный пароль!")
        logger.info(f"User with chat_id {update.effective_user.id} sent wrong password")
        return

    update.message.reply_text(messages.guide, ParseMode.HTML)


def faq(update: Update, context: CallbackContext):
    """Показывает список FAQ"""
    logger.info(f"User with chat_id {update.effective_user.id} sent /faq")

    update.message.reply_text(messages.faq, ParseMode.HTML)


    

# Создаем хендлеры

handlers_list = [
    CommandHandler("start", start),
    CommandHandler("download", download),
    CommandHandler("guide", guide),
    CommandHandler("faq", faq),
    ConversationHandler(
        entry_points=[CommandHandler("upload", upload)],
        states={
            1: [MessageHandler(Filters.document.mime_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), upload_file)]
        },
        fallbacks=[MessageHandler(Filters.all, upload_fallback)]
    ),
]
