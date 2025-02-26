# -*- coding: utf-8 -*-
""" A file parser. """

import logging
from typing import Any, Optional

from rich.progress import Progress, TaskID

_logger: logging.Logger = logging.getLogger(__name__)


class FileParser:
    """A class to parse a file."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.stack = [(None, {})]
        self.curr_key = None
        self.in_string = False
        self.buffer = []
        self.just_saw_separator = False

    def clear(self) -> None:
        """Reset the buffer and key."""
        self.buffer.clear()
        self.curr_key = None

    def add_element(self, new_element: str | dict[str, Any]) -> None:
        """Add a new element."""
        if isinstance(self.stack[-1][1], list):
            self.stack[-1][1].append(new_element)
        elif self.curr_key is not None:
            if self.curr_key in self.stack[-1][1]:
                if isinstance(self.stack[-1][1][self.curr_key], list):
                    self.stack[-1][1][self.curr_key].append(new_element)
                else:
                    self.stack[-1][1][self.curr_key] = [self.stack[-1][1][self.curr_key], new_element]
            else:
                self.stack[-1][1][self.curr_key] = new_element
        else:
            self.turn_dict_to_list(new_element)

    def process_word(self) -> None:
        """Process one word."""
        if self.buffer:
            self.add_element("".join(self.buffer).strip())
            self.clear()

    def add_container(self) -> None:
        """Add a container to the stack."""
        new_element = {}
        self.add_element(new_element)
        self.stack.append((self.curr_key, new_element))
        self.clear()

    def turn_dict_to_list(self, new_element: str | dict[str, Any]) -> None:
        """Turn a dict into a list."""
        tmp_key: str | int | None = self.stack[-1][0]
        if tmp_key is None:
            tmp_key = -1
        self.stack[-2][1][tmp_key] = [new_element]
        self.stack[-1] = (tmp_key, self.stack[-2][1][tmp_key])

    def process_quote(self) -> None:
        """Process the " caracter."""
        if self.in_string:
            self.buffer = ['"'] + self.buffer + ['"']
            self.in_string = False
        else:
            if self.just_saw_separator:
                self.process_word()
            self.in_string = True
            self.just_saw_separator = False

    def word_end(self, case: str, char: str = "") -> None:
        """Process the end of a word."""
        if self.just_saw_separator or case == "END_BLOCK":
            self.process_word()
        match case:
            case "START_BLOCK":
                self.add_container()
            case "END_BLOCK":
                self.stack.pop()
            case "LETTER":
                self.buffer.append(char)
            case _:
                _logger.critical("Error")
        self.just_saw_separator = False

    def parse_large_file_character_by_character(
        self,
        progress: Optional[Progress] = None,
        task: Optional[TaskID] = None,
    ) -> dict[str, Any]:
        """Parse a large file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            while True:
                # W read one character
                char = f.read(1)

                # End of file
                if not char:
                    break

                progress.update(task, advance=1)

                # Begining or end of string
                if char == '"':
                    self.process_quote()

                # If we are in a string, we add the characters
                elif self.in_string:
                    self.buffer.append(char)

                # Key detection
                elif char == "=":
                    self.curr_key = "".join(self.buffer).strip()
                    self.buffer.clear()
                    self.just_saw_separator = False

                # Beginning of a block
                elif char == "{":
                    self.word_end("START_BLOCK")

                # End of a block
                elif char == "}":
                    self.word_end("END_BLOCK")

                elif char in (" ", "\t", "\n", "\r", "\r\n"):
                    self.just_saw_separator = True
                else:
                    self.word_end("LETTER", char)

            self.process_word()
            return self.stack[0][1]
