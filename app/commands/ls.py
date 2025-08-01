# -*- coding: utf-8 -*-
""" ls command. """

import argparse
import logging
from command import Command

_logger: logging.Logger = logging.getLogger(__name__)


class LsCommand(Command):
    """ ls command. """
    name = "ls"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("path", nargs="?", default=".", help="Le chemin.")

    def handle(self, **options) -> int:
        path: str = options.get("path", ".")

        res = ""
        navigation = self.navigator.navigate_to(path.split("/"))
        if navigation:
            current = navigation[0]
            if isinstance(current, dict):
                res = "  ".join(current.keys())
            elif isinstance(current, list):
                res = "  ".join(str(i) for i in range(len(current)))
            else:
                res = f"Valeur: {current}"
        else:
            res = f"Chemin invalide : {path or '.'}"

        _logger.info(res)
        return 0
