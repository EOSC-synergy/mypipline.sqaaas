"""
A dummy script for testing the plot module.

.. currentmodule:: survey_analysis.scripts.example_plotting_stacked_bar_chart
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from pathlib import Path

from pandas import DataFrame

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart
from survey_analysis.question import QuestionCollection
from survey_analysis.util import dataframe_value_counts


def run():
    """Create plots of type stacked bar chart."""
    module_name: str = Path(__file__).stem

    print(module_name)

    question_collection: QuestionCollection = globals.survey_questions["G4002"]
    as_frame: DataFrame = question_collection.as_dataframe(
        question_text_as_id=True)

    absolute_count: DataFrame = dataframe_value_counts(as_frame)
    relative_count: DataFrame = dataframe_value_counts(as_frame,
                                                       relative_values=True)

    plot_bar_chart(
        absolute_count.transpose(),
        module_name + "_counts",
        stacked=True,
        plot_title=f"{question_collection.id}: {question_collection.text}",
        x_axis_label="Testing Techniques",
        y_axis_label="Absolute Numbers",
        legend_location="center left",
        legend_anchor=(1.025, 0.8)
    )

    plot_bar_chart(
        relative_count.transpose().mul(100),
        module_name + "_percentages",
        stacked=True,
        plot_title=f"{question_collection.id}: {question_collection.text}",
        x_axis_label="Testing Techniques",
        y_axis_label="Percentages",
        legend_location="center left",
        legend_anchor=(1.025, 0.8)
    )
