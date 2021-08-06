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

"""Provide pytest test cases for module question."""

import pytest
from pandas import Series

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict
from hifis_surveyval.models.question_collection import Question
from hifis_surveyval.models.translated import Translated
from tests.helper.data_structure_helper.data_structure_creator import \
    DataStructureCreator
from tests.helper.yaml_helper.yaml_reader import YamlReader


class TestQuestion(object):
    """
    Tests Question operations.

    Basic tests for class Question are performed in unit test methods of this
    class.
    """

    # Class properties used by test cases.
    participant_id: str = "1"
    collection_id: str = "Q001"
    question_id: str = "SQ001"
    answer_option_id: str = "A001"
    language_code: str = "en"

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_type(self) -> None:
        """Tests that getting a Question object given metadata works."""
        yaml_file_path: str = (
            "./tests/models/question/fixtures/metadata-single-question.yml"
        )
        metadata_yaml: YamlDict = YamlReader.read_in_yaml_file(yaml_file_path)
        question: Question = Question.from_yaml_dictionary(
            metadata_yaml[0],
            parent_id=TestQuestion.collection_id,
            settings=Settings()
        )
        # Make sure that object retrieved from metadata YAML is of type
        # Question.
        assert isinstance(
            question, Question
        ), "Object is not of type Question."

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_id(self) -> None:
        """Tests that getting a Question object given metadata works."""
        expected_question_id: str = TestQuestion.question_id
        yaml_file_path: str = (
            "./tests/models/question/fixtures/metadata-single-question.yml"
        )
        metadata_yaml: YamlDict = YamlReader.read_in_yaml_file(yaml_file_path)
        question: Question = Question.from_yaml_dictionary(
            metadata_yaml[0],
            parent_id=TestQuestion.collection_id,
            settings=Settings()
        )
        # Make sure that Question object retrieved from metadata YAML has
        # correct question ID.
        assert (
            question.short_id == expected_question_id
        ), "Question ID of question object is not correct."

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_answer_text(self) -> None:
        """Tests that getting a Question object given metadata works."""
        expected_translated_answer_option_text: str = "No"
        yaml_file_path: str = (
            "./tests/models/question/fixtures/metadata-single-question.yml"
        )
        metadata_yaml: YamlDict = YamlReader.read_in_yaml_file(yaml_file_path)
        question: Question = Question.from_yaml_dictionary(
            metadata_yaml[0],
            parent_id=TestQuestion.collection_id,
            settings=Settings()
        )
        answer_option_text: Translated = question._answer_options[
            TestQuestion.answer_option_id
        ].text
        actual_translated_answer_option_text: str = (
            answer_option_text.get_translation(TestQuestion.language_code)
        )
        # Make sure that a Question object retrieved from metadata YAML
        # contains correct translated answer option text.
        assert (
            actual_translated_answer_option_text
            == expected_translated_answer_option_text
        ), "Translated AnswerOption text is not correct."

    @pytest.mark.ci
    def test_add_answer_works(self, question_fixture: Question) -> None:
        """
        Tests that adding answers given by participants to dictionary works.

        Args:
            question_fixture (Question):
                Fixture that sets up a question object to be used in the test
                case.
        """
        expected_translated_answer_option_text: str = "No"
        question: Question = question_fixture
        question.add_answer(
            TestQuestion.participant_id, TestQuestion.answer_option_id
        )
        actual_translated_answer_option_text: str = question._answers[
            TestQuestion.participant_id
        ]
        # Make sure that a Question object of a mandatory question contains the
        # answer given.
        assert (
            actual_translated_answer_option_text
            == expected_translated_answer_option_text
        ), "Given answer of participant is not correct."

    @pytest.mark.ci
    def test_add_answer_but_no_mandatory_answer_given(
        self, question_fixture: Question
    ) -> None:
        """
        Tests that adding empty answer for a mandatory question fails.

        Args:
            question_fixture (Question):
                Fixture that sets up a question object to be used in the test
                case.

        Raises:
            ValueError:
                If answer given to a mandatory question is empty.
        """
        target_answer_value: str = ""
        question: Question = question_fixture
        # Make sure that a ValueError exception is raised if given answer to a
        # mandatory question is empty.
        with pytest.raises(ValueError):
            question.add_answer(
                TestQuestion.participant_id, target_answer_value
            )

    @pytest.mark.ci
    def test_add_empty_answer_works(
        self, question_not_mandatory_fixture: Question
    ) -> None:
        """
        Tests that adding empty answer for a non-mandatory question works.

        Args:
            question_not_mandatory_fixture (Question):
                Fixture that sets up a question object to be used in the test
                case.
        """
        target_answer_value: str = ""
        question: Question = question_not_mandatory_fixture
        question.add_answer(TestQuestion.participant_id, target_answer_value)
        actual_given_answer_value: str = question._answers[
            TestQuestion.participant_id
        ]
        # Make sure that a Question object of a non-mandatory question contains
        # None as answer given if an empty answer is given.
        assert (
            actual_given_answer_value is None
        ), "Given answer of participant is not None."

    @pytest.mark.ci
    def test_add_answer_with_no_answer_options_works(
        self, question_no_answer_options_fixture: Question
    ) -> None:
        """
        Tests that adding an answer to a question without answer options works.

        Args:
            question_no_answer_options_fixture (Question):
                Fixture that sets up a question object to be used in the test
                case.
        """
        target_given_answer_value: int = 42
        expected_given_answer_value: str = "42"
        question: Question = question_no_answer_options_fixture
        question.add_answer(
            TestQuestion.participant_id, target_given_answer_value
        )
        actual_given_answer_value: str = question._answers[
            TestQuestion.participant_id
        ]
        # Make sure that the Question object of a question with no answer
        # options contains the answer given.
        assert (
            actual_given_answer_value == expected_given_answer_value
        ), "Given answer of participant is not casted correctly."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/models/question/fixtures/"
                "metadata-single-question-collection.yml",
                "tests/models/question/fixtures/"
                "test_data_for_module_question.csv",
            ]
        ],
    )
    def test_as_series_works_check_series(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that unit returns a Series for given collection ID.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that sets up a DataContainer object with metadata and
                data to be used in the test cases.
        """
        question_collection_id: str = "Q001/SQ001"
        expected_data_dict = {"1": "No", "2": "Yes", "3": "Maybe"}
        expected_series: Series = DataStructureCreator. \
            create_series_from_dict(expected_data_dict, question_collection_id)
        question: Question = \
            data_container_load_metadata_and_data_fixture \
            .question_for_id(question_collection_id)
        actual_series: Series = question.as_series()
        # Make sure that expected and actual Series are equal.
        assert actual_series.equals(expected_series), \
            "Expected and actual Series are not equal."
