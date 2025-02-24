""" Tests for the utils methods. """

import logging
import unittest

from rich.progress import Progress, TaskID

from utils.utils import count_char_line_file
from utils import FileParser

logging.disable(logging.CRITICAL)


class TestUtils(unittest.TestCase):
    """Tests for the utils methods."""

    def test(self) -> None:
        """The main test function."""
        nb_line, nb_char = count_char_line_file(
            "app/tests/files/mock_file.txt"
        )
        self.assertEqual(nb_line, 5)
        self.assertEqual(nb_char, 18)

        data = {}
        with Progress(disable=True) as progress:
            task: TaskID = progress.add_task("")
            file_parser = FileParser("app/tests/files/gamestate_short")
            file_parser.word_end("MACHIN")
            data = file_parser.parse_large_file_character_by_character(
                progress, task
            )
        self.assertIsInstance(data, dict)
        self.assertIn("a", data)
        self.assertIsInstance(data["a"], list)
        self.assertEqual(len(data["a"]), 1)
        self.assertIsInstance(data["a"][0], list)
        self.assertEqual(len(data["a"][0]), 2)
        self.assertIsInstance(data["a"][0][0], str)
        self.assertEqual(data["a"][0][0], "b")
        self.assertIsInstance(data["a"][0][1], str)
        self.assertEqual(data["a"][0][1], '"c"')
        self.assertIn("d", data)
        self.assertIsInstance(data["d"], dict)
        self.assertIn("e", data["d"])
        self.assertIsInstance(data["d"]["e"], dict)
        self.assertIn("f", data["d"]["e"])
        self.assertEqual(data["d"]["e"]["f"], "g")
