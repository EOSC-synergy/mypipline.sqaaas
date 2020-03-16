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
    manipulate it in any desired way without interfering with other users.
    The initial data frame used is empty.
    """

    def __init__(self):
        """
        Populate the data container with a Pandas data frame.

        parameter: pandas_frame is a data frame containing all data available
        """
        self._raw_data: DataFrame = DataFrame()

    @property
    def empty(self) -> bool:
        """
        Checks if the container holds any data.

        This is considered to be the case if the stored data frame is empty.
        returns: True, if the container is considered empty, False otherwise
        """
        return self._raw_data.empty

    def set_raw_data(self, data_frame: DataFrame):
        """
        Try to set the current raw data frame.

        The data frame stored in the container will only be changed if:
        * The currently stored raw data frame is empty and
        * The provided data frame is not empty
        Otherwise, nothing will be done.
        Attempting to override an already set data frame will result in a
        RuntimeError.

        parameter: data_frame is the new frame to be stored in the container.
        """
        if data_frame.empty:
            return

        if self.empty:
            self._raw_data = data_frame
        else:
            raise RuntimeError("Do not re-assign the global data frame")

    @property
    def raw_data(self) -> DataFrame:
        """
        Provide a deep copy of the whole raw data frame.

        It is recommended to cache this copy as long as it is used.
        returns: A copy of the complete Pandas raw data frame.
        """
        return self._raw_data.copy(deep=True)
