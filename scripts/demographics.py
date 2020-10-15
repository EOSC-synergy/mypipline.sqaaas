"""
Analysis of the participants demographics.

* Which center do they work for?
* What is their research area?
* What is their distribution regarding research- and SW-development experience?
* How much time do they spend developing software?

.. currentmodule:: survey_analysis.scripts.demographics.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from pandas import DataFrame, Series

from survey_analysis.globals import survey_questions
from survey_analysis.plot import plot_bar_chart, plot_box_chart
from survey_analysis.question import Question
from survey_analysis.util import filter_and_group_series


def run() -> None:
    """
    Analyze the research and development years per research field and center
    """

    print("Running Demographic Analysis")

    # QID: Abbreviation for Question ID
    institute_qid: str = "G1003"
    research_field_qid: str = "G1002"
    research_years_qid: str = "G1001"
    development_years_qid: str = "G2001"

    institute: Question = survey_questions[institute_qid]
    research_field: Question = survey_questions[research_field_qid]
    research_years: Question = survey_questions[research_years_qid]
    development_years: Question = survey_questions[development_years_qid]

    institute_series: Series = institute.as_series(
        use_short_answer=True)
    research_field_series: Series = research_field.as_series(
        use_short_answer=True)
    institute_count: Series = institute.as_counted_series(
        use_short_answer=True)
    research_field_count = research_field.as_counted_series(
        use_short_answer=True)
    research_years_series: Series = research_years.as_series()
    development_years_series: Series = development_years.as_series()

    plot_bar_chart(DataFrame(institute_count),
                   plot_file_name="participants_per_institute",
                   plot_title=f"Participants per Institute "
                              f"(n={institute_count.sum()})",
                   show_legend=False,
                   x_label_rotation=45)

    plot_bar_chart(DataFrame(research_field_count),
                   plot_file_name="participants_per_research_field",
                   plot_title=f"Participants per Research Field"
                              f"(n={research_field_count.sum()})",
                   show_legend=False,
                   x_label_rotation=45)

    research_per_institute: DataFrame = filter_and_group_series(
        base_data=research_years_series,
        group_by=institute_series,
        min_value=0,
        max_value=70
        )

    development_per_institute: DataFrame = filter_and_group_series(
        base_data=development_years_series,
        group_by=institute_series,
        min_value=0,
        max_value=70
        )

    research_per_field: DataFrame = filter_and_group_series(
        base_data=research_years_series,
        group_by=research_field_series,
        min_value=0,
        max_value=70)

    development_per_field: DataFrame = filter_and_group_series(
        base_data=development_years_series,
        group_by=research_field_series,
        min_value=0,
        max_value=70)

    # Report the n-values for completeness
    print("--- n-values for box plots")
    print(DataFrame({
        "Research": research_per_institute.count(axis=0),
        "Development": development_per_institute.count(axis=0)
        }))
    print(DataFrame({
        "Research": research_per_field.count(axis=0),
        "Development": development_per_field.count(axis=0)
        }))
    print("---")

    research_per_institute.rename(columns=lambda x: "Research " + str(x),
                                  inplace=True)
    development_per_institute.rename(columns=lambda x: "Development " + str(x),
                                     inplace=True)

    plot_box_chart(data_frames=[research_per_institute,
                                development_per_institute],
                   plot_file_name="research_years_per_institution",
                   plot_title="Years of Experience by Institute",
                   x_label_rotation=45,
                   y_axis_label="Years in Experience")

    research_per_field.rename(columns=lambda x: "Research " + str(x),
                              inplace=True)
    development_per_field.rename(columns=lambda x: "Development " + str(x),
                                 inplace=True)

    plot_box_chart(data_frames=[research_per_field, development_per_field],
                   plot_file_name="years_per_field",
                   plot_title="Years of Experience by Research Field",
                   x_label_rotation=45,
                   y_axis_label="Years of Experience")
