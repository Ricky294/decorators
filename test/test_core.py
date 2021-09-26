import unittest
import numpy as np

from decorators.core import *


@not_none_or_empty
def test_none():
    return None


@not_none_or_empty
def test_empty_lst():
    return []


@not_none_or_empty
def test_empty_dct():
    return {}


@not_none_or_empty
def test_empty_tup():
    return ()


@not_none_or_empty
def test_not_empty():
    return 5


@not_none_or_empty
def test_not_empty_list():
    return [5, 10]


@shuffle()
def test_shuffle():
    lst = [5, 10, 15, 20, 25, 30]
    return lst


@count_calls
def count_calls_function():
    pass


@singleton
class SingletonTest:
    pass


@shuffle
def shuffle_tuple():
    return 1, 2, 3, 4, 5, 6, 7


@shuffle
def shuffle_list():
    return [1, 2, 3, 4, 5, 6, 7]


@shuffle
def shuffle_nparray():
    return np.array([1, 2, 3, 4, 5, 6, 7])


class MyTestCase(unittest.TestCase):

    def test_not_none_or_empty(self):
        self.assertRaises(ValueError, test_none)
        self.assertRaises(ValueError, test_empty_tup)
        self.assertRaises(ValueError, test_empty_dct)
        self.assertRaises(ValueError, test_empty_lst)
        self.assertEqual(test_not_empty(), 5)
        self.assertEqual(test_not_empty_list(), [5, 10])

        print(test_shuffle())

    def test_count_calls(self):
        count_calls_function()
        count_calls_function()
        count_calls_function()

        self.assertEqual(count_calls_function.call_counter, 3)

    def test_singleton(self):
        s1 = SingletonTest()
        s2 = SingletonTest()

        self.assertTrue(s1 is s2)

    def test_shuffle(self):
        print(shuffle_tuple())
        print(shuffle_list())
        print(shuffle_nparray())


if __name__ == '__main__':
    unittest.main()
