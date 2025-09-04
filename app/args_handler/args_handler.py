# -*- coding: utf-8 -*-
""" A class for the main input parameters. """

import argparse
import io
import logging
from typing import Optional

_logger: logging.Logger = logging.getLogger(__name__)


class ArgsHandler:
    """A class for the main input parameters."""

    main_args: Optional["ArgsHandler"] = None

    def __init__(self, *args) -> None:
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Script permettant lire un fichier de sauvegarde pour Stellaris"
        )
        self.parser.add_argument(
            "file", nargs="?", default="saves/gamestate", help="File"
        )

        self.parsed_args: argparse.Namespace
        try:
            self.parsed_args = self.parser.parse_args(args)
        except SystemExit as e:
            if e.code != 0:
                _logger.error("Code d'erreur: %d", e.code)
            raise e

    def get_usage(self) -> str:
        """Get a string that show how the script can be used."""
        usage_output = io.StringIO()
        self.parser.print_usage(usage_output)
        return usage_output.getvalue().rstrip()

    def __repr__(self) -> str:
        return f"""[{
            ", ".join(f"{k}: {v}" for k, v in vars(self.parsed_args).items())
        }]"""
