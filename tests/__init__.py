def join_to_absolute_path(*args):
    import os

    return "file://" + os.path.abspath(os.path.expanduser(os.path.expandvars(os.path.join('tests', *args))))

