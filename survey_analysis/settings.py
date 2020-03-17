"""
This module provides the definitions for a settings container.

.. currentmodule:: survey_analysis.settings
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from pathlib import Path


class Settings(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbosity: int = logging.NOTSET
        self.script_folder: Path = Path("scripts")
