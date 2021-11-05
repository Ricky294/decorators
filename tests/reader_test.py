import json
import os.path

import pytest

from decorators.reader import read_lines, read_json

file_content = "line 1\nline 2\n\nline 3\n\n\nline 4"
json_content = {
    "key1": "val1",
    "key2": 5,
    "key3": [5, 10, 11],
    "key4": {"inner_key1": 20, "inner_key2": "val2"},
}


@pytest.fixture(autouse=True)
def setup_and_tear_down():
    # SETUP

    if not os.path.isdir(os.path.join("tests", "resources")):
        os.mkdir(os.path.join("tests", "resources"))

    with open(os.path.join("tests", "resources", "empty_file.txt"), "w") as _:
        pass

    with open(os.path.join("tests", "resources", "file_with_lines.txt"), "w") as f:
        f.write(file_content)

    with open(os.path.join("tests", "resources", "json_file.json"), "w") as f:
        f.write(json.dumps(json_content))


@read_lines("tests", "resources", "empty_file.txt")
def read_lines_empty_file():
    return read_lines_empty_file.lines


@read_lines("tests", "resources", "file_with_lines.txt")
def read_lines_filter_empty():
    return read_lines_filter_empty.lines


@read_lines("tests", "resources", "file_with_lines.txt", filter_empty=False)
def read_lines():
    return read_lines.lines


@read_json("tests", "resources", "json_file.json")
def read_json():
    return read_json.json


def test_read_lines():
    assert read_lines_empty_file() == []
    assert read_lines_filter_empty() == ["line 1\n", "line 2\n", "line 3\n", "line 4"]
    assert read_lines()


def test_read_json():
    assert read_json() == json_content
