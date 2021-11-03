import os
from functools import wraps
from typing import Callable

__all__ = [
    'read_lines', 'read_json'
]


def read_lines(*path: str, filter_empty=True):
    from typing import List

    def decorator(func: Callable[..., List[str]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with open(os.path.join(*path), 'r') as f:
                lines = f.readlines()
                if filter_empty:
                    lines = [line for line in lines if line.strip()]
                wrapper.lines = lines
                return func(*args, **kwargs)

        return wrapper

    return decorator


def read_json(*path: str):
    from typing import Dict

    def decorator(func: Callable[..., Dict]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import json
            with open(os.path.join(*path), 'r') as f:
                jsn = json.loads(f.read())
                wrapper.json = jsn
                return func(*args, **kwargs)

        return wrapper

    return decorator
