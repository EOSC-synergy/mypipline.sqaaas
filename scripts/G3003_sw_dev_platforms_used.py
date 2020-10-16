"""
Analyses question about which SW Dev Platform is used most frequent.

Key questions and findings from only completed data:
* What are the SW Dev Platforms used most frequent?
GitHub.com / 54 %, Self-hosted GitLab / 49 %, GitLab.com / 25 %
* Which percentage of scientists use SW Dev Platforms?
87 %
* Which SW Dev Platforms do Helmholtz scientists need to manage
their software projects?
GitLab / 74 %, GitHub / 59 %

.. currentmodule:: survey_analysis.scripts.G3003_sw_dev_platforms_used.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from textwrap import wrap
from typing import Dict, List

from pandas import DataFrame

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart
from survey_analysis.question import QuestionCollection

# Reordered answer options of the question without free-text answer.
platform_labels: List[str] = [
    "None",
    "GitHub.com",
    "Self-hosted GitHub instance",
    "GitLab.com",
    "Self-hosted GitLab instance",
    "Redmine",
    "Bitbucket (+ other Atlassian tools)",
    "Azure DevOps",
    "Gitea",
    "Gogs",
    "Phabricator",
    "Other"
]

# Short versions of answer options.
short_platform_labels: List[str] = [
    "None",
    "GitHub.com",
    "Self-hosted\nGitHub instance",
    "GitLab.com",
    "Self-hosted\nGitLab instance",
    "Redmine",
    "Bitbucket\n(+ other Atlassian tools)",
    "Azure DevOps",
    "Gitea",
    "Gogs",
    "Phabricator",
    "Other Platforms"
]

# Dictionary to map full-length answer options to short versions.
map_long_to_short_platform_labels: Dict[str, str] = {
    platform_labels[0]: short_platform_labels[0],
    platform_labels[1]: short_platform_labels[1],
    platform_labels[2]: short_platform_labels[2],
    platform_labels[3]: short_platform_labels[3],
    platform_labels[4]: short_platform_labels[4],
    platform_labels[5]: short_platform_labels[5],
    platform_labels[6]: short_platform_labels[6],
    platform_labels[7]: short_platform_labels[7],
    platform_labels[8]: short_platform_labels[8],
    platform_labels[9]: short_platform_labels[9],
    platform_labels[10]: short_platform_labels[10],
    platform_labels[11]: short_platform_labels[11],
}


def run():
    """
    Run analysis script for multiple-choice question G3003.

    Which web-based software development platform do you use?

    Answer Options:
    * None
    * GitHub.com
    * Self-hosted GitHub instance
    * GitLab.com
    * Self-hosted GitLab instance
    * Redmine
    * Bitbucket (+ other Atlassian tools)
    * Azure DevOps
    * Gitea
    * Gogs
    * Phabricator
    * Other Platforms
    """
    platform_question_id: str = "G3003"
    platform_question_collection: QuestionCollection = \
        globals.survey_questions[platform_question_id]

    # Output basic information about analysis script.
    print(f"Script G3003_sw_dev_platforms_used: "
          f"Question {platform_question_id}:\n"
          f"\t{platform_question_collection.text}")
    subquestion_texts: str = []
    for question in platform_question_collection.subquestions:
        subquestion_texts.append(question.text)
    print(f"\t{'; '.join(subquestion_texts)}")

    platform_frame: DataFrame = platform_question_collection.\
        as_dataframe(question_text_as_id=True)

    # Transform "Other Platforms" used to True (answer given) or
    # False (no answer given) values.
    platform_frame_other_bool = platform_frame.replace(["nan", "None"], False)
    platform_frame_other_bool[platform_labels[11]] = \
        platform_frame_other_bool[platform_labels[11]].\
        apply(lambda x: x is not False)

    # Exclude all rows that have all False values in each column
    # (question has not been answered by participant).
    platform_frame_without_all_false = \
        platform_frame_other_bool.loc[
            (platform_frame_other_bool[platform_labels[0]]) |
            (platform_frame_other_bool[platform_labels[1]]) |
            (platform_frame_other_bool[platform_labels[2]]) |
            (platform_frame_other_bool[platform_labels[3]]) |
            (platform_frame_other_bool[platform_labels[4]]) |
            (platform_frame_other_bool[platform_labels[5]]) |
            (platform_frame_other_bool[platform_labels[6]]) |
            (platform_frame_other_bool[platform_labels[7]]) |
            (platform_frame_other_bool[platform_labels[8]]) |
            (platform_frame_other_bool[platform_labels[9]]) |
            (platform_frame_other_bool[platform_labels[10]]) |
            (platform_frame_other_bool[platform_labels[11]])]

    # Transform truth values to numerical values for the sake of counting them:
    # False will be NaN, True will be 1.0.
    valid_values_mask = platform_frame_without_all_false.isin([True])
    valid_values_for_counting = \
        platform_frame_without_all_false[valid_values_mask]

    # Reorder columns in DataFrame.
    platform_frame_reindexed = \
        valid_values_for_counting.reindex(platform_labels, axis="columns")
    # Rename columns in DataFrame.
    platform_frame_reindexed_renamed = platform_frame_reindexed.\
        rename(columns=map_long_to_short_platform_labels)

    # Count answers given to each item.
    platform_renamed_counts = platform_frame_reindexed_renamed.count()

    # Transform counts to percentage values.
    platform_renamed_counts_normalized = platform_renamed_counts.\
        apply(lambda x:
              (round(x/platform_frame_without_all_false.shape[0], 4)*100.0))

    # Plot a bar-chart with absolute numbers.
    plot_bar_chart(data_frame=DataFrame(data=platform_renamed_counts),
                   plot_file_name="G3003_sw_dev_platforms_used_absolute",
                   show_legend=False,
                   x_label_rotation=45,
                   y_axis_label="Absolute Count",
                   plot_title="\n".
                   join(wrap(platform_question_collection.text, width=60)))
    # Plot a bar-chart with percentages.
    plot_bar_chart(data_frame=DataFrame(
                                data=platform_renamed_counts_normalized),
                   plot_file_name="G3003_sw_dev_platforms_used_percentage",
                   show_legend=False,
                   x_label_rotation=45,
                   round_value_labels_to_decimals=2,
                   y_axis_label="Percentage",
                   plot_title="\n".
                   join(wrap(platform_question_collection.text, width=60)))
