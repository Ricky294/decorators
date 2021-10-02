import numpy as np
import pytest

from decorators.core import flatten_dict, shuffle, return_not_none_or_empty, count_calls, singleton


def test_flatten_dict():
    assert flatten_dict(lambda: {
        'a': {
            'b': 5, 'x': 10, 'y': {
                'q': 10
            },
        },
        'b': 2
    })() == {'b': 2, 'a.b': 5, 'a.x': 10, 'a.y.q': 10}


def test_return_not_none_or_empty():
    with pytest.raises(ValueError):
        assert return_not_none_or_empty(lambda: None)()
        assert return_not_none_or_empty(lambda: [])()
        assert return_not_none_or_empty(lambda: ())()
        assert return_not_none_or_empty(lambda: {})()

    assert return_not_none_or_empty(lambda: 5)() == 5
    assert return_not_none_or_empty(lambda: [5, 10])() == [5, 10]


def test_shuffle():
    gen = [i for i in range(1000)]

    assert shuffle(lambda: gen)() != gen
    assert shuffle(lambda: tuple(gen))() != tuple(gen)
    assert not np.array_equal(shuffle(lambda: np.array(gen))(), np.array(gen))


def test_count_calls():
    @count_calls
    def fun():
        return None

    for i in range(3):
        fun()

    assert fun.call_counter == 3


def test_singleton():

    @singleton
    class SingletonClass:
        pass

    x = SingletonClass()
    y = SingletonClass()
    assert x == y
