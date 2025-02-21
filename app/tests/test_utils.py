""" Tests for the utils methods. """

import unittest
from utils.utils import count_char_line_file
from utils import FileParser


class TestUtils(unittest.TestCase):
    """Tests for the utils methods."""

    def test(self) -> None:
        """The main test function."""
        nb_line, nb_char = count_char_line_file(
            "app/tests/files/mock_file.txt"
        )
        self.assertEqual(nb_line, 5)
        self.assertEqual(nb_char, 18)

        data = FileParser(
            "app/tests/files/gamestate_short"
        ).parse_large_file_character_by_character()
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
