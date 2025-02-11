# -*- coding: utf-8 -*-
""" A class to navigate a data structure. """

import logging
from typing import Any, Optional

_logger: logging.Logger = logging.getLogger(__name__)


class DataNavigator:
    """A class to navigate a data structure."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.root = data
        self.current = data
        self.history = []
        self.path = ["/"]

    def ls(self, path: Optional[str] = None) -> None:
        """Displays dictionary keys or list indices."""
        if isinstance(self.current, dict):
            _logger.info("  ".join(self.current.keys()))
        elif isinstance(self.current, list):
            _logger.info("  ".join(str(i) for i in range(len(self.current))))
        else:
            _logger.info("Valeur: %s", self.current)

    def get_path(self) -> str:
        """Returns the absolute path as a string."""
        return "/".join(self.path).replace("//", "/")

    def navigate_to(self, path_parts: list[str]) -> None:
        """Try to navigate to the path given in the key list."""
        # Starts at root if ‘/’.
        node = self.root if path_parts[0] == "" else self.current
        new_path = ["/"] if path_parts[0] == "" else self.path[:]
        # Save for rollback if error
        history_snapshot = self.history[:]

        for key in path_parts:
            if key in ("", "."):
                # Ignores a ‘/’ at the beginning or end of a path
                continue
            if key == "..":
                # Does not go beyond the root
                if len(new_path) > 1:
                    node = self.history.pop()
                    new_path.pop()
                continue
            if isinstance(node, dict) and key in node:
                self.history.append(node)
                node = node[key]
                new_path.append(key)
            elif isinstance(node, list):
                try:
                    index = int(key)
                    if 0 <= index < len(node):
                        self.history.append(node)
                        node = node[index]
                        new_path.append(str(index))
                    else:
                        _logger.error("Index %d hors limites.", index)
                        self.history = history_snapshot
                        return
                except ValueError:
                    _logger.error("'%s' n'est pas un index valide.", key)
                    self.history = history_snapshot
                    return
            else:
                _logger.error("'%s' n'existe pas dans la structure.", key)
                self.history = history_snapshot
                return

        self.current = node
        self.path = new_path

    def cd(self, path: str) -> None:
        """Change directory in data structure."""
        self.navigate_to(path.split("/"))

    @staticmethod
    def clear() -> None:
        """Cleans the console."""
        _logger.info("\033c")

    def run(self) -> int:
        """Main navigation loop."""
        while True:
            cmd = input(f"📂 {self.get_path()} > ").strip().split(maxsplit=1)
            if not cmd:
                continue
            if cmd[0] == "ls":
                self.ls(cmd[1] if len(cmd) > 1 else None)
            elif cmd[0] == "cd":
                self.cd(cmd[1] if len(cmd) > 1 else "..")
            elif cmd[0] == "clear":
                self.clear()
            elif cmd[0] == "exit":
                break
            else:
                _logger.info("Commandes disponibles: ls, cd <clé|index>, cd .., exit")
        return 0
