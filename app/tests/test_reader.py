""" Tests for the reader methods. """

import logging
import unittest
from unittest.mock import patch

from reader.save_reader import read_save

logging.disable(logging.CRITICAL)


class TestReader(unittest.TestCase):
    """Tests for the reader methods."""

    @patch("builtins.input", side_effect=["exit"])
    def test(self, _) -> None:
        """The main test function."""
        exit_code = read_save(
            "app/tests/files/gamestate_short", "app/tests/files/log/log.txt"
        )
        self.assertEqual(exit_code, 0)
