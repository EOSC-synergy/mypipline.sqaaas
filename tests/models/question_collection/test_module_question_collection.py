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
from typing import List

import pytest
from pandas import DataFrame

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict
from hifis_surveyval.models.question import Question
from hifis_surveyval.models.question_collection import QuestionCollection
from tests.helper.data_structure_helper.data_structure_creator import \
    DataStructureCreator


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
        actual_translated_answer_option_text: str = (
            question_collection.question_for_id(
                TestQuestionCollection.question_id
            )
            ._answer_options[TestQuestionCollection.answer_option_id]
            .text(
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

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/models/question_collection/fixtures/"
                "metadata-single-question-collection-three-questions.yml",
                "tests/models/question_collection/fixtures/"
                "test_data_for_module_question_collection.csv"
            ],
        ],
    )
    def test_as_data_frame_works(
            self,
            data_container_load_metadata_and_data_fixture: DataContainer):
        """
        Tests that the DataFrame retrieved from Collection is correct.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                DataContainer containing metadata from YAML file and data from
                CSV file.
        """
        expected_data_dict = {"id": ["1", "2", "3"],
                              "Q001/SQ001": ["No", "Yes", "I do not know"],
                              "Q001/SQ002": ["Yes", "I do not know", "No"],
                              "Q001/SQ003": ["I do not know", "No", "Yes"]}
        expected_frame: DataFrame = DataStructureCreator. \
            create_dataframe_from_dict(expected_data_dict)
        question_collection_id: str = "Q001"
        question_collection: QuestionCollection = \
            data_container_load_metadata_and_data_fixture \
            .collection_for_id(question_collection_id)
        actual_data_frame: DataFrame = question_collection.as_data_frame()
        # Make sure that expected and actual DataFrames are equal.
        assert actual_data_frame.equals(expected_frame), \
            "Expected and actual DataFrames are not equal."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/models/question_collection/fixtures/"
                "metadata-single-question-collection-three-questions.yml",
                "tests/models/question_collection/fixtures/"
                "test_data_for_module_question_collection.csv"
            ],
        ],
    )
    def test_as_data_frame_works_check_question_subset(
            self,
            data_container_load_metadata_and_data_fixture: DataContainer):
        """
        Tests that the DataFrame subset retrieved from Collection is correct.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                DataContainer containing metadata from YAML file and data from
                CSV file.
        """
        expected_data_dict = {"id": ["1", "2", "3"],
                              "Q001/SQ001": ["No", "Yes", "I do not know"],
                              "Q001/SQ003": ["I do not know", "No", "Yes"]}
        expected_frame: DataFrame = DataStructureCreator. \
            create_dataframe_from_dict(expected_data_dict)
        question_collection_id: str = "Q001"
        exclude_list_question_ids: List[str] = ["SQ002"]
        question_collection: QuestionCollection = \
            data_container_load_metadata_and_data_fixture \
            .collection_for_id(question_collection_id)
        actual_data_frame: DataFrame = \
            question_collection.as_data_frame(exclude_list_question_ids)
        # Make sure that expected and actual DataFrames are equal.
        assert actual_data_frame.equals(expected_frame), \
            "Expected and actual DataFrames are not equal."
