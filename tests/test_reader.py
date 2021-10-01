import json

from decorators.reader import *
from tests import join_to_absolute_path

file_content = ['line 1\n', 'line 2\n', '\n', 'line 3\n', '\n', '\n', 'line 4']
json_content = {
            "key1": "val1",
            "key2": 5,
            "key3": [5, 10, 11],
            "key4": {
                "inner_key1": 20,
                "inner_key2": "val2"
            }
        }

with open(join_to_absolute_path('resources', 'file_with_lines.txt'), 'w') as f:
    f.writelines(file_content)

with open(join_to_absolute_path('resources', 'json_file.json'), 'w') as f:
    f.write(json.dumps(json_content))


@read_lines(join_to_absolute_path("resources", "empty_file.txt"))
def read_lines_empty_file():
    return read_lines_empty_file.lines


@read_lines(join_to_absolute_path("resources", "file_with_lines.txt"))
def read_lines_filter_empty():
    return read_lines_filter_empty.lines


@read_lines(join_to_absolute_path("resources", "file_with_lines.txt"), filter_empty=False)
def read_lines():
    return read_lines.lines


@read_json(join_to_absolute_path("resources", "json_file.json"))
def read_json():
    return read_json.json


def test_read_lines():
    assert read_lines_empty_file() == []
    assert read_lines_filter_empty() == ['line 1\n', 'line 2\n', 'line 3\n', 'line 4']
    assert read_lines()


def test_read_json():
    assert read_json() == json_content
