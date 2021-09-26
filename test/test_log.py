import logging
import unittest

from decorators.log import log_return, inject_logger, create_logger, LogError, log_exception
from test import join_to_absolute_path

_LOGGER1 = 'test_logger1'
_LOGGER2 = 'test_logger2'
_NOT_EXISTS_LOGGER = 'test_logger_not_exists'
_EXCEPTION_LOGGER = 'test_exception_logger'


@log_return(name=_LOGGER1)
def test_log_return1():
    return 'Return value logging! (1)'


@log_return(name=_LOGGER2)
def test_log_return2():
    return 'Return value logging! (2)'


@inject_logger(name=_LOGGER1)
def test_inject_logger1():
    logger: logging.Logger = test_inject_logger1.logger
    logger.info('Inject logger log! (1)')


@inject_logger(name=[_LOGGER1, _LOGGER2])
def test_inject_logger2():
    logger1 = test_inject_logger2.logger[0]
    logger2 = test_inject_logger2.logger[1]
    logger1.info('Inject logger log! (1)')
    logger2.info('Inject logger log! (2)')


@log_return(name=_NOT_EXISTS_LOGGER)
def test_log_return_not_exists():
    return 'Return value logging! (2)'


@inject_logger(name=_NOT_EXISTS_LOGGER)
def test_inject_logger_not_exists():
    logger: logging.Logger = test_inject_logger_not_exists.logger
    logger.info('Inject logger log! (2)')


@log_exception(name=_EXCEPTION_LOGGER)
def test_log_exception():
    raise ValueError('Testing an exception!')


def setUpModule():
    create_logger(_LOGGER1)
    create_logger(_LOGGER2, file_path=join_to_absolute_path('logs', f'{_LOGGER2}.log'))
    create_logger(_EXCEPTION_LOGGER, file_path=join_to_absolute_path('logs', f'{_EXCEPTION_LOGGER}.log'))


class MyTestCase(unittest.TestCase):

    def test_logger_errors(self):
        self.assertRaises(LogError, create_logger, _LOGGER1)

        self.assertRaises(LogError, test_log_return_not_exists)
        self.assertRaises(LogError, test_inject_logger_not_exists)

    def test_log_return_decorated_functions(self):
        self.assertEqual(test_log_return1(), 'Return value logging! (1)')
        self.assertEqual(test_log_return2(), 'Return value logging! (2)')

    def test_inject_logger_decorated_functions(self):
        test_inject_logger1()
        test_inject_logger2()

    def test_log_exception_decorated_functions(self):
        self.assertRaises(ValueError, test_log_exception)


if __name__ == '__main__':
    unittest.main()
