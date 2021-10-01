from decimal import Decimal
from functools import wraps
from typing import Callable, Iterable, Dict, Any

import numpy as np

__all__ = [
    'to_datetime', 'to_date', 'to_time', 'to_dataframe', 'to_series'
]


def to_datetime(_func: Callable = None, *, unit='s'):
    from datetime import datetime, date

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)

            if isinstance(ret, datetime):
                return ret
            elif isinstance(ret, date):
                return datetime(year=ret.year, month=ret.month, day=ret.day)

            ret = Decimal(ret)
            if unit == 'ms' or unit == 'millisec':
                ret /= 1000
            elif unit == 'ns' or unit == 'nanosec':
                ret /= 1000000000

            return datetime.fromtimestamp(float(ret))
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def to_date(_func: Callable = None, *, unit='s'):

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return to_datetime(func, unit=unit)(*args, **kwargs).date()
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def to_time(_func: Callable = None, *, unit='s'):

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return to_datetime(func, unit=unit)(*args, **kwargs).time()
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def to_dataframe(
        _func: Callable = None,
        *,
        columns: Any = None,
        dtype: Any = None,
        copy: Any = None
):
    """
    Converts the return value of the decorated function to a ``pandas.Dataframe``.

    :return: pandas.DataFrame
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import pandas as pd

            ret = func(*args, **kwargs)

            if isinstance(ret, (Dict, np.ndarray, pd.Series)):
                data = ret
            elif isinstance(ret, Iterable):
                try:
                    data = [o.__dict__ for o in ret]
                except AttributeError:
                    slots = [o.__slots__ for o in ret][0]
                    data = [{slots[i]: getattr(o, slots[i]) for i in range(len(slots))} for o in ret]
            else:
                try:
                    data = ret.__dict__
                except AttributeError:
                    data = {slot: getattr(ret, slot) for slot in ret.__slots__}

            df = pd.DataFrame(data, columns=columns, dtype=dtype, copy=copy)

            return df
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def to_series(
        _func: Callable = None,
        *,
        index: Any = None,
        dtype: Any = None,
        name: Any = None,
        copy: bool = False,
        fastpath: bool = False
):
    """
    Converts the return value of the decorated function to a ``pandas.Series``.

    :return: pandas.Series
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import pandas as pd

            ret = func(*args, **kwargs)

            if isinstance(ret, Iterable):
                ser = pd.Series(ret, index=index, dtype=dtype, name=name, copy=copy, fastpath=fastpath)
            else:
                try:
                    ret = ret.__dict__
                except AttributeError:
                    slots = ret.__slots__
                    ret = {slots[i]: getattr(ret, slots[i]) for i in range(len(slots))}
                finally:
                    ser = pd.Series(ret, index=index, dtype=dtype, name=name, copy=copy, fastpath=fastpath)
            return ser
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)
