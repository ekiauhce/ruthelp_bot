import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
    filemode="a",
    filename="log/ruthelp.log"
)


def get_logger(name: str):
    return logging.getLogger(name)
