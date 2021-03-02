"""
A script for showing coding time distribution

.. currentmodule:: survey_analysis.scripts.time_spend_on_coding_distribution.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

# pipenv run survey_analysis -f PNG -n global_descriptive_statistics analyze data/results-survey652278_all.csv

from pathlib import Path

import yaml
from numpy import float64
from pandas import DataFrame, Index
from tabulate import tabulate

from survey_analysis.globals import settings
from survey_analysis.plot import plot_bar_chart
from survey_analysis.util import question_ids_to_dataframe


def get_descriptive_statistics(
    data: DataFrame, question_id: str
) -> (float64, float64, float64, float64, float64):
    mean = data[question_id].mean()
    std = data[question_id].std()
    median = data[question_id].median()
    min = data[question_id].min()
    max = data[question_id].max()

    return max, mean, median, min, std


def run():
    print("Generating descriptive statistics")

    numerical_questions = {
        "G1001 Series": "research experience (years)",
        "G2001 Series": "software development experience (years)",
        "G2003[SQ001] Series": "work time spend on software development (percentage)",
    }

    data: DataFrame
    data = question_ids_to_dataframe()

    with open("metadata/HIFIS_Software_Survey_2020_Questions.yml") as meta_yml:
        meta = yaml.load(meta_yml, Loader=yaml.FullLoader)

    # create output path
    output_path: Path = settings.output_folder / settings.run_timestamp
    if not output_path.exists():
        output_path.mkdir(parents=True)

    # handle numerical questions
    results_table = []

    for question in numerical_questions:
        max, mean, median, min, std = get_descriptive_statistics(data, question)
        results_table.append(
            [numerical_questions[question], min, max, median, mean, std]
        )

    with open(f"{output_path}/descriptive_statistics.md", "a+") as md_tables:
        md_tables.write(
            tabulate(
                results_table,
                ["Question", "min", "max", "median", "mean", "std"],
                tablefmt="github",
            )
        )

    # handle nominal questions

    # G2001
    question = "G1002"
    column_name = f"{question} Series"
    short_description = "research field"

    # Get names of indexes for which column question has value 'nan'
    indexNames = data[data[column_name] == "nan"].index
    # Delete these row indexes from dataFrame
    question_data = data.drop(indexNames, inplace=False)

    # get total number of answers
    answer_count = question_data.shape[0]

    # group by answer
    question_data_grouped = question_data[column_name].value_counts().to_frame()

    # convert to relative values in %
    question_data_grouped_relative = question_data_grouped.div(answer_count).mul(100)

    # plot results
    plot_bar_chart(
        question_data_grouped_relative,
        short_description,
        stacked=False,
        round_value_labels_to_decimals=2,
        plot_title=short_description,
        x_axis_label="Research Area",
        y_axis_label="Percentages",
        show_legend=False,
        x_label_rotation=45,
        ylim=[0, 100],
    )

    # G2001
    question = "G1003"
    column_name = f"{question} Series"
    short_description = "research center"

    # Get names of indexes for which column question has value 'nan'
    indexNames = data[data[column_name] == "nan"].index
    # Delete these row indexes from dataFrame
    question_data = data.drop(indexNames, inplace=False)

    # get total number of answers
    answer_count = question_data.shape[0]

    # group by answer
    question_data_grouped = question_data[column_name].value_counts().to_frame()

    # convert to relative values in %
    question_data_grouped_relative = question_data_grouped.div(answer_count).mul(100)

    old_index = question_data_grouped_relative.index
    new_index = []

    centers = meta[2]["answers"]

    for center in old_index:
        if center == "None":
            new_index.append("(Unknown)")
            continue
        for tmp in centers:
            if tmp["text"] == center:
                new_index.append(tmp["short-text"])
                break
    new_index = Index(new_index)

    question_data_grouped_relative = question_data_grouped_relative.set_index(
        [new_index]
    )

    # plot results
    plot_bar_chart(
        question_data_grouped_relative,
        short_description,
        stacked=False,
        round_value_labels_to_decimals=2,
        plot_title=short_description,
        x_axis_label="Research Center",
        y_axis_label="Percentages",
        show_legend=False,
        x_label_rotation=45,
        ylim=[0, 100],
    )

    # G2002
    questions = {
        "G2002[SQ001]": "edu core part",
        "G2002[SQ002]": "cours during edu",
        "G2002[SQ003]": "cours in research org",
        "G2002[SQ004]": "carpentry workshop",
        "G2002[SQ005]": "colleagues helped me",
        "G2002[SQ006]": "by myself",
    }

    column_names = [f"{q} Series" for q in questions]
    short_description = "prior education"

    # get question specifi columns
    question_data = data[column_names]

    # get total number of answers
    answer_count = question_data.shape[0]

    # group by answer
    question_data_grouped = None
    for column in column_names:
        if question_data_grouped is None:
            question_data_grouped = question_data[column].value_counts().to_frame()
        else:
            question_data_grouped = question_data_grouped.join(
                question_data[column].value_counts().to_frame()
            )

    question_data_grouped = question_data_grouped.transpose()

    # convert to relative values in %
    question_data_grouped_relative = question_data_grouped.div(answer_count).mul(100)

    new_index = Index(questions.values())

    question_data_grouped_relative = question_data_grouped_relative.set_index(
        [new_index]
    )

    question_data_grouped_relative = question_data_grouped_relative.rename(
        columns={False: "No", True: "Yes"}
    )

    question_data_grouped_relative = question_data_grouped_relative.reindex(
        columns=["Yes", "No"]
    )

    # plot results
    plot_bar_chart(
        question_data_grouped_relative,
        short_description,
        stacked=True,
        round_value_labels_to_decimals=2,
        plot_title=short_description,
        x_axis_label="Prior Education",
        y_axis_label="Percentages",
        show_legend=True,
        x_label_rotation=45,
        legend_location="center left",
        legend_anchor=(1.025, 0.8),
        ylim=[0, 100],
    )
