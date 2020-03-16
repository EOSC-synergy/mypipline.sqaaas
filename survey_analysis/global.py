#
# This file contains all global definitions for the project.
#

from typing import Optional
from pandas import DataFrame
from survey_analysis.data import DataContainer

# --- Define the global data container ---
globalContainer: Optional[DataContainer] = None


def initialize_global_data(data_frame: DataFrame):
    """
    Set up the global container with a data frame if there is not one already.

    If the container is already set up, a RuntimeError will be thrown to avoid
    changing the data mid-analysis.
    """
    global globalContainer
    if globalContainer is None:
        globalContainer = DataContainer(data_frame)
    else:
        raise RuntimeError("Do not re-assign the global data frame")
