import logging
from telegram.ext import Updater
from os import environ
from bot import handlers

# TODO: писать логи в файл
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


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
