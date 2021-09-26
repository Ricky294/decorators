# How to run all test:
# 1. cd to root folder if needed
# 2. run: python -m unittest


def join_to_absolute_path(*args):
    from pathlib import Path
    return Path(__file__).absolute().parent.joinpath(*args)
