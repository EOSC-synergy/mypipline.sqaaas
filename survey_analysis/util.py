"""
This module provides helper functions.

.. currentmodule:: survey_analysis.util
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from collections import defaultdict
from typing import Dict, List

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
