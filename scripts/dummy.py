"""
A dummy script for testing the function dispatch

.. currentmodule:: survey_analysis.scripts.dummy
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging

from survey_analysis import globals


def run():
    print("Dummy script called")
    data_frame = globals.dataContainer.raw_data

    if data_frame.empty:
        logging.warning("Data frame was empty")
    else:
        logging.info("Data frame was not empty")
