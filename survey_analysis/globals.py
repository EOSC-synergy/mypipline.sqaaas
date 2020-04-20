"""
This module provides the global definitions for the project.

.. currentmodule:: survey_analysis.globals
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import Dict

from survey_analysis.data import DataContainer
from survey_analysis.question import AbstractQuestion
from survey_analysis.settings import Settings

#: A global copy-on-read container for providing the survey data
#: to the analysis functions
dataContainer: DataContainer = DataContainer()

#: The settings storage
settings: Settings = Settings()

#: All the survey questions and their associated answers
survey_questions: Dict[str, AbstractQuestion] = {}
