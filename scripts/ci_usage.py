"""
Visualize the CI usage in the different research fields and by team size.

.. currentmodule:: survey_analysis.scripts.ci_usage
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import List

from pandas import DataFrame, Series, concat

from survey_analysis.globals import survey_questions
from survey_analysis.plot import plot_matrix_chart
from survey_analysis.util import cross_reference_sum


def run():
    research_fields: Series = survey_questions["G1002"].as_series()
    team_sizes: Series = survey_questions["G2004"].as_series()
    user_base: Series = survey_questions["G2005"].as_series().sort_values()
    ci_frame: DataFrame = survey_questions["G3004"].as_dataframe(
        question_text_as_id=True)
    # Drop irrelevant lines
    ci_frame.drop(columns=["Circle CI", "Atlassian Bamboo",
                            "Jetbrains TeamCity", "Other"], inplace=True)

    ci_by_team_sizes: DataFrame = cross_reference_sum(ci_frame, team_sizes)
    # Normalize the values by team size
    ci_by_team_sizes = ci_by_team_sizes.apply(lambda x: x/x.sum(), axis=0)

    plot_matrix_chart(ci_by_team_sizes,
                      "ci_by_team_size",
                      plot_title="CI usage by team size",
                      x_label_rotation=45)

    ci_by_research_field: DataFrame = cross_reference_sum(ci_frame, research_fields)
    # Normalize the values per research field
    ci_by_research_field = ci_by_research_field.apply(lambda x: x/x.sum(), axis=0)

    plot_matrix_chart(ci_by_research_field,
                      "ci_by_research_field",
                      plot_title="CI usage per research field",
                      x_label_rotation=45)

    ci_by_user_base: DataFrame = cross_reference_sum(ci_frame, user_base)
    # Normalize the values per research field
    ci_by_user_base = ci_by_user_base.apply(lambda x: x/x.sum(), axis=0)

    plot_matrix_chart(ci_by_user_base,
                      "ci_by_user_base",
                      plot_title="CI usage by user base",
                      x_label_rotation=45)
