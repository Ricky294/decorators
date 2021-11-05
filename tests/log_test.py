import logging
import os.path

import pytest
from decorators.log import (
    create_logger,
    log_return,
    log_exception,
    inject_logger,
    LogError,
)

_LOGGER1 = "test_logger1"
_LOGGER2 = "test_logger2"
_NOT_EXISTS_LOGGER = "test_logger_not_exists"
_EXCEPTION_LOGGER = "test_exception_logger"


create_logger(_LOGGER1)
create_logger(_LOGGER2, file_path=os.path.join("tests", f"{_LOGGER2}.log"))
create_logger(
    _EXCEPTION_LOGGER, file_path=os.path.join("tests", f"{_EXCEPTION_LOGGER}.log")
)


def test_log_return():
    log_return(name=_LOGGER1)(lambda: "Return value logging! (1)")()
    log_return(name=_LOGGER2)(lambda: "Return value logging! (2)")()

    with pytest.raises(LogError):
        log_return(name=_NOT_EXISTS_LOGGER)(
            lambda: "Trying to log with a non-existent logger."
        )()


def test_inject_logger():
    @inject_logger(name=_LOGGER1)
    def one_logger():
        logger: logging.Logger = one_logger.logger
        logger.info("Inject logger log! (1)")

    @inject_logger(name=[_LOGGER1, _LOGGER2])
    def multi_logger():
        logger1 = multi_logger.logger[0]
        logger2 = multi_logger.logger[1]
        logger1.info("Inject logger log! (1)")
        logger2.info("Inject logger log! (2)")

    @inject_logger(name=[_NOT_EXISTS_LOGGER])
    def inject_logger_not_exists():
        logger: logging.Logger = inject_logger_not_exists.logger
        logger.info("Inject logger log! (2)")

    one_logger()
    multi_logger()

    with pytest.raises(LogError):
        inject_logger_not_exists()


def test_log_exception():
    with pytest.raises(ZeroDivisionError):
        log_exception(name=_EXCEPTION_LOGGER)(lambda: 1 / 0)()
