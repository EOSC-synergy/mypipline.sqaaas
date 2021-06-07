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
import os
from pathlib import Path

import pytest

from hifis_surveyval.core.settings import Settings


@pytest.fixture(scope='function')
def settings_fixture() -> Settings:
    """
    Get a new Settings object.

    Returns:
        Settings:
            New Settings object containing settings of an analysis run.
    """
    return Settings()


@pytest.fixture(scope='function')
def settings_custom_config_fixture() -> Settings:
    """
    Get a new Settings object with custom configuration file loaded.

    Returns:
        Settings:
            New Settings object containing settings of an analysis run.
    """
    fixtures_folder_name: str = "fixtures"
    config_file_name: str = "hifis-surveyval-config-file.yml"
    settings: Settings = Settings()
    settings.CONFIG_FILENAME = os.path.dirname(__file__) / \
        Path(fixtures_folder_name) / Path(config_file_name)
    settings.load_config_file()
    return settings
