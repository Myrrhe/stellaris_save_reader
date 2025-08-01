# -*- coding: utf-8 -*-
"""A class to navigate a data structure."""

import argparse
import importlib
import logging
import pkgutil
import readline
from typing import Any, Optional
from command import Command

_logger: logging.Logger = logging.getLogger(__name__)


class DataNavigator:
    """A class to navigate a data structure."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.root = data
        self.current = data
        self.history = []
        self.path = ["/"]
        self.commands: dict[str, Command] = {}
        self.load_custom_commands("commands")
        self.load_custom_commands("custom_commands")

    def load_custom_commands(self, package_name: str) -> None:
        """Dynamically imports all commands from the package."""
        package = importlib.import_module(package_name)
        for _, modname, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package_name}.{modname}")
            for attr in dir(module):
                obj = getattr(module, attr)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, Command)
                    and obj is not Command
                ):
                    instance = obj(self)
                    self.commands[instance.name] = instance

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
        if not cmd:
            return 0
        command_name = cmd[0]
        args = cmd[1:]

        if command_name in ("exit", "q"):
            return 1

        command = self.commands.get(command_name)
        if command:
            parser = argparse.ArgumentParser(prog=command_name)
            command.add_arguments(parser)
            try:
                options = parser.parse_args(args)
                return command.handle(**vars(options))
            except SystemExit:
                # argparse calls sys.exit(), which we want to avoid
                return 0
        else:
            print(f"Commande inconnue: {command_name}")
            return 0
