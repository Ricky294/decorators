from decorators.core import *


@shuffle
def shuffle_example():
    print('Shuffling return items.')
    return [i for i in range(20)]


def run_core_examples():
    print(shuffle_example())


if __name__ == '__main__':
    run_core_examples()
