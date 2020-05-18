"""
This module provides helper functions.

.. currentmodule:: survey_analysis.util
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
from collections import defaultdict
from inspect import FrameInfo, getmodulename, stack
from pathlib import Path
from typing import Dict, List

from matplotlib import pyplot

from survey_analysis.answer import Answer
from survey_analysis.globals import settings
from survey_analysis.question import (AbstractQuestion, Question,
                                      QuestionCollection)
from survey_analysis.settings import OutputFormat


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


def output_pyplot_image(output_file_stem: str = "") -> None:
    """
    Shorthand function to render pyplot images depending on output settings.

    Use this after construction a pyplot plot to display the plot or render it
    into an image depending on the application settings.
    (Basically instead of pyplot.show() or pyplot.savefig())


    Args:
        output_file_stem:   The stem of the desired filename
                            (without extension).
                            Defaults to an empty string which will prompt the
                            automatic generation of a file name from the date
                            of the run and the module producing the image.
    """
    if settings.output_format == OutputFormat.SCREEN:
        pyplot.show()
        pyplot.close()
        return

    if not output_file_stem:
        # Auto-generate the file stem

        # Get the calling module's name, assuming this function is called from
        # a survey evaluation script
        # Keep in mind that
        # * FrameInfo is a named tuple in which the second entry is the
        #   fully qualified module name
        # * The first element on the stack is this function, the caller is the
        #   second frame
        calling_module_frame: FrameInfo = stack()[1]
        calling_module_name: str = getmodulename(calling_module_frame[1])

        output_file_stem: str = f"{calling_module_name}"

    file_ending: str = settings.output_format.name.lower()
    file_name: str = f"{output_file_stem}.{file_ending}"
    output_subfolder: Path = settings.output_folder/settings.run_timestamp
    output_path: Path = output_subfolder/file_name

    if not output_subfolder.exists():
        output_subfolder.mkdir(parents=True)

    if output_path.exists():
        logging.warning(f"Overriding existing output file {output_path}")

    pyplot.savefig(f"{output_path}")
    pyplot.close()
