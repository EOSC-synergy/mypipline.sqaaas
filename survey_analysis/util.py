"""
This module provides helper functions.

.. currentmodule:: survey_analysis.util
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from collections import defaultdict
from typing import Dict, List

from pandas import DataFrame

from survey_analysis.answer import Answer
from survey_analysis.question import (AbstractQuestion, Question,
                                      QuestionCollection)


def filter_and_group(
        filter_question: Question,
        group_question: Question,
        **filter_args
        ) -> Dict[Answer, Dict[str, List[Answer]]]:
    """
    Obtain filtered results grouped by the answers of a question.

    Args:
        filter_question: The question whose given answers are to be filtered.
        group_question:  The question according to whose given answers the
                         participants are grouped.
        filter_args:     Arguments passed to filter.

    Returns:
        An association of answers of grouped_question to the filtered answers
        of filter_question from these participants.
    """
    grouped_answers = group_question.grouped_by_answer()

    results: Dict[Answer, Dict[str, List[Answer]]] = defaultdict(dict)

    for answer, participant_ids in grouped_answers.items():
        filter_args['participant_id'] = participant_ids
        results[answer] = filter_question.filter_given_answers(
            **filter_args
        )

    return results


def get_free_text_subquestion(
        question: QuestionCollection,
        free_text_question_id: str = 'other'
        ) -> Question:
    """
    Get the subquestion of QuestionCollection that asks for free text answers.

    Args:
        question: QuestionCollection, in which the sub-question for free text
                  answers is searched

    Returns:
        A sub-question that asks for custom free text answers.
    """
    assert question.has_subquestions, \
        "QuestionCollection should have subquestions, but didn't"

    return next(
        (
            subquestion
            for subquestion in question.subquestions
            if subquestion.id == f"{question.id}[{free_text_question_id}]"
        ),
        None
    )


def get_given_free_text_answers(
        abstract_question: AbstractQuestion
        ) -> Dict[str, Answer]:
    """
    Obtain valid free text answers of a Question.

    Args:
        abstract_question: A Question or QuestionCollection whose free text
        answers are to be determined.

    Returns:
        An association of participant IDs to the free text answers from these
        participants. Only participants for which free text answers were found
        are included in the results.
    """
    if isinstance(abstract_question, QuestionCollection):
        question = get_free_text_subquestion(abstract_question)
    elif isinstance(abstract_question, Question):
        question = abstract_question
    else:
        return {}

    return {
        # it is assumed that only one free text answer is given to a question
        participant_id: list_of_answers[0]
        for participant_id, list_of_answers in question.given_answers.items()
        if list_of_answers[0].text != 'nan'
    }


def dataframe_value_counts(dataframe: DataFrame,
                           relative_values: bool = False,
                           drop_nans: bool = True) -> DataFrame:
    """
    Count how often a unique value appears in each column of a data frame.

    Args:
        dataframe:          The data frame of which the values shall be counted
        relative_values:    Instead of absolute counts fill the cells with
                            their relative contribution to the column total
        drop_nans:          Whether to remove the NaN value count.
                            Defaults to True

    Returns:
        A new data frame with the same columns as the input.
        The index is changed to represent the unique values and the cell
        contain the count of the unique values in the given column.
    """
    new_frame: DataFrame = DataFrame([
        dataframe[column].value_counts(
            normalize=relative_values,
            dropna=drop_nans)
        for column in dataframe.columns
        ])
    new_frame.fillna(0, inplace=True)
    new_frame = new_frame.transpose()

    return new_frame
