import unittest

import numpy as np
import pandas as pd
from decorators.convert import to_series, to_dataframe


class TestObjectDict:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class TestObjectSlots:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


@to_series(index=('x', 'y', 'z'))
def test_to_series_tuple():
    return 5, 10, 15


@to_series(index=('x', 'y', 'z'))
def test_to_series_list():
    return [5, 10, 15]


@to_series(index=('x', 'y', 'z'))
def test_to_series_nparray():
    return np.array([5, 10, 15], dtype=np.int64)


@to_series
def test_to_series_slots_object():
    return TestObjectSlots(5, 10, 15)


@to_series
def test_to_series_dict_object():
    return TestObjectDict(5, 10, 15)


@to_dataframe
def test_to_dataframe_dict():
    return {'x': [5, 10], 'y': [15, 20], 'z': [25, 30]}


@to_dataframe
def test_to_dataframe_slots_object():
    return TestObjectSlots([5, 10], [15, 20], [25, 30])


@to_dataframe
def test_to_dataframe_dict_object():
    return TestObjectDict([5, 10], [15, 20], [25, 30])


@to_dataframe(columns=('x', 'y', 'z'))
def test_to_dataframe_nparray():
    return np.array([[5, 15, 25], [10, 20, 30]], dtype=np.int64)


@to_dataframe()
def test_to_dataframe_series():
    return pd.Series([5, 10, 15, 20, 25, 30])


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ser = pd.Series([5, 10, 15], index=('x', 'y', 'z'))
        self.df = pd.DataFrame({'x': [5, 10], 'y': [15, 20], 'z': [25, 30]})

    def test_to_series(self):
        self.assertTrue(test_to_series_tuple().equals(self.ser))
        self.assertTrue(test_to_series_list().equals(self.ser))
        self.assertTrue(test_to_series_slots_object().equals(self.ser))
        self.assertTrue(test_to_series_dict_object().equals(self.ser))
        self.assertTrue(test_to_series_nparray().equals(self.ser))

    def test_to_dataframe(self):
        self.assertTrue(test_to_dataframe_dict().equals(self.df))
        self.assertTrue(test_to_dataframe_slots_object().equals(self.df))
        self.assertTrue(test_to_dataframe_dict_object().equals(self.df))
        self.assertTrue(test_to_dataframe_nparray().equals(self.df))
        self.assertTrue(test_to_dataframe_series().equals(pd.DataFrame([5, 10, 15, 20, 25, 30])))


if __name__ == '__main__':
    unittest.main()
