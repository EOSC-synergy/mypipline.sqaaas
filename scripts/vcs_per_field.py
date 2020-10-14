"""
Visualize the version control systems used in the different research fields
and by team size.

.. currentmodule:: survey_analysis.scripts.vcs_per_field
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import List

from pandas import DataFrame, Series, concat

from survey_analysis.globals import survey_questions
from survey_analysis.plot import plot_bar_chart
from survey_analysis.util import cross_reference_sum


def run():
    research_fields: Series = survey_questions["G1002"].as_series()
    team_sizes: Series = survey_questions["G2004"].as_series()
    vcs_frame: DataFrame = survey_questions["G3002"].as_dataframe(
        question_text_as_id=True)
    # Drop irrelevant lines
    vcs_frame.drop(
        columns=["Other centralized VCS (e.g., DARCS, SourceSafe)"], inplace=True)
    vcs_frame.drop(columns=[
                   "Other Dezentralized VCS (e.g. Bazaar, BitKeeper, GNU arch, Mercurial, Monotone)"], inplace=True)
    vcs_frame.drop(columns=["Other"], inplace=True)

    vcs_by_team_sizes: DataFrame = cross_reference_sum(vcs_frame, team_sizes)
    # Normalize the values per research field
    vcs_by_team_sizes = vcs_by_team_sizes.apply(lambda x: x/x.sum(), axis=0)

    plot_bar_chart(
        vcs_by_team_sizes.transpose(),
        "vcs_by_team_size",
        stacked=True,
        round_value_labels_to_decimals=2,
        plot_title=f"Portion of Version control systems used compared to the team size",
        x_axis_label="Team size",
        y_axis_label="Percentage",
        legend_location="center left",
        legend_anchor=(1.025, 0.8),
        x_label_rotation=45
    )

    vcs_by_research_field: DataFrame = cross_reference_sum(vcs_frame, research_fields)
    # Normalize the values per research field
    vcs_by_research_field = vcs_by_research_field.apply(lambda x: x/x.sum(), axis=0)

    plot_bar_chart(
        vcs_by_research_field.transpose(),
        "vcs_by_research_field",
        stacked=True,
        round_value_labels_to_decimals=2,
        plot_title=f"Portion of Version control systems used per research field",
        x_axis_label="Research fields",
        y_axis_label="Percentage",
        legend_location="center left",
        legend_anchor=(1.025, 0.8),
        x_label_rotation=45
    )
