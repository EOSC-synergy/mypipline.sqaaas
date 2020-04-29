"""
This module provides helper functions.

.. currentmodule:: survey_analysis.util
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from typing import Dict, List

from .answer import Answer
from .question import Question


def filter_and_group(
        filter_question: Question,
        filter_args,
        group_question: Question
        ) -> Dict[Answer, Dict[str, List[Answer]]]:
    """
    Obtain filtered results grouped by the answers of a question.

    Args:
        filter_question: The question whose given answers are to be filtered.
        filter_args:     Arguments for the filter
        group_question:  The question according to whose given answers the
                         participants are grouped.

    Returns:
        An association of answers of grouped_question to the filtered answers
        of filter_question from these participants.
    """
    grouped_answers = group_question.grouped_by_answer()

    results: Dict[Answer, Dict[str, List[Answer]]] = \
        dict.fromkeys(grouped_answers)

    for answer, participant_ids in grouped_answers.items():
        results[answer] = filter_question.filter_given_answers(
            participant_id=participant_ids
        )

    return results
