""" Tests for the data navigator methods. """

import logging
import unittest
from unittest.mock import patch
from data_navigator import DataNavigator

logging.disable(logging.CRITICAL)


class TestDataNavigator(unittest.TestCase):
    """Tests for the data navigator methods."""

    def test(self) -> None:
        """The main test function."""
        data = {
            "users": {
                "alice": {"age": "25", "city": "Paris"},
                "bob": {"age": "30", "city": "Lyon"},
            },
            "posts": [
                "alpha",
                "beta",
            ],
        }
        DataNavigator.clear()
        navigator = DataNavigator(data)

        navigator.setup_autocomplete()
        self.assertEqual(navigator.complete_path("", 0), "users")
        self.assertIsNone(navigator.complete_path("", 2))
        self.assertIsNone(navigator.complete_path("user/al", 0))
        self.assertIsNone(navigator.complete_path("posts/0", 0))
        self.assertEqual(navigator.get_path(), "/")
        self.assertEqual(navigator.ls("machin"), "")
        self.assertEqual(navigator.ls(""), "users  posts")
        navigator.cd("machin")
        self.assertEqual(navigator.current, data)
        navigator.cd("users")
        self.assertEqual(navigator.current, data["users"])
        navigator.cd("")
        self.assertEqual(navigator.current, data)
        navigator.cd("posts/0")
        self.assertEqual(navigator.ls("."), "Valeur: alpha")
        self.assertEqual(navigator.current, data["posts"][0])
        navigator.cd("../../..")
        self.assertEqual(navigator.current, data)
        navigator.cd("posts")
        self.assertEqual(navigator.ls("."), "0  1")
        navigator.cd("2")
        self.assertEqual(navigator.current, data["posts"])
        navigator.cd("machin")
        self.assertEqual(navigator.current, data["posts"])

        navigator.process_input(["ls"])
        navigator.process_input(["ls", "alpha"])

        navigator.process_input(["cd"])
        navigator.process_input(["cd", "users"])
        navigator.process_input(["clear"])
        navigator.process_input(["exit"])
        navigator.process_input(["q"])
        navigator.process_input(["machin"])

    @patch("builtins.input", side_effect=["ls", "cd subdir", "", "exit"])
    def test_run(self, _) -> None:
        """Test the loop."""
        data = {"subdir": {"file.txt": "content"}}
        navigator = DataNavigator(data)

        with patch(
            "app.data_navigator.data_navigator._logger.info"
        ) as _:
            exit_code = navigator.run()

        # Check the the loop ended
        self.assertEqual(exit_code, 0)
