"""
This module provides the global definitions for the project.

.. currentmodule:: survey_analysis.data
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from pandas import DataFrame

from survey_analysis.data import DataContainer

#: A global copy-on-read container for providing the survey data
#: to the analysis functions
dataContainer: DataContainer = DataContainer()
