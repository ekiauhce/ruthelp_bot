from telegram.ext import Updater
from os import environ
from bot import handlers
from log import get_logger


logger = get_logger(__name__)


def main():
    updater = Updater(environ.get("TG_API_TOKEN"))

    dp = updater.dispatcher
    dp.add_handler(handlers.start_handler)
    dp.add_handler(handlers.conv_handler)
    dp.add_handler(handlers.download_handler)
    dp.add_handler(handlers.upload_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
