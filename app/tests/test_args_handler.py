""" Tests for the args handler methods. """

import logging
import unittest
from args_handler import ArgsHandler

logging.disable(logging.CRITICAL)


class TestArgsHandler(unittest.TestCase):
    """Tests for the args handler methods."""

    def test(self) -> None:
        """The main test function."""
        handler = ArgsHandler("machin")
        self.assertEqual(
            handler.get_usage(), "usage: execution.py [-h] [file]"
        )
        self.assertEqual(f"{handler}", "[file: machin]")
        with self.assertRaises(SystemExit):
            ArgsHandler("machin", "truc")
