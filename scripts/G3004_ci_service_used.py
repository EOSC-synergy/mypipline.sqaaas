"""
Analyses question about which Continuous Integration Services are used.

Key questions and findings from only completed data:
* What are the Continuous Integration Services used most frequent?
GitLab CI / 29 %, Jenkins / 15 %, Travis CI / 13 %
* Which percentage of scientists use Continuous Integration Services?
47 %
* Which Continuous Integration Services do Helmholtz scientists need for their
software projects?
GitLab CI / 29 %, Jenkins / 15 %, Travis CI / 13 %

.. currentmodule:: survey_analysis.scripts.G3004_ci_service_used.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from textwrap import wrap
from typing import Dict, List

from pandas import DataFrame

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart
from survey_analysis.question import QuestionCollection

# Reordered answer options of the question without free-text answer.
ci_labels: List[str] = [
    "None",
    "Travis CI",
    "Jenkins",
    "GitLab CI",
    "Circle CI",
    "Atlassian Bamboo",
    "Jetbrains TeamCity",
    "Other"
]

# Short versions of answer options.
short_ci_labels: List[str] = [
    "None",
    "Travis CI",
    "Jenkins",
    "GitLab CI",
    "Circle CI",
    "Atlassian Bamboo",
    "Jetbrains TeamCity",
    "Other CI Services"
]

# Dictionary to map full-length answer options to short versions.
map_long_to_short_ci_labels: Dict[str, str] = {
    ci_labels[0]: short_ci_labels[0],
    ci_labels[1]: short_ci_labels[1],
    ci_labels[2]: short_ci_labels[2],
    ci_labels[3]: short_ci_labels[3],
    ci_labels[4]: short_ci_labels[4],
    ci_labels[5]: short_ci_labels[5],
    ci_labels[6]: short_ci_labels[6],
    ci_labels[7]: short_ci_labels[7],
}


def run():
    """
    Run analysis script for multiple-choice question G3004.

    Which Continuous Integration service do you use to automate building and
    testing your code?

    Answer Options:
    * None
    * Travis CI
    * Jenkins
    * GitLab CI
    * Circle CI
    * Atlassian Bamboo
    * Jetbrains TeamCity
    * Other CI Services
    """
    ci_question_id: str = "G3004"
    ci_question_collection: QuestionCollection = \
        globals.survey_questions[ci_question_id]

    # Output basic information about analysis script.
    print(f"Script G3004_ci_service_used: "
          f"Question {ci_question_id}:\n"
          f"\t{ci_question_collection.text}")
    subquestion_texts: str = []
    for question in ci_question_collection.subquestions:
        subquestion_texts.append(question.text)
    print(f"\t{'; '.join(subquestion_texts)}")

    ci_frame: DataFrame = ci_question_collection.\
        as_dataframe(question_text_as_id=True)

    # Transform "Other CI Services" used to True (answer given) or
    # False (no answer given) values.
    ci_frame_other_bool = ci_frame.replace(["nan", "None"], False)
    ci_frame_other_bool[ci_labels[7]] = \
        ci_frame_other_bool[ci_labels[7]].\
        apply(lambda x: x is not False)

    # Exclude all rows that have all False values in each column
    # (question has not been answered by participant).
    ci_frame_without_all_false = \
        ci_frame_other_bool.loc[
            (ci_frame_other_bool[ci_labels[0]]) |
            (ci_frame_other_bool[ci_labels[1]]) |
            (ci_frame_other_bool[ci_labels[2]]) |
            (ci_frame_other_bool[ci_labels[3]]) |
            (ci_frame_other_bool[ci_labels[4]]) |
            (ci_frame_other_bool[ci_labels[5]]) |
            (ci_frame_other_bool[ci_labels[6]]) |
            (ci_frame_other_bool[ci_labels[7]])]

    # Transform truth values to numerical values for the sake of counting them:
    # False will be NaN, True will be 1.0.
    valid_values_mask = ci_frame_without_all_false.isin([True])
    valid_values_for_counting = \
        ci_frame_without_all_false[valid_values_mask]

    # Reorder columns in DataFrame.
    ci_frame_reindexed = \
        valid_values_for_counting.reindex(ci_labels, axis="columns")
    # Rename columns in DataFrame.
    ci_frame_reindexed_renamed = ci_frame_reindexed.\
        rename(columns=map_long_to_short_ci_labels)

    # Count answers given to each item.
    ci_renamed_counts = ci_frame_reindexed_renamed.count()

    # Transform counts to percentage values.
    ci_renamed_counts_normalized = ci_renamed_counts.\
        apply(lambda x:
              (round(x/ci_frame_without_all_false.shape[0], 4)*100.0))

    # Plot a bar-chart with absolute numbers.
    plot_bar_chart(data_frame=DataFrame(data=ci_renamed_counts),
                   plot_file_name="G3004_ci_services_used_absolute",
                   show_legend=False,
                   x_label_rotation=45,
                   y_axis_label="Absolute Count",
                   plot_title="\n".
                   join(wrap(ci_question_collection.text, width=60)))
    # Plot a bar-chart with percentages.
    plot_bar_chart(data_frame=DataFrame(data=ci_renamed_counts_normalized),
                   plot_file_name="G3004_ci_services_used_percentage",
                   show_legend=False,
                   x_label_rotation=45,
                   round_value_labels_to_decimals=2,
                   y_axis_label="Percentage",
                   plot_title="\n".
                   join(wrap(ci_question_collection.text, width=60)))
