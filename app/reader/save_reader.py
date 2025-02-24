# -*- coding: utf-8 -*-
""" Save reading. """

import json
import logging
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


def read_save(file_path: str, log_path: str) -> int:
    """Read the save file"""
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
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return DataNavigator(data).run()
