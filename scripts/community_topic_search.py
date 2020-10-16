"""
A script for showing coding time distribution

.. currentmodule:: survey_analysis.scripts.time_spend_on_coding_distribution.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

# pipenv run survey_analysis -n community_topic_search analyze data/results-survey652278_all.csv

import os
from collections import OrderedDict
from datetime import datetime

import matplotlib.pyplot as plt
import pandas
import requests
from wordcloud import STOPWORDS, WordCloud

from survey_analysis.util import question_ids_to_dataframe


def filter_data_frame(answer_data_frame: pandas.DataFrame, filter: dict) -> pandas.DataFrame:
    if 'sort_out_empty' in filter and filter['sort_out_empty']:
        answer_data_frame = answer_data_frame[answer_data_frame['G2001 Series'].notna()]
        answer_data_frame = answer_data_frame[answer_data_frame['G2003[SQ001] Series'].notna()]
        answer_data_frame = answer_data_frame.drop(
            answer_data_frame[(answer_data_frame['G6003[other] Series'] == 'None') &
                              (answer_data_frame['G6004 Series'] == 'None') &
                              (answer_data_frame['G7001 Series'] == 'None')].index)
        answer_data_frame = answer_data_frame.drop(2013)  # spaces as answers
        answer_data_frame = answer_data_frame.drop(811)  # did not answer questions 6003, 6004, 7001
        answer_data_frame = answer_data_frame.drop(443)  # did not answer questions 6003, 6004, 7001

    if 'min_coding_experience' in filter:
        answer_data_frame = answer_data_frame.drop(
            answer_data_frame[answer_data_frame['G2001 Series'] < filter['min_coding_experience']].index)
    if 'max_coding_experience' in filter:
        answer_data_frame = answer_data_frame.drop(
            answer_data_frame[answer_data_frame['G2001 Series'] > filter['max_coding_experience']].index)
    if 'min_dev_time' in filter:
        answer_data_frame = answer_data_frame.drop(
            answer_data_frame[answer_data_frame['G2003[SQ001] Series'] < filter['min_dev_time']].index)
    if 'max_dev_time' in filter:
        answer_data_frame = answer_data_frame.drop(
            answer_data_frame[answer_data_frame['G2003[SQ001] Series'] > filter['max_dev_time']].index)

    return answer_data_frame


def correct_free_texts(answer_data_frame: pandas.DataFrame, question: str) -> dict:
    results = {'word_count': {},
               'full_text': '',
               'word_frequencies': {}}

    # count words in support wishes
    for answer in answer_data_frame.index:
        answer_text: str = answer_data_frame[question][answer].lower()
        # sort out 'None' answers
        if answer_text == 'none':
            continue
        # sort out special characters
        answer_text = answer_text.replace('\n', ' ')
        tmp = ''
        for character in answer_text:
            if character.isalnum():
                tmp += character
            else:
                tmp += ' '
        answer_text = tmp
        # sort word to dict and count them
        for word in answer_text.split(' '):
            if word in results['word_count']:
                results['word_count'][word] += 1
            else:
                results['word_count'][word] = 1
        # add words to full text
        results['full_text'] += ' ' + answer_text

    # remove quirky entries
    meaningless_words = ['software',
                         'development',
                         'scientific',
                         'scientists',
                         'helmholtz',
                         'etc',
                         'code',
                         'programming',
                         'research',
                         'site',
                         'years',
                         'away',
                         'really',
                         'things',
                         'topic',
                         'going',
                         'making',
                         'however',
                         'given',
                         'something',
                         'become',
                         'nearly',
                         'into',
                         'shows'
                         'doing',
                         'having',
                         'getting',
                         'sw',
                         'because',
                         'maybe']
    results['word_count'] = remove_entries(word_count=results['word_count'],
                                           remove_empty=True,
                                           remove_short=1,
                                           remove_numbers=True,
                                           remove_most_common=True,
                                           remove_specific=meaningless_words)

    # order dict
    results['word_count'] = OrderedDict(sorted(results['word_count'].items(), key=lambda x: x[1]))

    # calculate word frequencies
    for word in results['word_count']:
        results['word_frequencies'][word] = results['word_count'][word] / sum(results['word_count'].values())

    return results


def create_wordcloud(data, filename: str):
    fig = plt.figure(figsize=(16, 8))

    if isinstance(data, str):
        # stopwords
        stopwords = set(STOPWORDS)

        words = []
        for stopword in words:
            stopwords.add(stopword)
        stopwords.remove('r')

        wordcloud = WordCloud(max_font_size=500, min_font_size=10,
                              stopwords=stopwords,
                              width=1600,
                              height=800,
                              max_words=100).generate(data)
    elif isinstance(data, dict):
        wordcloud = WordCloud(max_font_size=500, min_font_size=10,
                              width=1600,
                              height=800,
                              max_words=100,
                              ).generate_from_frequencies(data)
    else:
        return
    # Plotting
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # Save to file
    wordcloud.to_file(filename)


def remove_entries(word_count: dict,
                   remove_empty: bool = False,
                   remove_short: int = -1,
                   remove_numbers: bool = False,
                   remove_specific: list = [],
                   remove_most_common: bool = False) -> dict:
    # remove empty entries
    if remove_empty:
        if '' in word_count:
            del word_count['']
    # remove to short values
    if remove_short >= 1:
        tmp = {}
        for key in word_count:
            if len(key) > remove_short:
                tmp[key] = word_count[key]
        word_count = tmp
    # remove numbers
    if remove_numbers:
        tmp = {}
        for key in word_count:
            if not key.isnumeric():
                tmp[key] = word_count[key]
        word_count = tmp
    # remove meaningless entries
    if remove_specific:
        for word in remove_specific:
            if word in word_count:
                del word_count[word]

    # sort out 1000 most common words in english
    if remove_most_common:
        r = requests.get(
            'https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt')
        common_words_list = r.text.split('\n')
        for word in common_words_list:
            if word in word_count:
                del word_count[word]

    return word_count


def analyze(relevant_questions: list, name: str, filter: dict, path: str):
    print(f'##### {name} #####')
    answer_data_frame = question_ids_to_dataframe(relevant_questions)

    print('raw entries: ', answer_data_frame.shape[0])

    # apply filter
    answer_data_frame = filter_data_frame(answer_data_frame, filter)

    print('filtered entries:', answer_data_frame.shape[0])
    # analysis
    print('years of software development experience (mean):', answer_data_frame['G2001 Series'].mean(axis=0))
    print('years of software development experience (median):', answer_data_frame['G2001 Series'].median(axis=0))
    print('years of software development experience (std):', answer_data_frame['G2001 Series'].std(axis=0))
    print('percent worktime spend on coding (mean):', answer_data_frame['G2003[SQ001] Series'].mean(axis=0))
    print('percent worktime spend on coding (median):', answer_data_frame['G2003[SQ001] Series'].median(axis=0))
    print('percent worktime spend on coding (std):', answer_data_frame['G2003[SQ001] Series'].std(axis=0))

    # handle let us know
    G6003_processed_dict = correct_free_texts(answer_data_frame, 'G6003[other] Series')

    # handle support wishes
    G6004_processed_dict = correct_free_texts(answer_data_frame, 'G6004 Series')

    # handle let us know
    G7001_processed_dict = correct_free_texts(answer_data_frame, 'G7001 Series')

    # join previous questions
    joint_processed_dict = {
        'full_text': G6003_processed_dict['full_text'] + ' ' + G6004_processed_dict['full_text'] + ' ' +
                     G7001_processed_dict['full_text'],
        'word_count': G6003_processed_dict['word_count'],
        'word_frequencies': {}}

    for word in G6004_processed_dict['word_count']:
        if word in joint_processed_dict['word_count']:
            joint_processed_dict['word_count'][word] += G6004_processed_dict['word_count'][word]
        else:
            joint_processed_dict['word_count'][word] = G6004_processed_dict['word_count'][word]

    for word in G7001_processed_dict['word_count']:
        if word in joint_processed_dict['word_count']:
            joint_processed_dict['word_count'][word] += G7001_processed_dict['word_count'][word]
        else:
            joint_processed_dict['word_count'][word] = G7001_processed_dict['word_count'][word]

    # calculate word frequencies
    for word in joint_processed_dict['word_count']:
        joint_processed_dict['word_frequencies'][word] = joint_processed_dict['word_count'][word] / \
                                                         sum(joint_processed_dict['word_count'].values())

    create_wordcloud(data=joint_processed_dict['word_frequencies'],
                     filename=f'{path}/wordcloud_from_frequencies_joint_{name}.png')


def run():
    # load data set
    relevant_questions = ['G2001',  # years of software dev experience
                          'G2003[SQ001]',  # percentage of time spend coding
                          'G6003[other]',  # kind of learning
                          'G6004',  # support wishes
                          'G7001']  # let us know

    # Filter params
    filter_all = {'min_dev_time': 0,
                  'max_dev_time': 100,
                  'min_coding_experience': 0,
                  'max_coding_experience': 70,
                  'sort_out_empty': True}
    filter_experts = {'min_dev_time': 0,
                      'max_dev_time': 100,
                      'min_coding_experience': 10,
                      'max_coding_experience': 70,
                      'sort_out_empty': True}
    filter_core_community = {'min_dev_time': 25,
                             'max_dev_time': 100,
                             'min_coding_experience': 0,
                             'max_coding_experience': 70,
                             'sort_out_empty': True}
    filter_peripherals = {'min_dev_time': 0,
                          'max_dev_time': 24.999,
                          'min_coding_experience': 0,
                          'max_coding_experience': 9.999,
                          'sort_out_empty': True}

    # create path
    now = datetime.now().strftime("%Y-%m-%d_%H:%m:%S")
    output_path = f'output/{now}'
    os.mkdir(output_path)

    analyze(relevant_questions=relevant_questions,
            name='all',
            filter=filter_all,
            path=output_path)
    analyze(relevant_questions=relevant_questions,
            name='experts',
            filter=filter_experts,
            path=output_path)
    analyze(relevant_questions=relevant_questions,
            name='core community',
            filter=filter_core_community,
            path=output_path)
    analyze(relevant_questions=relevant_questions,
            name='peripherals',
            filter=filter_peripherals,
            path=output_path)
