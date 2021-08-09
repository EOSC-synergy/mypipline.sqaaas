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

"""Provide pytest test cases for module data_container."""

from typing import Dict, List, Optional, Union

import pytest
from pandas import DataFrame

from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.models.answer_option import AnswerOption
from hifis_surveyval.models.mixins.identifiable import Identifiable
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict, YamlList
from hifis_surveyval.models.question import Question
from hifis_surveyval.models.question_collection import QuestionCollection
from hifis_surveyval.models.translated import Translated
from tests.helper.data_structure_helper.data_structure_creator import \
    DataStructureCreator


class TestDataContainer(object):
    """
    Tests DataContainer operations.

    Basic tests for class DataContainer are performed in unit test methods of
    this class.
    """

    # Default class properties to be used in several test-cases.
    collection_id: str = "Q001"
    question_id: str = "SQ001"
    answer_option_id: str = "A001"
    answer_option_language_code: str = "en"
    answer_translation: str = "No"

    @pytest.mark.ci
    def test_data_is_empty_initially(
        self, data_container_fixture: DataContainer
    ) -> None:
        """
        Tests that list of QuestionCollections in DataContainer is empty.

        Args:
            data_container_fixture (DataContainer):
                Fixture that provides an empty DataContainer.
        """
        # Make sure that list of QuestionCollections in DataContainer is empty
        # initially.
        assert (
            not data_container_fixture.survey_questions
        ), "Metadata is not empty initially."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_load_metadata_works_check_question_collection_count(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading metadata works and checks question collection count.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        expected_count_question_collection: int = 1
        actual_count_question_collection: int = len(
            data_container_load_metadata_fixture.survey_questions
        )
        # Make sure that one QuestionCollection is in the list of
        # QuestionCollections.
        assert (
            expected_count_question_collection
            == actual_count_question_collection
        ), "Count of metadata is not correct."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_load_metadata_works_check_question_collection_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading metadata works and checks type of collection object.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question_collection: QuestionCollection = (
            data_container_load_metadata_fixture
            .collection_for_id(TestDataContainer.collection_id)
        )
        # Make sure that object is of type QuestionCollection.
        assert isinstance(
            question_collection, QuestionCollection
        ), "Object is not of type QuestionCollection."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_load_metadata_works_check_question_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading metadata works and checks type of question object.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question: Question = data_container_load_metadata_fixture\
            .collection_for_id(
                TestDataContainer.collection_id
            ).question_for_id(TestDataContainer.question_id)
        # Make sure that object is of type Question.
        assert isinstance(
            question, Question
        ), "Object is not of type Question."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_load_metadata_works_check_answer_option_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading metadata works and checks type of answer object.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        answer_option: AnswerOption = (
            data_container_load_metadata_fixture
            .collection_for_id(TestDataContainer.collection_id)
            .question_for_id(TestDataContainer.question_id)
            ._answer_options[TestDataContainer.answer_option_id]
        )
        # Make sure object is of type AnswerOption.
        assert isinstance(
            answer_option, AnswerOption
        ), "Object is not of type AnswerOption."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_load_metadata_works_check_translated_answer_text(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading metadata works and checks translated answer text.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        translated_answer: Translated = (
            data_container_load_metadata_fixture
            .collection_for_id(TestDataContainer.collection_id)
            .question_for_id(TestDataContainer.question_id)
            ._answer_options[TestDataContainer.answer_option_id]
            .text
        )
        actual_translated_answer_text: str = translated_answer.get_translation(
            TestDataContainer.answer_option_language_code
        )
        # Make sure that translated answer option is correct.
        assert (
            actual_translated_answer_text
            == TestDataContainer.answer_translation
        ), "Translated answer option is not correct."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-question-collections.yml"
        ],
    )
    def test_load_multi_metadata_works_check_collection_count(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading multiple metadata works and check collection count.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        expected_count_question_collection: int = 2
        actual_count_question_collection: int = len(
            data_container_load_metadata_fixture.survey_questions
        )
        # Make sure that two QuestionCollections are in the list of
        # QuestionCollections.
        assert (
            actual_count_question_collection
            == expected_count_question_collection
        ), "Count of metadata is not correct."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-question-collections.yml"
        ],
    )
    def test_load_multi_metadata_works_check_collection_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading multiple metadata works and check collection count.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question_collection_id: str = "Q002"
        question_collection: QuestionCollection = (
            data_container_load_metadata_fixture
            .collection_for_id(question_collection_id)
        )
        # Make sure that object is of type QuestionCollection.
        assert isinstance(
            question_collection, QuestionCollection
        ), "Object is not of type QuestionCollection."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-question-collections.yml"
        ],
    )
    def test_load_multi_metadata_works_check_question_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading multi metadata works and checks type of question.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question_collection_id: str = "Q002"
        question_id: str = "SQ002"
        question: Question = data_container_load_metadata_fixture \
            .collection_for_id(question_collection_id) \
            .question_for_id(question_id)
        # Make sure that object is of type question.
        assert isinstance(
            question, Question
        ), "Object is not of type Question."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-question-collections.yml"
        ],
    )
    def test_load_multi_metadata_works_check_answer_option_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading multi metadata works and checks type of answer.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question_collection_id: str = "Q002"
        question_id: str = "SQ002"
        answer_option_id: str = "A002"
        answer_option: AnswerOption = (
            data_container_load_metadata_fixture
            .collection_for_id(question_collection_id)
            .question_for_id(question_id)
            ._answer_options[answer_option_id]
        )
        # Make sure that object is of type AnswerOption.
        assert isinstance(
            answer_option, AnswerOption
        ), "Object is not of type AnswerOption."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-question-collections.yml"
        ],
    )
    def test_load_multi_metadata_works_check_translated_answer_text(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that loading multi metadata works and checks translated answer.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        expected_translated_answer_text: str = "No"
        question_collection_id: str = "Q002"
        question_id: str = "SQ002"
        answer_option_id: str = "A002"
        translation_language_code: str = "en"
        translated_answer: Translated = (
            data_container_load_metadata_fixture
            .collection_for_id(question_collection_id)
            .question_for_id(question_id)
            ._answer_options[answer_option_id]
            .text
        )
        actual_translated_answer_text: str = translated_answer.get_translation(
            translation_language_code
        )
        # Make sure that translated answer option is correct.
        assert (
            actual_translated_answer_text == expected_translated_answer_text
        ), "Translated answer option is not correct."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-duplicate-question-collections.yml"
        ],
    )
    def test_add_collection_from_yaml_with_duplicates(
        self,
        data_container_fixture: DataContainer,
        read_in_metadata_yaml_file: Union[YamlList, YamlDict],
    ) -> None:
        """
        Tests that exception is raised when loading metadata with duplications.

        Args:
            data_container_fixture (DataContainer):
                Fixture that provides an empty DataContainer.
            read_in_metadata_yaml_file (Union[YamlList, YamlDict]):
                Fixture that provides metadata from YAML file.

        Raises:
            ValueError:
                If metadata contains duplicated IDs.
        """
        metadata: Union[YamlList, YamlDict] = read_in_metadata_yaml_file
        data_container_fixture._add_collection_from_yaml(metadata[0])
        # Make sure that ValueError is raised when facing duplicate
        # QuestionCollection IDs.
        with pytest.raises(ValueError):
            data_container_fixture._add_collection_from_yaml(metadata[1])

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-two-duplicate-question-collections.yml"
        ],
    )
    def test_load_metadata_with_duplicates(
        self,
        caplog,
        data_container_fixture: DataContainer,
        read_in_metadata_yaml_file: Union[YamlList, YamlDict],
    ) -> None:
        """
        Tests that exception is raised when loading metadata with duplications.

        Args:
            data_container_fixture (DataContainer):
                Fixture that provides an empty DataContainer.
            read_in_metadata_yaml_file (Union[YamlList, YamlDict]):
                Fixture that provides metadata from YAML file.
        """
        metadata: Union[YamlList, YamlDict] = read_in_metadata_yaml_file
        data_container_fixture.load_metadata(metadata[0])
        data_container_fixture.load_metadata(metadata[1])
        # Make sure that warning is logged when facing duplicate
        # QuestionCollection IDs.
        assert (
            "Error while parsing metadata: "
            "Attempted to assign duplicate ID" in caplog.text
        )

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path,"
        "collection_id,expected_type",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q001",
                bool,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q002",
                str,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q003",
                int,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q004",
                float,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q005",
                str,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q006",
                str,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q007",
                type(None),
            ],
        ],
    )
    def test_load_survey_data_works_check_given_answer_type(
        self,
        data_container_load_metadata_and_data_fixture: DataContainer,
        collection_id: str,
        expected_type: type,
    ) -> None:
        """
        Tests that loading survey data works and check answer type.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
            collection_id (str):
                ID of the collection to load.
            expected_type (type):
                Expected type of the given answer.
        """
        question_id: str = "SQ001"
        answer_id: str = "1"
        actual_answer_type: type = type(
            data_container_load_metadata_and_data_fixture
            .collection_for_id(collection_id)
            .question_for_id(question_id)
            ._answers[answer_id]
        )
        # Make sure that data consists of correct types.
        assert (
            actual_answer_type is expected_type
        ), "Given answer to question is not of expected type."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path,"
        "collection_id,expected_value",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q001",
                True,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q002",
                "Option1",
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q003",
                123,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q004",
                12.3,
            ],
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
                "Q006",
                "N/A",
            ],
        ],
    )
    def test_load_survey_data_works_check_given_answer_value(
        self,
        data_container_load_metadata_and_data_fixture: DataContainer,
        collection_id: str,
        expected_value: Union[bool, str, int, float],
    ) -> None:
        """
        Tests that loading survey data works and check answer value.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
            collection_id (str):
                ID of the collection to load.
            expected_value (str):
                Expected value of the given answer.
        """
        question_id: str = "SQ001"
        answer_id: str = "1"
        actual_answer_value: Union[bool, str, int, float] = (
            data_container_load_metadata_and_data_fixture
            .collection_for_id(collection_id)
            .question_for_id(question_id)
            ._answers[answer_id]
        )
        # Make sure that data consists of correct values.
        assert (
            actual_answer_value == expected_value
        ), "Given answer to question is not as expected."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container_wrong_keys.csv",
            ]
        ],
    )
    def test_load_survey_data_with_wrong_keys_works_check_collection_count(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that loading survey data works also with wrong keys.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        expected_question_collection_count: int = 7
        collections: List[QuestionCollection] = \
            data_container_load_metadata_and_data_fixture.survey_questions
        count_collections: int = len(collections)
        # Make sure that seven QuestionCollections are in the list of
        # QuestionCollections.
        assert (
            count_collections == expected_question_collection_count
        ), "Wrong QuestionCollection count."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container_wrong_keys.csv",
            ]
        ],
    )
    def test_load_survey_data_with_wrong_keys_works_check_question_count(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that loading survey data works also with wrong keys.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        expected_question_count_from_metadata: int = 1
        questions: Dict[str, Question] = \
            data_container_load_metadata_and_data_fixture \
            .collection_for_id(TestDataContainer.collection_id) \
            ._questions
        count_questions: int = len(questions)
        # Make sure that one Question is in the list of Questions.
        assert (
            count_questions == expected_question_count_from_metadata
        ), "Wrong Question count."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container_wrong_keys.csv",
            ]
        ],
    )
    def test_load_survey_data_with_wrong_keys_works_check_answer_count(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that loading survey data works also with wrong keys.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        expected_answer_count_from_data: int = 0
        answers: Dict[str, Optional[Union[bool, str, int, float]]] = (
            data_container_load_metadata_and_data_fixture
            .collection_for_id(TestDataContainer.collection_id)
            .question_for_id(TestDataContainer.question_id)
            ._answers
        )
        count_given_answers: int = len(answers)
        # Make sure that one Answer is in the list of given answers.
        assert (
            count_given_answers == expected_answer_count_from_data
        ), "Wrong given answer count."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_collection_for_id_works_check_object_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that retrieving a QuestionCollection entry works.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question_collection: QuestionCollection = (
            data_container_load_metadata_fixture
            .collection_for_id(TestDataContainer.collection_id)
        )
        # Make sure that object is of type QuestionCollection.
        assert isinstance(
            question_collection, QuestionCollection
        ), "Retrieved object is not of type QuestionCollection."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_collection_for_id_works_check_full_id(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that retrieving a QuestionCollection entry works.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        expected_question_collection_id: str = "Q001"
        question_collection_full_id: str = \
            data_container_load_metadata_fixture.collection_for_id(
                TestDataContainer.collection_id
            )._full_id
        # Make sure that QuestionCollection has correct full ID.
        assert (
            question_collection_full_id == expected_question_collection_id
        ), "Wrong QuestionCollection object has been retrieved."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_question_for_id_in_question_collection_works_check_object_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that retrieving a Question entry works.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        target_question_full_id: str = (
            f"Q001{Identifiable.HIERARCHY_SEPARATOR}SQ001"
        )
        question: Question = data_container_load_metadata_fixture \
            .question_for_id(target_question_full_id)
        # Make sure that object is of type QuestionCollection.
        assert isinstance(
            question, Question
        ), "Retrieved object is not of type Question."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_question_for_id_in_question_collection_works_check_full_id(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that retrieving a Question entry works.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        target_question_full_id: str = (
            f"Q001{Identifiable.HIERARCHY_SEPARATOR}SQ001"
        )
        question_full_id: str = data_container_load_metadata_fixture \
            .question_for_id(target_question_full_id)._full_id
        # Make sure that Question has correct full ID.
        assert (
            question_full_id == target_question_full_id
        ), "Wrong Question object has been retrieved."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_question_for_id_works_check_question_type(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that retrieving a Question entry works.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        question: Question = data_container_load_metadata_fixture \
            .collection_for_id(TestDataContainer.collection_id) \
            .question_for_id(TestDataContainer.question_id)
        # Make sure that object is of type Question.
        assert isinstance(
            question, Question
        ), "Retrieved object is not of type Question."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path",
        [
            "tests/data_container/fixtures/"
            "metadata-single-question-collection.yml"
        ],
    )
    def test_question_for_id_works_check_question_full_id(
        self, data_container_load_metadata_fixture: DataContainer
    ) -> None:
        """
        Tests that retrieving a Question entry works.

        Args:
            data_container_load_metadata_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata.
        """
        expected_question_full_id: str = (
            f"Q001{Identifiable.HIERARCHY_SEPARATOR}SQ001"
        )
        question_full_id: str = (
            data_container_load_metadata_fixture
            .collection_for_id(TestDataContainer.collection_id)
            .question_for_id(TestDataContainer.question_id)
            ._full_id
        )
        # Make sure that Question has correct full ID.
        assert (
            question_full_id == expected_question_full_id
        ), "Wrong Question object has been retrieved."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
            ]
        ],
    )
    def test_data_frame_for_ids_works_check_single_question(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that unit returns a DataFrame for a given collection ID.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        expected_data_dict = {"id": ["1", "2", "3"],
                              "Q002/SQ001": ["Option1", "Option2", "Option3"]}
        expected_frame: DataFrame = DataStructureCreator. \
            create_dataframe_from_dict(expected_data_dict)
        actual_frame: DataFrame = \
            data_container_load_metadata_and_data_fixture \
            .data_frame_for_ids(["Q002/SQ001"])
        # Make sure that expected and actual DataFrames are equal.
        assert actual_frame.equals(expected_frame), \
            "Expected and actual DataFrames are not equal."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/data_container/fixtures/"
                "metadata-seven-question-collections.yml",
                "tests/data_container/fixtures/"
                "test_data_for_module_data_container.csv",
            ]
        ],
    )
    def test_data_frame_for_ids_works_check_multiple_questions(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that unit returns a DataFrame for given collection IDs.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        expected_data_dict = {"id": ["1", "2", "3"],
                              "Q002/SQ001": ["Option1", "Option2", "Option3"],
                              "Q003/SQ001": [123, 456, 789]}
        expected_frame: DataFrame = DataStructureCreator. \
            create_dataframe_from_dict(expected_data_dict)
        actual_frame: DataFrame = \
            data_container_load_metadata_and_data_fixture \
            .data_frame_for_ids(["Q002/SQ001", "Q003/SQ001"])
        # Make sure that expected and actual DataFrames are equal.
        assert actual_frame.equals(expected_frame), \
            "Expected and actual DataFrames are not equal."
