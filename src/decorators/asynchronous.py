from typing import Iterable, Callable
from functools import wraps

__all__ = [
    'run_forever', 'run_thread', 'run_thread_pool', 'run_process'
]


def run_thread(_func: Callable = None, *, daemon=False):

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import threading

            thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=daemon)
            thread.start()
            return thread

        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def run_thread_pool(args: Iterable):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper():
            from concurrent import futures
            with futures.ThreadPoolExecutor() as executor:
                executor.map(func, args)

        return wrapper

    return decorator


def run_process(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import multiprocessing
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        return process

    return wrapper


def do_on_user_input(_func: Callable = None, *, prompt=''):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            inp = input(prompt)
            kwargs['user_input'] = inp
            ret = func(*args, **kwargs)
            return ret
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)


def non_blocking_user_input(func: Callable):
    import threading
    import queue

    def add_input(input_queue):
        import sys

        while True:
            input_queue.put(sys.stdin.readline())
            sys.stdout.flush()

    @wraps(func)
    def wrapper(*args, **kwargs):
        input_queue = queue.Queue()

        input_thread = threading.Thread(target=add_input, args=(input_queue,))
        input_thread.daemon = True
        input_thread.start()

        while True:
            if not input_queue.qsize() == 0:
                print('NOT EMTPY')
                kwargs['user_input'] = input_queue.get()
                ret = func(*args, **kwargs)
                return ret

    return wrapper


def run_on_every(_func: Callable = None, *, seconds=1.0):
    from apscheduler.schedulers.background import BackgroundScheduler
    sx = BackgroundScheduler()

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['scheduler'] = sx
            sx.add_job(func, 'interval', seconds=seconds, args=args, kwargs=kwargs)
            sx.start()

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)


def run_forever(func: Callable):
    import asyncio

    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            ret = func(*args, **kwargs)
            loop.run_forever()
        finally:
            loop.close()
        return ret
    return wrapper
