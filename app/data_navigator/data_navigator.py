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

        navigation: Optional[tuple[Any, list[str], list[dict[str, Any]]]] = (
            self.navigate_to(path.split("/"))
        )
        if navigation:
            current: Any = navigation[0]
            if isinstance(current, dict):
                _logger.info("  ".join(current.keys()))
            elif isinstance(current, list):
                _logger.info("  ".join(str(i) for i in range(len(current))))
            else:
                _logger.info("Valeur: %s", current)

    def get_path(self) -> str:
        """Returns the absolute path as a string."""
        return "/".join(self.path).replace("//", "/")

    def navigate_to(
        self, path_parts: list[str]
    ) -> Optional[tuple[Any, list[str], list[dict[str, Any]]]]:
        """Try to navigate to the path given in the key list."""
        # Starts at root if ‘/’.
        node = self.root if path_parts[0] == "" else self.current
        new_path = ["/"] if path_parts[0] == "" else self.path[:]
        history_snapshot = self.history[:]

        for key in path_parts:
            if key in ("", "."):
                # Ignores a ‘/’ at the beginning or end of a path
                continue
            if key == "..":
                # Does not go beyond the root
                if len(new_path) > 1:
                    node = history_snapshot.pop()
                    new_path.pop()
                continue
            if isinstance(node, dict) and key in node:
                history_snapshot.append(node)
                node = node[key]
                new_path.append(key)
            elif isinstance(node, list):
                try:
                    index = int(key)
                    if 0 <= index < len(node):
                        history_snapshot.append(node)
                        node = node[index]
                        new_path.append(str(index))
                    else:
                        _logger.critical("Index %d hors limites.", index)
                        return None
                except ValueError:
                    _logger.critical("'%s' n'est pas un index valide.", key)
                    return None
            else:
                _logger.critical("'%s' n'existe pas dans la structure.", key)
                return None

        return node, new_path, history_snapshot

    def cd(self, path: str) -> None:
        """Change directory in data structure."""
        navigation: Optional[tuple[Any, list[str], list[dict[str, Any]]]] = (
            self.navigate_to(path.split("/"))
        )
        if navigation:
            self.current = navigation[0]
            self.path = navigation[1]
            self.history = navigation[2]

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
                self.ls(cmd[1] if len(cmd) > 1 else ".")
            elif cmd[0] == "cd":
                self.cd(cmd[1] if len(cmd) > 1 else "..")
            elif cmd[0] == "clear":
                self.clear()
            elif cmd[0] == "exit":
                break
            else:
                _logger.info("Commandes disponibles: ls, cd <clé|index>, cd .., exit")
        return 0
