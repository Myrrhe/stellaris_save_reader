# -*- coding: utf-8 -*-
""" clear command. """

import logging
from command import Command

_logger: logging.Logger = logging.getLogger(__name__)


class ClearCommand(Command):
    """ clear command. """
    name = "clear"

    def handle(self, **options) -> int:
        _logger.info("\033c")
