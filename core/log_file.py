import logging

def my_log(name):
    log_file = "../log/%s.log"%name
    log_level = logging.DEBUG

    logger = logging.getLogger(name)
    handler = logging.FileHandler(log_file,encoding="utf-8")
    formatter = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger