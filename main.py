import logging
from telegram.ext import Updater
import os
from bot import handlers

#TODO: писать логи в файл
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(os.environ.get("TG_API_TOKEN"))

    dp = updater.dispatcher
    dp.add_handler(handlers.start_handler)
    dp.add_handler(handlers.conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()