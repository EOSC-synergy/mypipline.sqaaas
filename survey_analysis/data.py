"""
This module provides the definitions for a global data container.

The container is meant to serve as the data source for the individual analysis
functions.

.. currentmodule:: survey_analysis.data
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from typing import Optional

from pandas import DataFrame


class DataContainer(object):
    """
    The data container holds the data read from the command line.

    It can hand out copies of the data frame so the using function can
    manipulate it in any desired way without interfering with other users
    """

    def __init__(self, pandas_frame: DataFrame):
        """
        Populate the data container with a Pandas data frame.

        parameter: pandas_frame is a data frame containing all data available
        """
        self._raw_data: DataFrame = pandas_frame

    @property
    def get_raw_data(self) -> DataFrame:
        """
        Provide a deep copy of the whole raw data frame.
        It is recommended to cache this copy as long as it is used.
        returns: A copy of the complete Pandas raw data frame.
        """
        return self._raw_data.copy(deep=True)


# --- Define the global data container ---
globalContainer: Optional[DataContainer] = None


def initialize_global_data(data_frame: DataFrame):
    """
    Set up the global container with a data frame if ther is not one already.

    If the container is already set up, a RuntimeError will be thrown to avoid
    changing the data mid-analysis.
    """
    global globalContainer
    if globalContainer is None:
        globalContainer = DataContainer(data_frame)
    else:
        raise RuntimeError("Do not re-assign the global data frame")
