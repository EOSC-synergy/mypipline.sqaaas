"""
A dummy script for testing the plot module.

.. currentmodule:: survey_analysis.scripts.example_plotting_stacked_bar_chart
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from pathlib import Path
from typing import Dict

from pandas import DataFrame, concat

from survey_analysis import globals
from survey_analysis.plot import plot_as_stacked_bar_chart
from survey_analysis.question import QuestionCollection


def run():
    """Create plots of type stacked bar chart."""
    module_name: str = Path(__file__).stem

    print(module_name)

    question_collection: QuestionCollection = globals.survey_questions["G4002"]

    mapping: Dict[str, str] = {
        sub_question.id: sub_question.text
        for sub_question in question_collection.subquestions
    }

    sub_data_frame: DataFrame = \
        globals.dataContainer.raw_data.\
        loc[:,
            question_collection.subquestions[0].id:
            question_collection.subquestions[-1].id]

    data_frame: DataFrame
    column_id: str
    for column_id in sub_data_frame:
        if column_id == question_collection.subquestions[0].id:
            data_frame = DataFrame(sub_data_frame.loc[:, column_id].
                                   value_counts().to_frame(column_id))
        else:
            data_frame = \
                concat([data_frame,
                        sub_data_frame.loc[:, column_id].value_counts()],
                       axis=1)

    data_frame_transposed: DataFrame = \
        data_frame.rename_axis('answers').transpose()

    data_frame_transposed = data_frame_transposed.rename(index=mapping)

    plot_as_stacked_bar_chart(
        data_frame_transposed,
        module_name + "_counts",
        plot_title=f"{question_collection.id}: {question_collection.text}",
        x_axis_label="Testing Techniques",
        y_axis_label="Absolute Numbers",
        legend_location="center left",
        legend_anchor=(1.025, 0.8)
    )

    data_frame: DataFrame
    column_id: str
    for column_id in sub_data_frame:
        if column_id == question_collection.subquestions[0].id:
            data_frame = DataFrame(sub_data_frame.loc[:, column_id].
                                   value_counts(normalize=True, dropna=True).
                                   mul(100).to_frame(column_id))
        else:
            data_frame = concat(
                [data_frame,
                 sub_data_frame.loc[:, column_id].
                    value_counts(normalize=True, dropna=True).mul(100)],
                axis=1)

    data_frame_transposed: DataFrame = \
        data_frame.rename_axis('answers').transpose()

    data_frame_transposed = data_frame_transposed.rename(index=mapping)

    plot_as_stacked_bar_chart(
        data_frame_transposed,
        module_name+"_percentages",
        plot_title=f"{question_collection.id}: {question_collection.text}",
        x_axis_label="Testing Techniques",
        y_axis_label="Percentages",
        legend_location="center left",
        legend_anchor=(1.025, 0.8)
    )
