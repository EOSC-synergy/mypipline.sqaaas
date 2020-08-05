"""
A dummy script for testing the function dispatch

.. currentmodule:: survey_analysis.scripts.example_institute_count.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import Dict

from pandas import DataFrame, Series

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart, plot_box_chart
from survey_analysis.question import Question


def run():
    # As an example, count how many participants there were for each
    # institution
    question_id: str = "G1003"
    question: Question = globals.survey_questions[question_id]
    print(f"Example Script: "
          f"Counting Answers for Question {question_id}:\n"
          f"\t{question.text}")

    # Replace the series index by the short versions of the answers since the
    # full text does not fit on the plot
    count: Series = question.as_counted_series(use_short_answer=True)

    # Set a proper name for the series, it will become the tick label for the
    # box plot
    count.name = "Count"

    # The plot functions take data frames, so convert the series into one
    frame: DataFrame = DataFrame(count)

    # Generate a box plot and a bar plot
    # The x labels for the bar plot are rotated to make better use of the space
    plot_bar_chart(frame, show_legend=False, x_label_rotation=45)
    plot_box_chart(frame)
