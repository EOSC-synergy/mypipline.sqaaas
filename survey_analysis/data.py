"""
This module provides the definitions for a data container.

The container is meant to serve as the data source for the individual analysis
functions.

.. currentmodule:: survey_analysis.data
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from pandas import DataFrame


class DataContainer(object):
    """
    The data container holds the data read from the command line.

    It can hand out copies of the data frame so the using function can
    manipulate it in any desired way without interfering with other users
    """

    def __init__(self, pandas_frame: DataFrame = DataFrame()):
        """
        Populate the data container with a Pandas data frame.

        parameter: pandas_frame is a data frame containing all data available
        """
        self._raw_data: DataFrame = pandas_frame

    @property
    def empty(self) -> bool:
        return self._raw_data.empty

    @property
    def get_raw_data(self) -> DataFrame:
        """
        Provide a deep copy of the whole raw data frame.

        It is recommended to cache this copy as long as it is used.
        returns: A copy of the complete Pandas raw data frame.
        """
        return self._raw_data.copy(deep=True)
