import numpy as np
import pandas as pd
from decorators.convert import *


class DictObject:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SlotsObject:
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


@to_series(index=('x', 'y', 'z'))
def tuple_to_series():
    return 5, 10, 15


@to_series(index=('x', 'y', 'z'))
def list_to_series():
    return [5, 10, 15]


@to_series(index=('x', 'y', 'z'))
def nparray_to_series():
    return np.array([5, 10, 15], dtype=np.int64)


@to_series
def slots_object_to_series():
    return SlotsObject(5, 10, 15)


@to_series
def dict_object_to_series():
    return DictObject(5, 10, 15)


@to_dataframe
def dict_to_dataframe():
    return {'x': [5, 10], 'y': [15, 20], 'z': [25, 30]}


@to_dataframe
def slots_object_to_dataframe():
    return SlotsObject([5, 10], [15, 20], [25, 30])


@to_dataframe
def dict_object_to_dataframe():
    return DictObject([5, 10], [15, 20], [25, 30])


@to_dataframe(columns=('x', 'y', 'z'))
def nparray_to_dataframe():
    return np.array([[5, 15, 25], [10, 20, 30]], dtype=np.int64)


@to_dataframe()
def series_to_dataframe():
    return pd.Series([5, 10, 15, 20, 25, 30])


ser = pd.Series([5, 10, 15], index=('x', 'y', 'z'))
df = pd.DataFrame({'x': [5, 10], 'y': [15, 20], 'z': [25, 30]})


def test_to_series():
    assert tuple_to_series().equals(ser)
    assert list_to_series().equals(ser)
    assert slots_object_to_series().equals(ser)
    assert dict_object_to_series().equals(ser)
    assert nparray_to_series().equals(ser)


def test_to_dataframe():
    assert dict_to_dataframe().equals(df)
    assert slots_object_to_dataframe().equals(df)
    assert dict_object_to_dataframe().equals(df)
    assert nparray_to_dataframe().equals(df)
    assert series_to_dataframe().equals(pd.DataFrame([5, 10, 15, 20, 25, 30]))

