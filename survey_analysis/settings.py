"""
This module provides the definitions for a settings container.

.. currentmodule:: survey_analysis.settings
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from datetime import datetime
from enum import Enum, auto, unique
from pathlib import Path
from typing import List, Set


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

        # Path in which modules to be executed are located which defaults
        # to "scripts" folder.
        self.script_folder: Path = Path("scripts")

        # List of selected module names to be executed which defaults to
        # an empty list for all modules in the module folder.
        self.script_names: List[str] = []

        # The Format in which the data should be output
        self.output_format: OutputFormat = OutputFormat.SCREEN

        # Folder, into which the output file goes
        # if the output format is not screen
        self.output_folder: Path = Path("output")

        if not self.output_folder.exists():
            self.output_folder.mkdir()

        # The date prefix is used to identify the run
        # (e.g. for saving output images)
        self.run_timestamp: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        # Using a set for true_values and false_values to avoid duplicates and
        # because order does not matter
        self.true_values: Set[str] = {
            "True", "Yes", "Y", "On", "1"
            }
        """
        A set of strings to be interpreted as boolean 'True' when
        parsing the input data.
        """

        self.false_values: Set[str] = {
            "False", "No", "N", "Off", "0"
            }
        """
        A set of strings to be interpreted as boolean 'False' when
        parsing the input data.
        """

        # Add upper- and lowercase variants for
        # 'true_values' and 'false_values'
        # Using an extra set because one can not change a set
        # while iterating over it.

        additional_versions: Set[str] = set()
        for item in self.true_values:
            additional_versions.add(item.lower())
            additional_versions.add(item.upper())
        self.true_values.update(additional_versions)

        additional_versions.clear()
        for item in self.false_values:
            additional_versions.add(item.lower())
            additional_versions.add(item.upper())
        self.false_values.update(additional_versions)
