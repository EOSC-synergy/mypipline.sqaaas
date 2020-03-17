"""
A dummy script for testing the function dispatch

.. currentmodule:: survey_analysis.scripts.dummy
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from survey_analysis import globals


def run():
    print("Dummy script called")
    data_frame = globals.dataContainer.raw_data

    if data_frame.empty:
        print("Data frame was empty")
    else:
        print("Data frame was not empty")
