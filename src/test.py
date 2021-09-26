from functools import wraps
from typing import Callable


def debug_print(func: Callable):
    """Print the function signature and return value"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        ret = func(*args, **kwargs)
        print(f"{func.__name__}({signature}) returned {ret!r}")
        return ret
    return wrapper


