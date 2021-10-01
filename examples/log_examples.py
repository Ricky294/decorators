import logging
from decorators.log import *

LOGGER1 = 'logger1'
LOGGER2 = 'logger2'
EXCEPTION_LOGGER = 'exception_logger'


@log_return(name=LOGGER1)
@log_exception(name=EXCEPTION_LOGGER)
def log_return_example(a, b):
    return a / b


@inject_logger(name=LOGGER2)
def inject_logger_example(a, b):
    logger: logging.Logger = inject_logger_example.logger
    logger.info(f'a * b = {a * b}')


@inject_logger(name=[LOGGER1, LOGGER2])
def inject_multiple_logger_example(a, b):
    logger1: logging.Logger = inject_multiple_logger_example.logger[0]
    logger2: logging.Logger = inject_multiple_logger_example.logger[1]

    logger1.info(f'{a} / {b} = {a / b}')
    logger2.info(f'{a} / {b} = {a / b}')


@debug_log(name=LOGGER1)
def debug_log_example(*args, **kwargs):
    return 15


def create_loggers():
    # Creating logger with default parameters.
    create_logger(name=LOGGER1)
    create_logger(name=LOGGER2)

    # By specifying file_path file logging is enabled.
    # This logger won't log anything to the console.
    create_logger(
        name=EXCEPTION_LOGGER,
        file_path='exception_logs.log',
        console_log=False
    )


def run_log_examples():

    # Logs number 5 to console by @log_return
    log_return_example(10, 2)

    try:
        # Raises ZeroDivisionError by @log_exception
        log_return_example(2, 0)
    except ZeroDivisionError:
        pass

    inject_logger_example(10, 2)
    inject_multiple_logger_example(100, 10)

    debug_log_example('val1', 'val2', param3='val3', param4='val4')


if __name__ == '__main__':
    create_loggers()
    run_log_examples()
