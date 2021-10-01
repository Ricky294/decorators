from typing import Callable, Type, Dict, Iterable, Union
from functools import wraps
import pandas as pd
import numpy as np
import random

__all__ = [
    'return_not_none_or_empty', 'return_not_none', 'repeat', 'shuffle',
    'singleton', 'count_calls', 'flatten_dict'
]


def flatten_dict(_func: Callable[..., Dict] = None, *, sep: str = '.'):
    def decorator(func: Callable[..., Dict]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            [flat_dict] = pd.json_normalize(ret, sep=sep).to_dict(orient='records')
            return flat_dict
        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)


def count_calls(func):
    """
    Counts how many times the decorated function was called.

    You can get the ``call_counter`` by typing: ``decorated_function.call_counter``.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_counter += 1
        return func(*args, **kwargs)

    wrapper.call_counter = 0
    return wrapper


def singleton(cls: Type):
    """
    Creates a Singleton class (only one instance).
    """
    @wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


def required(func: Callable):
    """
    Raises ValueError if any argument or keyword argument is ``None``.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if arg is None:
                raise ValueError(f'Argument at index {i!r} is None.')
        for key, val in kwargs.items():
            if val is None:
                raise ValueError(f'Keyword argument {key!r} is None!')

        val = func(*args, **kwargs)
        return val

    return wrapper


def return_not_none(func: Callable):
    """
    Raises ValueError if the return value is ``None``.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        if val is None:
            raise ValueError('Return value is None.')
        return val

    return wrapper


def return_not_none_or_empty(func: Callable):
    """
    Raises ValueError if the return value is ``None`` or empty.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        from typing import Sized

        val = func(*args, **kwargs)
        if val is None:
            raise ValueError('Return value is None.')
        elif isinstance(val, Sized) and len(val) == 0:
            raise ValueError('Container is empty.')
        return val

    return wrapper


def repeat(_func: Callable = None, *, times=2):
    """
    Number of ``times`` to execute function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)

        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def shuffle(func: Callable[..., Union[Iterable, np.ndarray]]):
    """
    Shuffles all the items in place.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        arr = func(*args, **kwargs)

        if isinstance(arr, np.ndarray):
            np.random.shuffle(arr)

        elif isinstance(arr, Iterable):
            arr = list(arr)
            random.shuffle(arr)

        return arr

    return wrapper
