import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log/ruthelp.log"),
        logging.StreamHandler()
    ]
)


def get_logger(name: str):
    return logging.getLogger(name)
