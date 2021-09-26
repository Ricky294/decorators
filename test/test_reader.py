import json
import unittest

from decorators import read_lines, read_json
from test import join_to_absolute_path


@read_lines(join_to_absolute_path("resources", "empty_file.txt"))
def read_lines_empty_file():
    return read_lines_empty_file.lines


@read_lines(join_to_absolute_path("resources", "file_with_lines.txt"))
def read_lines_no_blank():
    return read_lines_no_blank.lines


@read_lines(join_to_absolute_path("resources", "file_with_lines.txt"), filter_empty=False)
def read_lines():
    return read_lines.lines


@read_json(join_to_absolute_path("resources", "json_file.json"))
def read_json():
    return read_json.json


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


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        with open(join_to_absolute_path('resources', 'file_with_lines.txt'), 'w') as f:
            f.writelines(file_content)

        with open(join_to_absolute_path('resources', 'json_file.json'), 'w') as f:
            f.write(json.dumps(json_content))

    def test_read_lines(self):
        self.assertEqual(read_lines_empty_file(), [])
        self.assertEqual(read_lines_no_blank(), ['line 1\n', 'line 2\n', 'line 3\n', 'line 4'])
        self.assertEqual(read_lines(), file_content)

    def test_read_json(self):
        self.assertEqual(read_json(), json_content)


if __name__ == '__main__':
    unittest.main()
