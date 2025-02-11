# -*- coding: utf-8 -*-
""" A class to navigate a data structure. """

import logging
from typing import Any

_logger: logging.Logger = logging.getLogger(__name__)


class DataNavigator:
    """A class to navigate a data structure."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.root = data
        self.current = data
        self.history = []
        self.path = ["/"]

    def ls(self) -> None:
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

    def cd(self, key: str) -> None:
        """Change directory in data structure."""
        if key == "..":
            if self.history:
                self.current = self.history.pop()
                self.path.pop()
            else:
                _logger.info("Déjà à la racine.")
        elif isinstance(self.current, dict) and key in self.current:
            self.history.append(self.current)
            self.current = self.current[key]
            self.path.append(key)
        elif isinstance(self.current, list):
            try:
                index = int(key)
                if 0 <= index < len(self.current):
                    self.history.append(self.current)
                    self.current = self.current[index]
                    self.path.append(str(index))
                else:
                    print("Index hors limite.")
            except ValueError:
                _logger.info("Utilisation: cd <clé> ou cd <index>")
        else:
            _logger.info("Chemin invalide.")

    def clear(self) -> None:
        """Cleans the console."""
        _logger.info("\033c")

    def run(self) -> int:
        """Main navigation loop."""
        while True:
            cmd = input(f"📂 {self.get_path()} > ").strip().split(maxsplit=1)
            if not cmd:
                continue
            if cmd[0] == "ls":
                self.ls()
            elif cmd[0] == "cd":
                self.cd(cmd[1] if len(cmd) > 1 else "..")
            elif cmd[0] == "clear":
                self.clear()
            elif cmd[0] == "exit":
                break
            else:
                _logger.info("Commandes disponibles: ls, cd <clé|index>, cd .., exit")
        return 0
