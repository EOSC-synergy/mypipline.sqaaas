from pandas import DataFrame
from typing import Optional


class DataContainer(object):
    """
    The data container holds the data read from the command line.
    It can hand out copies of the data frame so the using function can
    manipulate it in any desired way without interfering with other users
    """

    def __init__(self, pandas_frame: DataFrame):
        self._raw_data : DataFrame = pandas_frame

    @property
    def get_raw_data(self) -> DataFrame:
        """
        Provides a deep copy of the whole raw data frame.
        It is recommended to cache this copy as long as it is used.
        returns: A copy of the complete Pandas raw data frame.
        """
        return self._raw_data.copy(deep=True)