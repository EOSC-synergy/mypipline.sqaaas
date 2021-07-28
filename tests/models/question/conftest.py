#!/usr/bin/env python

# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

"""Offering pytest fixtures to test cases of this package."""

import pytest

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict
from hifis_surveyval.models.question import Question
from tests.helper.yaml_helper.yaml_reader import YamlReader


def question_from_metadata(yaml_file_path: str) -> Question:
    """
    Retrieve Question object from given metadata YAML file.

    Args:
        yaml_file_path (str):
            Path to YAML file containing metadata.

    Returns:
        Question:
            Question object constructed from given metadata YAML file.
    """
    target_question_collection_id: str = "Q001"
    metadata_yaml: YamlDict = YamlReader.read_in_yaml_file(yaml_file_path)
    question: Question = Question.from_yaml_dictionary(
        metadata_yaml[0],
        parent_id=target_question_collection_id,
        settings=Settings()
    )
    return question


@pytest.fixture(scope="function")
def question_fixture() -> Question:
    """
    Get a new Question object of a mandatory question.

    Returns:
        Question:
            New Question object of given metadata as a test fixture.
    """
    yaml_file_path: str = (
        "./tests/models/question/fixtures/metadata-single-question.yml"
    )
    question: Question = question_from_metadata(yaml_file_path)
    return question


@pytest.fixture(scope="function")
def question_not_mandatory_fixture() -> Question:
    """
    Get a new Question object of a non-mandatory question.

    Returns:
        Question:
            New Question object of given metadata as a test fixture.
    """
    yaml_file_path: str = (
        "./tests/models/question/fixtures/"
        "metadata-single-question-not-mandatory.yml"
    )
    question: Question = question_from_metadata(yaml_file_path)
    return question


@pytest.fixture(scope="function")
def question_no_answer_options_fixture() -> Question:
    """
    Get a new Question object not containing answer options.

    Returns:
        Question:
            New Question object of given metadata as a test fixture.
    """
    yaml_file_path: str = (
        "./tests/models/question/fixtures/"
        "metadata-single-question-no-answer-options.yml"
    )
    question: Question = question_from_metadata(yaml_file_path)
    return question
