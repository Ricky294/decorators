def join_to_absolute_path(*args):
    from pathlib import Path
    return Path(__file__).absolute().parent.joinpath(*args)
