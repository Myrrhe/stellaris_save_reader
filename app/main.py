# -*- coding: utf-8 -*-
""" Entry point. """

import json
import logging
import os
import sys
from typing import Any

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskID,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from data_navigator import DataNavigator
from utils import FileParser
from utils.utils import count_char_line_file

_logger: logging.Logger = logging.getLogger(__name__)


def main(*_, **__) -> int | str | None:
    """Entry point."""
    res: int = 0
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

    file_path: str = "../saves/gamestate"

    _, nb_char = count_char_line_file(file_path)

    data: dict[Any, Any] = {}
    with Progress(
        "[progress.description]{task.description}",
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        BarColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task: TaskID = progress.add_task(
            "[cyan]Traitement en cours...",
            start=True,
            total=nb_char,
        )
        data = FileParser(file_path).parse_large_file_character_by_character(
            progress, task
        )
    with open("logs/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    navigator: DataNavigator = DataNavigator(data)
    res = navigator.run()
    return res


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
