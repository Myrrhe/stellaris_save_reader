# -*- coding: utf-8 -*-
"""The base command class."""

from abc import ABC, abstractmethod
import argparse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_navigator import DataNavigator


class Command(ABC):
    """Command class."""

    name: str

    def __init__(self, navigator: "DataNavigator") -> None:
        self.navigator = navigator

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Adds arguments to the ArgumentParser"""

    @abstractmethod
    def handle(self, **options) -> int:
        """Executes the command with the analyzed options."""
