# -*- coding: utf-8 -*-
""" cd command. """

import argparse
import logging
from command import Command

_logger: logging.Logger = logging.getLogger(__name__)


class CdCommand(Command):
    """ cd command. """
    name = "cd"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("path", nargs="?", default="..", help="Le chemin.")

    def handle(self, **options) -> int:
        """Executes the command."""
        path: str = options["path"]
        navigation = self.navigator.navigate_to(path.split("/"))
        if navigation:
            self.navigator.current = navigation[0]
            self.navigator.path = navigation[1]
            self.navigator.history = navigation[2]
        else:
            _logger.info("Chemin invalide : %s", path)
        return 0
