from src.timer import *


@timeit
@delay(sec=0.5)
def timeit_delay_example():
    pass


@delay(sec=0.5)
@timeit
def delay_timeit_example():
    pass


if __name__ == '__main__':
    timeit_delay_example()
    delay_timeit_example()
    print('Note: In some cases like this, decoration order do matter.')
