"""
This module provides the global definitions for the project.

.. currentmodule:: survey_analysis.globals
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from survey_analysis.data import DataContainer
from survey_analysis.settings import Settings

#: A global copy-on-read container for providing the survey data
#: to the analysis functions
dataContainer: DataContainer = DataContainer()

#: The settings storage
settings: Settings = Settings()
