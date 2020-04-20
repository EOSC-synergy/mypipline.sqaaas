#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides the definitions for survey metadata.

Survey metadata given in a YAML file is transformed into a dictionary.

.. currentmodule:: survey_analysis.metadata
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import yaml

from survey_analysis import globals

from .answer import Answer
from .data import DataContainer
from .question import Question, QuestionCollection

# The YAML dictionary has a recursive type
YamlDict = Dict[str, Optional[Union[str, "YamlDict"]]]

# This would be cooler as an enum
# How to do that in an elegant way with minimal overhead?
KEYWORD_QUESTIONS: str = "questions"
KEYWORD_ANSWERS: str = "answers"
KEYWORD_ID: str = "id"
KEYWORD_TEXT: str = "text"


def parse_question(content: YamlDict,
                   collection_id: Optional[str] = None) -> Question:
    """
    Parse a Question object from YAML.

    Args:
        content:        The YAML representation as a dictionary
        collection_id:  (Optional) If the question is part of a question
                        collection, this is the ID of the collection as it will
                        be part of the question ID.
                        Otherwise, just default to None.

    Returns:
        A newly constructed Question object. It will automatically be added to
        globals.survey_questions
    """
    assert KEYWORD_ID in content
    assert KEYWORD_TEXT in content

    question_id: str = content.get(KEYWORD_ID)

    if collection_id:
        question_id = collection_id + "[" + question_id + "]"

    question_text: str = content.get(KEYWORD_TEXT)
    predefined_answers: List[Answer] = []

    # Check for predefined answers
    if KEYWORD_ANSWERS in content and content[KEYWORD_ANSWERS]:
        answers_yaml: Dict[str, str] = content[KEYWORD_ANSWERS]
        answer_id: str
        for answer_id in answers_yaml:
            answer_text: Optional[str] = answers_yaml[answer_id]
            new_answer: Answer = Answer(answer_id, answer_text)
            predefined_answers.append(new_answer)

    new_question: Question = Question(question_id, question_text,
                                      predefined_answers)
    logging.debug(f"Parsed question {new_question}")

    # Put the newly parsed object into the global dictionary
    globals.survey_questions[question_id] = new_question
    return new_question


def parse_question_collection(content: YamlDict) -> None:
    """
    Parse a Question Collection object from YAML.

    Args:
        content:        The YAML representation as a dictionary

    Returns:
        A newly constructed Question Collection object.
        It will automatically be added to globals.survey_questions
    """
    # TODO handle requirements more gracefully
    assert KEYWORD_ID in content
    assert KEYWORD_TEXT in content
    assert KEYWORD_QUESTIONS in content

    collection_id: str = content.get(KEYWORD_ID)
    text: str = content.get(KEYWORD_TEXT)
    questions: List[Question] = []

    for question_yaml in content[KEYWORD_QUESTIONS]:
        questions.append(parse_question(question_yaml, collection_id))

    assert questions

    new_collection: QuestionCollection = QuestionCollection(collection_id,
                                                            text, questions)
    logging.debug(f"Parsed question collection {new_collection}")

    # Put the newly parsed object into the global dictionary
    globals.survey_questions[collection_id] = new_collection


def construct_questions_from_metadata(metadata_file: Path) -> None:
    """
    Load metadata from given YAML file.

    Given YAML file with metadata is loaded into a dictionary.

    Raises:
        IOError:    Will be raised if given YAML file could
                    not be opened and loaded.
        ValueError: Will be raised if the provided file does not exist.
    """
    raw_metadata: YamlDict = {}

    if not metadata_file.exists():
        raise ValueError("Metadata file did not exist")

    try:
        with metadata_file.open(mode='r', encoding='utf-8') as file:
            raw_metadata = yaml.load(stream=file,
                                     Loader=yaml.Loader)
    except IOError:
        logging.error(f"YAML file {metadata_file} could not be opened.")
        raise

    if len(raw_metadata) == 0:
        logging.error(f"File {metadata_file} was empty.")
        return

    item: YamlDict
    for item in raw_metadata:
        if KEYWORD_QUESTIONS in item:
            parse_question_collection(item)
        else:
            parse_question(item)


def fetch_participant_answers(
        data_source: DataContainer = globals.dataContainer) -> None:
    """
    Extract the participants' answers for `globals.survey_questions`.

    The function will iterate through the raw pandas frame in the data
    container and extract the per-participant answers for each question.
    All answers will be stored in the globals.survey_questions dictionary.
    No data will be filtered during this operation, all will be transferred
    as-is.

    Args:
        data_source:    A DataContainer wrapping the raw data.
                        Defaults to global.dataContainer
    """
    if data_source.empty:
        raise ValueError("Could not initialize participant answers - "
                         "data source was empty")

    for question_id in globals.survey_questions:
        current_question = globals.survey_questions[question_id]
        if current_question.has_subquestions:
            continue  # collections have no answers

        answers: Dict[str, str] = data_source.data_for_question(question_id)
        participant_id: str
        answer_text: str
        for (participant_id, answer_text) in answers.items():
            current_question.add_given_answer(participant_id, answer_text)
