"""
Analyses question about which VCS is used most frequent.

Key questions and findings from only completed data:
* What are the VCSs used most frequent?
Git / 86 %, SVN / 20 %
* Which percentage of scientists use VCSs?
91 %
* Which VCSs do Helmholtz scientists need to version control their software?
Git, SVN

.. currentmodule:: survey_analysis.scripts.G3002_vcs_used.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from textwrap import wrap
from typing import Dict, List

from pandas import DataFrame

from survey_analysis import globals
from survey_analysis.plot import plot_bar_chart
from survey_analysis.question import QuestionCollection

# Reordered answer options of the question without free-text answer.
vcs_labels: List[str] = [
    "None",
    "Git",
    "Other Dezentralized VCS "
    "(e.g. Bazaar, BitKeeper, GNU arch, Mercurial, Monotone)",
    "Subversion",
    "CVS",
    "Other centralized VCS "
    "(e.g., DARCS, SourceSafe)",
    "Other"
]

# Short versions of answer options without typo.
short_vcs_labels: List[str] = [
    "None",
    "Git",
    "Other de-centralized\nVCS",
    "Subversion / SVN",
    "Concurrent Versions\nSystem / CVS",
    "Other centralized\nVCS",
    "Other VCS"
]

# Dictionary to map full-length answer options to short versions.
map_long_to_short_vcs_labels: Dict[str, str] = {
    vcs_labels[0]: short_vcs_labels[0],
    vcs_labels[1]: short_vcs_labels[1],
    vcs_labels[2]: short_vcs_labels[2],
    vcs_labels[3]: short_vcs_labels[3],
    vcs_labels[4]: short_vcs_labels[4],
    vcs_labels[5]: short_vcs_labels[5],
    vcs_labels[6]: short_vcs_labels[6],
}


def run():
    """
    Run analysis script for multiple-choice question G3002.

    Which version control systems (VCS) do you use for software development?

    Answer Options:
    * None
    * Git
    * Other de-centralized VCS
    * Subversion / SVN
    * Concurrent Versions System / CVS
    * Other centralized VCS
    * Other VCS
    """
    vcs_question_id: str = "G3002"
    vcs_question_collection: QuestionCollection = \
        globals.survey_questions[vcs_question_id]

    # Output basic information about analysis script.
    print(f"Script G3002_vcs_used: "
          f"Question {vcs_question_id}:\n"
          f"\t{vcs_question_collection.text}")
    subquestion_texts: str = []
    for question in vcs_question_collection.subquestions:
        subquestion_texts.append(question.text)
    print(f"\t{'; '.join(subquestion_texts)}")

    vcs_frame: DataFrame = vcs_question_collection.\
        as_dataframe(question_text_as_id=True)

    # Transform "Other VCS" used to True (answer given) or
    # False (no answer given) values.
    vcs_frame_other_bool = vcs_frame.replace(["nan", "None"], False)
    vcs_frame_other_bool[vcs_labels[6]] = vcs_frame_other_bool[vcs_labels[6]].\
        apply(lambda x: x is not False)

    # Exclude all rows that have all False values in each column
    # (question has not been answered by participant).
    vcs_frame_without_all_false = \
        vcs_frame_other_bool.loc[
            (vcs_frame_other_bool[vcs_labels[0]]) |
            (vcs_frame_other_bool[vcs_labels[1]]) |
            (vcs_frame_other_bool[vcs_labels[2]]) |
            (vcs_frame_other_bool[vcs_labels[3]]) |
            (vcs_frame_other_bool[vcs_labels[4]]) |
            (vcs_frame_other_bool[vcs_labels[5]]) |
            (vcs_frame_other_bool[vcs_labels[6]])]

    # Transform truth values to numerical values for the sake of counting them:
    # False will be NaN, True will be 1.0.
    valid_values_mask = vcs_frame_without_all_false.isin([True])
    valid_values_for_counting = vcs_frame_without_all_false[valid_values_mask]

    # Reorder columns in DataFrame.
    vcs_frame_reindexed = \
        valid_values_for_counting.reindex(vcs_labels, axis="columns")
    # Rename columns in DataFrame.
    vcs_frame_reindexed_renamed = vcs_frame_reindexed.\
        rename(columns=map_long_to_short_vcs_labels)

    # Count answers given to each item.
    vcs_renamed_counts = vcs_frame_reindexed_renamed.count()

    # Transform counts to percentage values.
    vcs_renamed_counts_normalized = vcs_renamed_counts.\
        apply(lambda x:
              (round(x/vcs_frame_without_all_false.shape[0], 4)*100.0))

    # Plot a bar-chart with absolute numbers.
    plot_bar_chart(data_frame=DataFrame(data=vcs_renamed_counts),
                   plot_file_name="G3002_VCSs_used_absolute",
                   show_legend=False,
                   x_label_rotation=45,
                   y_axis_label="Absolute Count",
                   plot_title="\n".
                   join(wrap(vcs_question_collection.text, width=60)))
    # Plot a bar-chart with percentages.
    plot_bar_chart(data_frame=DataFrame(data=vcs_renamed_counts_normalized),
                   plot_file_name="G3002_VCSs_used_percentage",
                   show_legend=False,
                   x_label_rotation=45,
                   round_value_labels_to_decimals=2,
                   y_axis_label="Percentage",
                   plot_title="\n".
                   join(wrap(vcs_question_collection.text, width=60)))
