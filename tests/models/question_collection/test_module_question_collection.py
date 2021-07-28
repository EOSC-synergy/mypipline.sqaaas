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

"""Provide pytest test cases for module question_collection."""

import pytest

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict
from hifis_surveyval.models.question import Question
from hifis_surveyval.models.question_collection import QuestionCollection
from hifis_surveyval.models.translated import Translated


class TestQuestionCollection(object):
    """
    Tests QuestionCollection operations.

    Basic tests for class QuestionCollection are performed in unit test
    methods of this class.
    """

    # Default class properties used by test cases.
    question_id: str = "SQ001"
    answer_option_id: str = "A001"
    language_code: str = "en"

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_type(self, metadata_fixture):
        """
        Tests that the retrieved object is of type QuestionCollection.

        Args:
            metadata_fixture (YamlDict):
                Test fixture providing metadata of a QuestionCollection.
        """
        metadata_yaml: YamlDict = metadata_fixture
        question_collection: QuestionCollection = (
            QuestionCollection.from_yaml_dictionary(metadata_yaml[0],
                                                    settings=Settings())
        )
        # Make sure that QuestionCollection object can be retrieved by
        # metadata YAML file.
        assert isinstance(
            question_collection, QuestionCollection
        ), "Object is not of type QuestionCollection."

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_text(self, metadata_fixture):
        """
        Tests that the retrieved translated AnswerOption text is as expected.

        Args:
            metadata_fixture (YamlDict):
                Test fixture providing metadata of a QuestionCollection.
        """
        expected_translated_answer_option_text: str = "No"
        metadata_yaml: YamlDict = metadata_fixture
        question_collection: QuestionCollection = (
            QuestionCollection.from_yaml_dictionary(metadata_yaml[0],
                                                    settings=Settings())
        )
        answer_option_text: Translated = (
            question_collection.question_for_id(
                TestQuestionCollection.question_id
            )
            ._answer_options[TestQuestionCollection.answer_option_id]
            .text
        )
        actual_translated_answer_option_text: str = (
            answer_option_text.get_translation(
                TestQuestionCollection.language_code
            )
        )
        # Make sure that translated AnswerOption text is correct.
        assert (
            actual_translated_answer_option_text
            == expected_translated_answer_option_text
        ), "Translated AnswerOption text is not correct."

    @pytest.mark.ci
    def test_question_for_id_works(self, metadata_fixture):
        """
        Tests that the retrieved object is of type Question.

        Args:
            metadata_fixture (YamlDict):
                Test fixture providing metadata of a QuestionCollection.
        """
        metadata_yaml: YamlDict = metadata_fixture
        question_collection: QuestionCollection = (
            QuestionCollection.from_yaml_dictionary(metadata_yaml[0],
                                                    settings=Settings())
        )
        question: Question = question_collection.question_for_id(
            TestQuestionCollection.question_id
        )
        # Make sure that object is of type Question.
        assert isinstance(
            question, Question
        ), "Object is not of type Question."
