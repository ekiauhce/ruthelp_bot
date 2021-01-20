#! /home/ekiauhce/code/python/ruthelp_bot/env/bin/python

from telegram.ext import Updater
from os import environ
from bot import handlers
from log import get_logger


logger = get_logger(__name__)

TG_API_TOKEN = environ.get("TG_API_TOKEN")
HOST_IP = environ.get("HOST_IP")


def main():
    updater = Updater(TG_API_TOKEN)

    dp = updater.dispatcher
    dp.add_handler(handlers.start_handler)
    dp.add_handler(handlers.conv_handler)
    dp.add_handler(handlers.download_handler)
    dp.add_handler(handlers.upload_handler)
    dp.add_handler(handlers.admins_handler)
    dp.add_handler(handlers.add_admin_handler)
    dp.add_handler(handlers.remove_admin_handler)

    updater.start_webhook(listen='0.0.0.0',
                          port=8443,
                          url_path=TG_API_TOKEN,
                          key='../ssl/private.key',
                          cert='../ssl/cert.pem',
                          webhook_url=f"https://{HOST_IP}:8443/{TG_API_TOKEN}")
    updater.idle()


if __name__ == '__main__':
    main()
