"""
A script for showing coding time distribution

.. currentmodule:: survey_analysis.scripts.time_spend_on_coding_distribution.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

# pipenv run survey_analysis -n community_coding_time_distribution analyze data/results-survey652278_all.csv

import os
from datetime import datetime

import plotnine as p9
from pandas import DataFrame

from survey_analysis import globals
from survey_analysis.question import Question


def run():
    print("Show distribution of time spend on coding per center and average over helmholtz")

    # load question about coding percentage
    question_G2003: Question = globals.survey_questions["G2003"]
    time_coding_percentage_frame: DataFrame = question_G2003.as_dataframe(question_text_as_id=True)
    time_coding_percentage_frame.columns = ['coding_percentage']

    # load question about center
    question_G1003: Question = globals.survey_questions["G1003"]
    tmp = {id: question_G1003.given_answers[id][0].short_text for id in question_G1003.given_answers.keys()}
    helmholtz_center_frame: DataFrame = DataFrame.from_dict(tmp, orient='index')
    helmholtz_center_frame.columns = ['helmholtz_center']

    # # load question about research are
    question_G1002: Question = globals.survey_questions["G1002"]
    tmp = {id: question_G1002.given_answers[id][0].text for id in question_G1002.given_answers.keys()}
    research_area_frame: DataFrame = DataFrame.from_dict(tmp, orient='index')
    research_area_frame.columns = ['research_area']

    # merge all frames
    merged_frame = time_coding_percentage_frame.join(helmholtz_center_frame).join(research_area_frame)

    print('##########')
    print(time_coding_percentage_frame.mean())
    print(time_coding_percentage_frame.std())
    print('##########')

    # create path
    now = datetime.now().strftime("%Y-%m-%d_%H:%m:%S")
    output_path = f'output/{now}'
    os.mkdir(output_path)

    # coding time all
    plot = (p9.ggplot(data=time_coding_percentage_frame,
                      mapping=p9.aes(x='coding_percentage'))
            + p9.geom_bar()
            )

    plot.save(filename=f'{output_path}/time_all.png')

    plot = (p9.ggplot(data=merged_frame.dropna(),
                      mapping=p9.aes(x='helmholtz_center',
                                     y='coding_percentage'))
            + p9.geom_boxplot()
            + p9.theme(
                figure_size=(18, 6)
            )
            # + p9.geom_hline(data=)
            )
    plot.save(filename=f'{output_path}/time_center.png')

    # coding time by research area
    plot = (p9.ggplot(data=merged_frame,
                      mapping=p9.aes(x='research_area',
                                     y='coding_percentage'))
            + p9.geom_boxplot()
            + p9.theme(figure_size=(18, 6))
            )

    plot.save(filename=f'{output_path}/time_area.png')
