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

from hifis_surveyval.models.mixins.yaml_constructable import YamlDict
from tests.helper.yaml_helper.yaml_reader import YamlReader


@pytest.fixture(scope='function')
def metadata_fixture() -> YamlDict:
    """
    Get metadata from YAML file.

    Returns:
        YamlDict:
            YAML containing metadata.
    """
    yaml_file_path: str = \
        './tests/models/answer_option/fixtures/' \
        'metadata-single-answer-option.yml'
    return YamlReader.read_in_yaml_file(yaml_file_path)
