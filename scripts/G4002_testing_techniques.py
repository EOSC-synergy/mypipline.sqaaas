"""
A script to analyze answers given to question G4002.

.. currentmodule:: survey_analysis.scripts.G4002_testing_techniques
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from pathlib import Path
from typing import List

import numpy
from pandas import DataFrame, Series

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart, plot_matrix_chart
from survey_analysis.question import QuestionCollection
from survey_analysis.util import cross_reference_sum, dataframe_value_counts

# Testing techniques used in the survey
testing_techniques: List[str] = [
    "Test automation",
    "Unit testing",
    "Integration testing",
    "System testing",
    "Acceptance testing",
    "Exploratory testing",
    "Behavior driven testing",
    "Usability testing",
    "Performance testing",
    "Regression testing",
    "Static code analysis",
    "Code coverage analysis"]

# Magic values expressing regularity from most to unknown
regularity: List[str] = [
    "Regularly",
    "Sometimes",
    "Never",
    "I do not know what this is."]


def run():
    """
    Analyse question G4002: "What kind of testing practices do you use?".

    This script analyses how regular the given testing techniques are applied
    (question G4002) with respect to the research field of the participant 
    (question G1002).
    The topics displayed in the resulting charts are:
    1) Stacked bar charts of how regular the testing techniques are applied.
    2) Matrix charts of weighted sums of how regular the testing techniques 
    are applied per research field of the participant.
    3) Matrix charts of which testing techniques are unknown per research 
    field of the participant.
    """
    module_name: str = Path(__file__).stem

    print(module_name)

    # Gather the required data
    research_fields: Series = globals.survey_questions["G1002"].as_series()
    research_fields.dropna(inplace=True)
    testing_questions: QuestionCollection = globals.survey_questions["G4002"]
    testing_frame: DataFrame = testing_questions.as_dataframe(
        question_text_as_id=True)

    # Filter out answers which do not match the regularity ratings
    # given by the question at hand and sort the columns in a sensible order.
    valid_values_mask = testing_frame.isin(regularity)
    valid_values = testing_frame[valid_values_mask]
    valid_values = valid_values.reindex(testing_techniques, axis="columns")
    print(len(valid_values.index))

    # Forming an inner join over research_fields and valid_values gives the
    # data for participants that answered both questions. This is then counted
    # per research field for later use
    answered_both = valid_values.join(research_fields, how="inner")
    participants_per_field = answered_both[research_fields.name].value_counts()

    # Count given answers to question Testing Techniques.
    absolute_count: DataFrame = dataframe_value_counts(valid_values)
    relative_count: DataFrame = dataframe_value_counts(valid_values,
                                                       relative_values=True)

    # Create a matrix of weights for the usage
    # TODO Discuss: should potential usage have a weight of 0.1?
    weighted_by_usage = valid_values.replace(
        {regularity[0]: 1.0,  # Technique in regular use
         regularity[1]: 0.5,  # Used sometimes
         regularity[2]: 0.0,  # Technique known, but not used
         regularity[3]: 0.0,  # Technique unknown
         numpy.NaN: 0.0})

    usage_summary: DataFrame = cross_reference_sum(weighted_by_usage,
                                                   research_fields)
    # Normalize the values per research field
    # Careful with the interpretation here!
    # This only highlights prevalence of usage, since multiple answers were
    # possible.
    usage_summary_relative = usage_summary.apply(lambda x: x / x.sum(), axis=0)
    usage_summary_normalized = usage_summary.divide(participants_per_field,
                                                    axis=1)

    weighted_by_non_awareness = valid_values.replace(
        {
            regularity[0]: 0.0,  # Technique in regular use
            regularity[1]: 0.0,  # Used sometimes
            regularity[2]: 0.0,  # Technique known, but not used
            regularity[3]: 1.0,  # Technique unknown
            numpy.NaN: 0.0
            })
    non_awareness: DataFrame = cross_reference_sum(weighted_by_non_awareness,
                                                   research_fields)
    non_awareness_relative = non_awareness.apply(
        lambda x: x / x.sum(), axis=0)
    non_awareness_normalized = non_awareness.divide(participants_per_field,
                                                    axis=1)

    # Plot all the data
    # =================

    question_title = f"{testing_questions.id}: {testing_questions.text}\n"

    # Plot stacked bar charts with testing techniques on the x-axis.
    # Plot absolute numbers.
    plot_bar_chart(
        absolute_count.transpose(),
        "testing_techniques_counts",
        stacked=True,
        round_value_labels_to_decimals=0,
        plot_title=f"{question_title}"
                   f"Absolute answer count",
        x_axis_label="Testing Techniques",
        y_axis_label="Absolute Numbers",
        legend_location="center left",
        legend_anchor=(1.025, 0.8),
        x_label_rotation=45
    )
    # Plot relative numbers.
    plot_bar_chart(
        relative_count.transpose().mul(100),
        "testing_techniques_percentages",
        stacked=True,
        round_value_labels_to_decimals=0,
        plot_title=f"{question_title}"
                   f"Answer percentage distribution",
        x_axis_label="Testing Techniques",
        y_axis_label="Percentages",
        legend_location="center left",
        legend_anchor=(1.025, 0.8),
        x_label_rotation=45
    )

    # Plot matrix charts with research fields on the x-axis and
    # testing techniques on the y-axis.
    # Plot absolute numbers.
    plot_matrix_chart(usage_summary,
                      "testing_techniques_per_field",
                      plot_title=f"{question_title}"
                                 f"Weighted usage per research field",
                      x_label_rotation=45)
    # Plot relative numbers.
    plot_matrix_chart(usage_summary_relative,
                      "testing_techniques_per_field_relative",
                      plot_title=f"{question_title}"
                                 f"Weighted usage per research field "
                                 f"(Relative per field)",
                      x_label_rotation=45)

    # Plot normalized numbers.
    plot_matrix_chart(usage_summary_normalized,
                      "testing_techniques_per_field_normalized",
                      plot_title=f"{question_title}"
                                 f"Weighted usage per research field "
                                 f"(Normalized per participants per field)",
                      x_label_rotation=45)

    # Plot the non-awareness of testing techniques
    plot_matrix_chart(non_awareness,
                      "unknown_testing_techniques_per_field",
                      plot_title=f"{question_title}"
                                 f"Unknown techniques per research field",
                      invert_colors=True,
                      x_label_rotation=45)
    # Plot relative numbers.
    plot_matrix_chart(non_awareness_relative,
                      "unknown_testing_techniques_per_field_relative",
                      plot_title=f"{question_title}"
                                 f"Unknown techniques"
                                 f"(Relative distribution per field)",
                      invert_colors=True,
                      x_label_rotation=45)

    # Plot normalized numbers.
    plot_matrix_chart(non_awareness_normalized,
                      "unknown_testing_techniques_per_field_prevalence",
                      plot_title=f"{question_title}"
                                 f"Unknown techniques"
                                 f"(Normalized per participants per field)",
                      invert_colors=True,
                      x_label_rotation=45)
