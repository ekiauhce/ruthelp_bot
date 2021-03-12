from telegram.ext import Updater
from os import environ
from bot import commands
from bot import form
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TG_API_TOKEN = environ.get("TG_API_TOKEN")
# HOST_IP = environ.get("HOST_IP")


def main():
    updater = Updater(TG_API_TOKEN)

    dp = updater.dispatcher

    [dp.add_handler(handler) for handler in commands.handlers_list]
    dp.add_handler(form.conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
