# -*- coding: utf-8 -*-
""" Entry point. """

import logging
import os
import sys

from reader.save_reader import read_save


def main(*_, **__) -> int | str | None:
    """Entry point."""
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    return read_save("../saves/gamestate", "../logs/data.json")


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
