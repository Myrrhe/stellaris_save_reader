""" Tests for the args handler methods. """

import unittest
from args_handler import ArgsHandler


class TestArgsHandler(unittest.TestCase):
    """Tests for the args handler methods."""

    def test(self) -> None:
        """The main test function."""
        handler = ArgsHandler("machin")
        self.assertEqual(
            handler.get_usage(), "usage: execution.py [-h] [file]"
        )
        self.assertEqual(str(handler), "[file: machin]")
        handler = ArgsHandler("machin", "truc")
