"""
Visualize the programming languages used in the different research fields

.. currentmodule:: survey_analysis.scripts.language_per_field
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import List

from pandas import DataFrame, Series, concat

from survey_analysis.globals import survey_questions
from survey_analysis.plot import plot_matrix_chart
from survey_analysis.util import cross_reference_sum


def run():
    research_fields: Series = survey_questions["G1002"].as_series()
    languages_frame: DataFrame = survey_questions["G3001"].as_dataframe(
        question_text_as_id=True)
    languages_frame.drop(columns=["Other"], inplace=True)

    summary: DataFrame = cross_reference_sum(languages_frame, research_fields)

    # Normalize the values per research field
    normalized_summary = summary.apply(lambda x: x/x.sum(), axis=0)

    plot_matrix_chart(summary,
                      "programming_language_per_research_field",
                      x_label_rotation=45)
    plot_matrix_chart(normalized_summary,
                      "programming_language_per_research_field_normalized",
                      x_label_rotation=45)
