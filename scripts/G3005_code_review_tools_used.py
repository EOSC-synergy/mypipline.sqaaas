"""
Analyses question about which code review tools are used most frequently.

Key questions and findings from only completed data:
* What are the code review tools used most frequently?
GitLab / 40 %, GutHub / 30 %
* Which percentage of scientists use code review tools?
61 %
* Which code review tools do Helmholtz scientists need to manage
their software projects?
GitLab, GutHub

.. currentmodule:: survey_analysis.scripts.G3005_code_review_tools_used.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from textwrap import wrap
from typing import Dict, List

from pandas import DataFrame

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart
from survey_analysis.question import QuestionCollection

# Reordered answer options of the question without free-text answer.
review_labels: List[str] = [
    "None",
    "GitHub",
    "GitLab",
    "Atlassian Crucible",
    "Jetbrains Upsource",
    "Review Board",
    "Other"
]

# Short versions of answer options
short_review_labels: List[str] = [
    "None",
    "GitHub",
    "GitLab",
    "Atlassian Crucible",
    "Jetbrains Upsource",
    "Review Board",
    "Other review tools"
]

# Dictionary to map full-length answer options to short versions.
map_long_to_short_review_labels: Dict[str, str] = {
    review_labels[0]: short_review_labels[0],
    review_labels[1]: short_review_labels[1],
    review_labels[2]: short_review_labels[2],
    review_labels[3]: short_review_labels[3],
    review_labels[4]: short_review_labels[4],
    review_labels[5]: short_review_labels[5],
    review_labels[6]: short_review_labels[6],
}


def run():
    """
    Run analysis script for multiple-choice question G3005.

    Which tools do you use to review your code?

    Answer Options:
    * None
    * GitHub
    * GitLab
    * Atlassian Crucible
    * Jetbrains Upsource
    * Review Board
    * Other review tools
    """
    review_question_id: str = "G3005"
    review_question_collection: QuestionCollection = \
        globals.survey_questions[review_question_id]

    # Output basic information about analysis script.
    print(f"Script G3005_code_review_tools_used: "
          f"Question {review_question_id}:\n"
          f"\t{review_question_collection.text}")
    subquestion_texts: str = []
    for question in review_question_collection.subquestions:
        subquestion_texts.append(question.text)
    print(f"\t{'; '.join(subquestion_texts)}")

    review_frame: DataFrame = review_question_collection.\
        as_dataframe(question_text_as_id=True)

    # Transform "Other review tools" used to True (answer given) or
    # False (no answer given) values.
    review_frame_other_bool = review_frame.replace(["nan", "None"], False)
    review_frame_other_bool[review_labels[6]] = \
        review_frame_other_bool[review_labels[6]].\
        apply(lambda x: x is not False)

    # Exclude all rows that have all False values in each column
    # (question has not been answered by participant).
    review_frame_without_all_false = \
        review_frame_other_bool.loc[
            (review_frame_other_bool[review_labels[0]]) |
            (review_frame_other_bool[review_labels[1]]) |
            (review_frame_other_bool[review_labels[2]]) |
            (review_frame_other_bool[review_labels[3]]) |
            (review_frame_other_bool[review_labels[4]]) |
            (review_frame_other_bool[review_labels[5]]) |
            (review_frame_other_bool[review_labels[6]])]

    # Transform truth values to numerical values for the sake of counting them:
    # False will be NaN, True will be 1.0.
    valid_values_mask = review_frame_without_all_false.isin([True])
    valid_values_for_counting = \
        review_frame_without_all_false[valid_values_mask]

    # Reorder columns in DataFrame.
    review_frame_reindexed = \
        valid_values_for_counting.reindex(review_labels, axis="columns")
    # Rename columns in DataFrame.
    review_frame_reindexed_renamed = review_frame_reindexed.\
        rename(columns=map_long_to_short_review_labels)

    # Count answers given to each item.
    review_renamed_counts = review_frame_reindexed_renamed.count()

    # Transform counts to percentage values.
    review_renamed_counts_normalized = review_renamed_counts.\
        apply(lambda x:
              (round(x/review_frame_without_all_false.shape[0], 4)*100.0))

    # Plot a bar-chart with absolute numbers.
    plot_bar_chart(data_frame=DataFrame(data=review_renamed_counts),
                   plot_file_name="G3005_code_review_tools_used_absolute",
                   show_legend=False,
                   x_label_rotation=45,
                   y_axis_label="Absolute Count",
                   plot_title="\n".
                   join(wrap(review_question_collection.text, width=60)))
    # Plot a bar-chart with percentages.
    plot_bar_chart(data_frame=DataFrame(
                                data=review_renamed_counts_normalized),
                   plot_file_name="G3005_code_review_tools_used_percentage",
                   show_legend=False,
                   x_label_rotation=45,
                   round_value_labels_to_decimals=2,
                   y_axis_label="Percentage",
                   plot_title="\n".
                   join(wrap(review_question_collection.text, width=60)))
