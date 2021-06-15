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

from typing import Dict

import pytest

from hifis_surveyval.models.mixins.yaml_constructable import YamlDict
from hifis_surveyval.models.translated import Translated
from tests.helper.yaml_helper.yaml_reader import YamlReader


@pytest.fixture(scope="function")
def non_iso_code_translations_dict_fixture() -> Dict[str, str]:
    """
    Get a new translations dict.

    Returns:
        Dict[str, str]:
            New translations dict to manage translations of questions and
            answers.
    """
    yaml_file_path: str = (
        "./tests/models/translated/fixtures/"
        "non-iso-code-translations-fixture.yml"
    )
    return YamlReader.read_in_yaml_file(yaml_file_path)


@pytest.fixture(scope="function")
def translated_fixture() -> Translated:
    """
    Get a new Translated object.

    Returns:
        Translated:
            New Translated object to manage translations of questions and
            answers.
    """
    yaml_file_path: str = (
        "./tests/models/translated/fixtures/translations-fixture.yml"
    )
    translations: YamlDict = YamlReader.read_in_yaml_file(yaml_file_path)
    return Translated(translations)


@pytest.fixture(scope="function")
def translations_dict_fixture() -> Dict[str, str]:
    """
    Get a new translations dict.

    Returns:
        Dict[str, str]:
            New translations dict to manage translations of questions and
            answers.
    """
    yaml_file_path: str = (
        "./tests/models/translated/fixtures/translations-fixture.yml"
    )
    return YamlReader.read_in_yaml_file(yaml_file_path)
