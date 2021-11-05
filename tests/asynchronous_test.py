import unittest

from decorators import run_thread


@run_thread
def test_run_on_thread(*args, **kwargs):
    import time

    seconds_to_sleep = 1
    time.sleep(seconds_to_sleep)
    print(f"Printed after {seconds_to_sleep} seconds.")


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test_run_on_thread()


if __name__ == "__main__":
    unittest.main()
