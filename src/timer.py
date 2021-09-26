import datetime
import time
from typing import Callable, Union
from functools import wraps


__all__ = ['delay', 'timeit', 'only_between_time', 'schedule_run']


def _date_to_datetime(dt: datetime.date):
    return datetime.datetime(dt.year, dt.month, dt.day)


def delay(sec: float):
    """
    Executes the decorated function after ``sec`` seconds.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(sec)
            return func(*args, **kwargs)

        return wrapper
    return decorator


def timeit(func: Callable):
    """
    Measures the execution time of the decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        ret = func(*args, **kwargs)
        duration = time.time_ns() - start

        print(f'{func.__name__!r} executed in: {duration / 1000000000} seconds')

        return ret

    return wrapper


def only_between_time(_func: Callable = None, *, start=datetime.time(hour=8), end=datetime.time(hour=22)):
    """
    Executes the decorated function only if current time is between ``start`` and ``end``.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now().time()

            if start <= now < end:
                return func(*args, **kwargs)
            else:
                pass
        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


def schedule_run(when: Union[datetime.datetime, datetime.time, datetime.date, int, float]):
    """
    Executes the decorated function at ``when``.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if isinstance(when, datetime.datetime):
                ts = when.timestamp()
            elif isinstance(when, datetime.date):
                ts = _date_to_datetime(when).timestamp()
            elif isinstance(when, datetime.time):
                today = datetime.datetime.now().date()
                ts = datetime.datetime(
                    today.year, today.month, today.day,
                    when.hour, when.minute, when.second, when.microsecond
                ).timestamp()
            else:
                ts = when

            # Too late! Current time is already ahead of the parameter time.
            if ts < time.time():
                return

            while True:
                if ts <= time.time():
                    ret = func(*args, **kwargs)
                    return ret

        return wrapper

    return decorator
