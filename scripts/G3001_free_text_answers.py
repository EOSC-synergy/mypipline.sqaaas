"""
A script for analyze free text answer of G3001.

.. currentmodule:: survey_analysis.scripts.research_center_filter
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
from collections import Counter

import click
import spacy
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from survey_analysis import globals
from survey_analysis.plot import _output_pyplot_image
from survey_analysis.question import Question, QuestionCollection
from survey_analysis.util import (get_free_text_subquestion,
                                  get_given_free_text_answers)


def run():
    """
    Obtain G3001 free text answers and plot their frequencies in a bar chart.
    """
    click.echo(f"Start free text analysis for Question G3001 ..")

    question: QuestionCollection = globals.survey_questions['G3001']
    assert question.has_subquestions
    click.echo(f"{question.text}")

    # obtain the sub-question with free text answers
    free_text_subquestion: Question = get_free_text_subquestion(question)
    assert type(free_text_subquestion) is Question
    assert 'other' in free_text_subquestion.id
    free_text_answers = get_given_free_text_answers(question)

    # load language model
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        click.echo("Downloading spaCy language model..")
        from spacy.cli import download
        download('en_core_web_sm')
        nlp = spacy.load('en_core_web_sm')

    token_list = []

    # tokenize free text answer, remove punctuation + stopwords
    for _, answer in free_text_answers.items():
        doc = nlp(answer.text)
        for token in doc:
            lexeme = nlp.vocab[token.text]
            if token.is_punct:
                logging.debug(f"Remove punctuation: '{token.text}'")
                continue
            if lexeme.is_stop:
                logging.debug(f"Remove stop word: '{token.text}'")
                continue

            logging.debug(f"Adding token '{token.text}'")
            token_list.append(str(token.text.lower()))

    # merge 'bash' + 'shell' answers since it means the same
    token_list = [
        'bash / shell'
        if (token == 'bash') or (token == 'shell') else token
        for token in token_list
    ]

    logging.debug(f"Token list:\n{token_list}")
    token_counts = Counter(token_list)
    logging.debug(f"{token_counts}")

    min_frequency = 3
    # unpack list of tupels
    tokens, frequencies = zip(*[
        pair for pair in token_counts.most_common()
        if pair[1] >= min_frequency
    ])

    plt.bar(range(len(tokens)), frequencies)
    plt.title("G3001: Programming languages - free text aswers")
    plt.ylabel("# of given answers")
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(range(len(tokens)), tokens, rotation=70)
    # prevent xlabel cut off
    plt.tight_layout()

    _output_pyplot_image()
