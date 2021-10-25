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

"""Provide pytest test cases for module answer_option."""

import pytest

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.models.answer_option import AnswerOption
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict


class TestAnswerOption(object):
    """
    Tests AnswerOption operations.

    Basic tests for class AnswerOption are performed in unit test
    methods of this class.
    """

    # Class properties used by test cases.
    question_id: str = "SQ001"
    answer_option_id: str = "A001"
    language_code: str = "en"

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_type(
        self,
        metadata_fixture: YamlDict,
        settings_fixture: Settings
    ) -> None:
        """
        Tests that retrieving an AnswerOption object given metadata works.

        Args:
            metadata_fixture (YamlDict):
                Test fixture providing an AnswerOption object.
            settings_fixture:
                Test fixture providing default settings.
        """
        answer_option: AnswerOption = AnswerOption.from_yaml_dictionary(
            yaml=metadata_fixture[0],
            parent_id=TestAnswerOption.question_id,
            settings=settings_fixture,
            answer_type=str
        )
        # Make sure that object retrieved from metadata YAML file given is of
        # type AnswerOption.
        assert isinstance(
            answer_option, AnswerOption
        ), "Object is not of type AnswerOption."

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_id(
        self,
        metadata_fixture: YamlDict,
        settings_fixture: Settings
    ) -> None:
        """
        Tests that retrieving an AnswerOption object given metadata works.

        Args:
            metadata_fixture (YamlDict):
                Test fixture providing an AnswerOption object.
            settings_fixture:
                Test fixture providing default settings.
        """
        expected_answer_option_id: str = TestAnswerOption.answer_option_id
        answer_option: AnswerOption = AnswerOption.from_yaml_dictionary(
            yaml=metadata_fixture[0],
            parent_id=TestAnswerOption.question_id,
            settings=settings_fixture,
            answer_type=str
        )
        actual_answer_option_id: str = answer_option.short_id
        # Make sure that AnswerOption object retrieved from metadata YAML file
        # has correct AnswerOption ID.
        assert (
            actual_answer_option_id == expected_answer_option_id
        ), "AnswerOption ID of AnswerOption object is not correct."

    @pytest.mark.ci
    def test_from_yaml_dictionary_works_check_text(
            self,
            metadata_fixture: YamlDict,
            settings_fixture: Settings
    ) -> None:
        """
        Tests that retrieving an AnswerOption object given metadata works.

        Args:
            metadata_fixture (YamlDict):
                Test fixture providing an AnswerOption object.
            settings_fixture:
                Test fixture providing default settings.
        """
        expected_translated_answer_option_text: str = "No"
        answer_option: AnswerOption = AnswerOption.from_yaml_dictionary(
            yaml=metadata_fixture[0],
            parent_id=TestAnswerOption.question_id,
            settings=settings_fixture,
            answer_type=str
        )
        actual_translated_answer_option_text: str = (
            answer_option.text(TestAnswerOption.language_code)
        )
        # Make sure that AnswerOption object retrieved from metadata YAML file
        # has correct translated AnswerOption text.
        assert (
            actual_translated_answer_option_text
            == expected_translated_answer_option_text
        ), "Translated AnswerOption text is not correct."
