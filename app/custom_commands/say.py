# -*- coding: utf-8 -*-
"""Dummy command."""

import argparse
import logging
from command import Command

_logger: logging.Logger = logging.getLogger(__name__)


class SayCommand(Command):
    """Dummy command."""

    name = "say"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "message", nargs="+", help="Le message à afficher."
        )
        parser.add_argument(
            "--upper", action="store_true", help="Afficher en majuscules."
        )
        parser.add_argument(
            "--prefix", type=str, default="", help="Préfixe à ajouter."
        )

    def handle(self, **options) -> int:
        """Executes the command."""
        message = " ".join(options["message"])
        if options["upper"]:
            message = message.upper()
        _logger.info("%s%s", options["prefix"], message)
        return 0
