import logging
import os
from datetime import datetime

# https://stackoverflow.com/questions/39718895/python-multiple-logger-for-multiple-modules/39719135
# https://blog.muya.co.ke/configuring-multiple-loggers-python/
# https://gist.github.com/nguyendv/ccf4d9e1d0b4679da938872378c46226

def setup_logger(logger_name,level=logging.INFO):
    logger = None

    cur_path = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(cur_path, r"./logs/")

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    formatter = logging.Formatter(
        '[%(asctime)s - %(filename)s:%(lineno)i - %(funcName)s() %(levelname)s ] - %(message)s')
    current_time = datetime.strftime(datetime.now(), '%m%d%Y')

    if logger_name == "http_request_logger":
        logger = logging.getLogger(logger_name)
        fileHandler = logging.FileHandler(filename=os.path.join(log_dir,"http_requester_{}.log".format(current_time)),
                                          mode='a')
        fileHandler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(fileHandler)

    if logger_name == "component_health_check_logger":
        logger = logging.getLogger(logger_name)
        fileHandler = logging.FileHandler(filename=os.path.join(log_dir,"component_health_check_{}.log".format(current_time)), mode='a')

        # fileHandler = logging.FileHandler(filename="/logs/component_health_check_{}.log".format(current_time),
        #                                   mode='a')
        fileHandler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(fileHandler)

    return logger

