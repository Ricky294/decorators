import logging
from src.log import *

LOGGER = 'logger'
EXCEPTION_LOGGER = 'exception_logger'

create_logger(name=LOGGER, level=logging.DEBUG)  # logger with default params

# Specifying file_path will result logging to this file.
create_logger(
    name=EXCEPTION_LOGGER,
    file_path='exception_logs.log',
    console_log=False
)


@log_return(name=LOGGER)
@log_exception(name=EXCEPTION_LOGGER)
def divide_numbers(a, b):
    return a / b


@inject_logger(name=LOGGER)
def divide_numbers2(a, b):
    logger: logging.Logger = divide_numbers2.logger
    logger.info(f'Dividing number {a} with number {b}.')
    return a / b


@debug_log(name=LOGGER)
def log_function(*args, **kwargs):
    return 15


def log_examples():

    # Logs number 5 to console by @log_return
    divide_numbers(10, 2)

    try:
        # Raises ZeroDivisionError by @log_exception
        divide_numbers(2, 0)
    except ZeroDivisionError:
        pass

    divide_numbers2(10, 2)

    log_function('val1', 'val2', param3='val3', param4='val4')


if __name__ == '__main__':
    log_examples()
