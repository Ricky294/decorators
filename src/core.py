from typing import Callable, Type, Tuple, List
from functools import wraps

__all__ = ['not_none_or_empty',  'not_none', 'repeat', 'shuffle', 'singleton', 'count_calls']


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


def not_none(func: Callable):
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


def not_none_or_empty(func: Callable):
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
    else:
        return decorator(_func)


def shuffle(_func: Callable = None, *, in_place=False):
    """
    Randomly shuffles the items in the container.
    """

    import numpy as np

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import random

            arr = func(*args, **kwargs)

            if isinstance(arr, np.ndarray):
                if in_place:
                    np.random.shuffle(arr)
                else:
                    arr_copy = np.ndarray.copy(arr)
                    np.random.shuffle(arr_copy)
                    return arr_copy
            elif isinstance(arr, List):
                if in_place:
                    random.shuffle(arr)
                else:
                    return random.sample(arr, len(arr))
            elif isinstance(arr, Tuple):
                if in_place:
                    arr = tuple(random.sample(arr, len(arr)))
                else:
                    return tuple(random.sample(arr, len(arr)))

            return arr

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

