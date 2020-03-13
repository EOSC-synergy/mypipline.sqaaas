from typing import Optional

from pandas import DataFrame


class DataContainer(object):
    """
    The data container holds the data read from the command line.
    It can hand out copies of the data frame so the using function can
    manipulate it in any desired way without interfering with other users
    """

    def __init__(self, pandas_frame: DataFrame):
        self._raw_data: DataFrame = pandas_frame

    @property
    def get_raw_data(self) -> DataFrame:
        """
        Provides a deep copy of the whole raw data frame.
        It is recommended to cache this copy as long as it is used.
        returns: A copy of the complete Pandas raw data frame.
        """
        return self._raw_data.copy(deep=True)


# --- Define the global data container ---
globalContainer: Optional[DataContainer] = None


def initialize_global_data(data_frame: DataFrame):
    global globalContainer
    if globalContainer is None:
        globalContainer = DataContainer(data_frame)
    else:
        raise RuntimeError("Do not re-assign the global data frame")
