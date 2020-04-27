"""
This module provides the definitions for a settings container.

.. currentmodule:: survey_analysis.settings
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from enum import Enum, auto, unique
from pathlib import Path
from typing import List


@unique
class OutputFormat(Enum):
    """An Abstraction of the supported output formats for generated images."""

    SCREEN = auto()
    PDF = auto()
    PNG = auto()
    SVG = auto()

    @staticmethod
    def list_supported() -> str:
        """Generate a string listing the supported output formats."""
        values: List[str] = list(value.name for value in OutputFormat)
        return ", ".join(values)


class Settings(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbosity: int = logging.NOTSET
        self.script_folder: Path = Path("scripts")
        self.output_format: OutputFormat = OutputFormat.SCREEN
