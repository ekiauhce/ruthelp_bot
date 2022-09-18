import os
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


def main():
    updater = Updater(TG_API_TOKEN)

    dp = updater.dispatcher

    [dp.add_handler(handler) for handler in commands.handlers_list]
    dp.add_handler(form.conversation_handler)

    if "POLLING" in os.environ:
        updater.start_polling()
    else:
        PORT = int(os.environ['PORT'])
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TG_API_TOKEN,
            webhook_url="https://ekiauhce.xyz/ruthelp/" + TG_API_TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
