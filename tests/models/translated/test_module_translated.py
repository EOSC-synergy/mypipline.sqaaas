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

"""Provide pytest test cases for module translated."""

from typing import Dict, List

import pytest
from schema import SchemaWrongKeyError

from hifis_surveyval.models.translated import Translated


class TestModuleTranslated(object):
    """
    Tests Translated operations.

    Basic tests for class Translated are performed in unit test methods of
    this class.
    """

    @pytest.mark.ci
    def test_get_translation_works(self, translated_fixture: Translated):
        """
        Tests that getting a translation given a language code works.

        Args:
            translated_fixture (Translated):
                New Translated object to manage translations of questions and
                answers.
        """
        translated: Translated = translated_fixture
        target_language_code: str = 'de'
        expected_translated_text: str = 'deutscher Text'
        # Make sure that translation can be retrieved by a language code.
        assert translated.get_translation(target_language_code) == \
               expected_translated_text, \
               "Getter is not returning expected translation given a code."

    @pytest.mark.ci
    def test_translation_code_not_iso(
            self, non_iso_code_translations_dict_fixture: Dict[str, str]):
        """
        Tests that a non-iso language code raises exception.

        Args:
            non_iso_code_translations_dict_fixture (Dict[str, str]):
                New translations dict object to manage translations of
                questions and answers.
        """
        # Make sure that exception SchemaWrongKeyError is raised.
        with pytest.raises(SchemaWrongKeyError):
            # Try to instantiate Translated object given a non-iso language
            # code.
            Translated(non_iso_code_translations_dict_fixture)

    @pytest.mark.ci
    def test_available_languages_works(self, translated_fixture: Translated):
        """
        Tests that getting a list of all languages works.

        Args:
            translated_fixture (Translated):
                New Translated object to manage translations of questions and
                answers.
        """
        translated: Translated = translated_fixture
        expected_languages_list: List[str] = ['de', 'en']
        # Make sure that available languages can be retrieved.
        assert translated.available_languages().sort() == \
               expected_languages_list.sort(), \
               "Getter is not returning expected list of translations."

    @pytest.mark.ci
    def test_from_yaml_dictionary_works(
            self, translations_dict_fixture: Dict[str, str]):
        """
        Tests that a construction of Translated object works.

        Args:
            translations_dict_fixture (Dict[str, str]):
                New translations dict object to manage translations of
                questions and answers.
        """
        target_language_code: str = 'de'
        expected_translated_text: str = 'deutscher Text'
        translated: Translated = \
            Translated.from_yaml_dictionary(translations_dict_fixture)
        # Make sure Translated object was constructed properly.
        assert translated.get_translation(target_language_code) == \
               expected_translated_text, \
               "Method from_yaml_dictionary did not construct Translated" \
               "object properly."
