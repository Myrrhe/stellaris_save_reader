# -*- coding: utf-8 -*-
""" A class to navigate a data structure. """

import logging
import readline
from typing import Any, Optional

_logger: logging.Logger = logging.getLogger(__name__)


class DataNavigator:
    """A class to navigate a data structure."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.root = data
        self.current = data
        self.history = []
        self.path = ["/"]

    def ls(self, path: Optional[str] = None) -> str:
        """Displays dictionary keys or list indices."""

        res = ""
        navigation: Optional[tuple[Any, list[str], list[dict[str, Any]]]] = (
            self.navigate_to(path.split("/"))
        )
        if navigation:
            current: str | dict | list = navigation[0]
            if isinstance(current, dict):
                res = "  ".join(current.keys())
            elif isinstance(current, list):
                res = "  ".join(str(i) for i in range(len(current)))
            else:
                res = f"Valeur: {current}"
        return res

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
        ko: bool = False

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
                        ko = True
                        break
                except ValueError:
                    _logger.critical("'%s' n'est pas un index valide.", key)
                    ko = True
                    break
            else:
                _logger.critical("'%s' n'existe pas dans la structure.", key)
                ko = True
                break

        return None if ko else (node, new_path, history_snapshot)

    def cd(self, path: str) -> None:
        """Change directory in data structure."""
        nav: Optional[tuple[Any, list[str], list[dict[str, Any]]]] = (
            self.navigate_to(path.split("/"))
        )
        if nav:
            self.current = nav[0]
            self.path = nav[1]
            self.history = nav[2]

    @staticmethod
    def clear() -> None:
        """Cleans the console."""
        _logger.info("\033c")

    def complete_path(self, text: str, state: int) -> Optional[list[str]]:
        """Automatically completes key names when typing."""
        path_prefix: list[str] = (
            text.rsplit("/", 1)[:-1] if "/" in text else []
        )
        key: str = text.rsplit("/", 1)[-1]

        node: dict[str, Any] = self.current

        if path_prefix:
            nav: Optional[tuple[Any, list[str], list[dict[str, Any]]]] = (
                self.navigate_to(path_prefix)
            )
            if nav:
                node = nav[0]
            else:
                return None

        if isinstance(node, dict):
            options: list[str] = [k for k in node.keys() if k.startswith(key)]
            prefix = f"{"/".join(path_prefix)}/" if path_prefix else ""
            return prefix + options[state] if state < len(options) else None
        return None

    def setup_autocomplete(self) -> None:
        """Configure l'autocomplétion avec la touche Tab."""
        readline.set_completer(self.complete_path)
        readline.parse_and_bind("tab: complete")

    def run(self) -> int:
        """Main navigation loop."""
        self.setup_autocomplete()
        while True:
            cmd = input(f"📂 {self.get_path()} > ").strip().split(maxsplit=1)
            if not cmd:
                continue
            code_run = self.process_input(cmd)
            if code_run == 1:
                break
        return 0

    def process_input(self, cmd: list[str]) -> int:
        """Process the command during the execution."""
        res = 0
        if cmd[0] == "ls":
            _logger.info(self.ls(cmd[1] if len(cmd) > 1 else "."))
        elif cmd[0] == "cd":
            self.cd(cmd[1] if len(cmd) > 1 else "..")
        elif cmd[0] == "clear":
            self.clear()
        elif cmd[0] == "exit" or cmd[0] == "q":
            res = 1
        else:
            _logger.info("Commandes disponibles: ls, cd <chemin>, exit, q")
        return res
