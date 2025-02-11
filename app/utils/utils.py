# -*- coding: utf-8 -*-
""" Miscellaneous functions. """


def count_char_line_file(path: str) -> tuple[int, int]:
    """Count the number of line and number of char of a file."""
    with open(path, "r", encoding="utf-8") as f:
        nb_line = sum(1 for _ in f)
        f.seek(0)
        nb_char = sum(len(ligne) for ligne in f)

    return nb_line, nb_char
