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

"""Provide pytest test cases for module settings."""

import logging
import os
import re
from pathlib import Path
from typing import List

import pytest

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.plotting.supported_output_format import \
    SupportedOutputFormat


class TestModuleSettings(object):
    """
    Tests Settings operations.

    Basic tests for class Settings are performed in unit test methods of
    this class.
    """

    @pytest.mark.ci
    def test_config_filename_is_correct(self, settings_fixture: Settings):
        """
        Tests that config filename is given.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_config_filename: str = "hifis-surveyval.yml"
        settings: Settings = settings_fixture
        assert settings.CONFIG_FILENAME.absolute() == \
               Path(expected_config_filename).absolute(), \
               "Default value of config filename is not correct."

    @pytest.mark.ci
    def test_verbosity_is_correct(self, settings_fixture: Settings):
        """
        Tests that verbosity default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_verbosity: int = logging.NOTSET
        settings: Settings = settings_fixture
        assert settings.VERBOSITY == expected_verbosity, \
               "Default value of verbosity is not correct."

    @pytest.mark.ci
    def test_run_timestamp_is_correct(self, settings_fixture: Settings):
        """
        Tests that run timestamp default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_timestamp_regex: re = \
            r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}'
        settings: Settings = settings_fixture
        settings.set_timestamp('')
        assert re.match(expected_timestamp_regex, settings.RUN_TIMESTAMP), \
               "Default value of run timestamp is not correct."

    @pytest.mark.ci
    def test_analysis_output_path_is_correct(self, settings_fixture: Settings):
        """
        Tests that analysis output path default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        settings: Settings = settings_fixture
        expected_output_folder: str = "output"
        expected_run_timestamp: str = settings.set_timestamp('')
        expected_output_folder_path: Path = \
            Path(expected_output_folder) / Path(expected_run_timestamp)
        settings.assemble_output_path(
            '',
            {"OUTPUT_FOLDER": Path(expected_output_folder),
             "RUN_TIMESTAMP": Path(expected_run_timestamp)})
        assert settings.ANALYSIS_OUTPUT_PATH.absolute() == \
               Path(expected_output_folder_path).absolute(), \
               "Default value of analysis output path is not correct."

    @pytest.mark.ci
    def test_metadata_path_is_correct(self, settings_fixture: Settings):
        """
        Tests that metadata path default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_metadata_path: str = "metadata/meta.yml"
        settings: Settings = settings_fixture
        assert settings.METADATA.absolute() == \
               Path(expected_metadata_path).absolute(), \
               "Default value of metadata path is not correct."

    @pytest.mark.ci
    def test_scripts_folder_is_correct(self, settings_fixture: Settings):
        """
        Tests that script folder default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_script_folder: str = "scripts"
        settings: Settings = settings_fixture
        assert settings.SCRIPT_FOLDER.absolute() == \
               Path(expected_script_folder).absolute(), \
               "Default value of script folder is not correct."

    @pytest.mark.ci
    def test_script_names_is_correct(self, settings_fixture: Settings):
        """
        Tests that script names default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        settings: Settings = settings_fixture
        assert isinstance(settings.SCRIPT_NAMES, List), \
               "Datatype of list of script names is not a list."
        assert len(settings.SCRIPT_NAMES) == 0, \
               "Default value of list of script names is not empty."

    @pytest.mark.ci
    def test_output_format_is_correct(self, settings_fixture: Settings):
        """
        Tests that output format default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_output_format: SupportedOutputFormat = \
            SupportedOutputFormat.SCREEN
        settings: Settings = settings_fixture
        assert settings.OUTPUT_FORMAT == expected_output_format, \
               "Default value of output format is not correct."

    @pytest.mark.ci
    def test_output_folder_is_correct(self, settings_fixture: Settings):
        """
        Tests that output folder default value is correct.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_output_folder: str = "output"
        settings: Settings = settings_fixture
        assert settings.OUTPUT_FOLDER.absolute() == \
               Path(expected_output_folder).absolute(), \
               "Default value of output folder is not correct."

    @pytest.mark.ci
    def test_set_verbosity_warning(self, settings_fixture: Settings):
        """
        Tests that setting verbosity level works.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_verbosity: int = logging.WARNING
        verbosity_option_index_warning: int = 1
        settings: Settings = settings_fixture
        settings.set_verbosity(verbosity_option_index_warning)
        assert settings.VERBOSITY == expected_verbosity, \
               "Value of verbosity level set is not correct."

    @pytest.mark.ci
    def test_load_config_file(self, settings_fixture: Settings):
        """
        Tests that loading a configuration file works.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        fixtures_folder_name: str = "fixtures"
        config_file_name: str = "hifis-surveyval-fixture.yml"
        expected_metadata_path: str = "metadata/metadata.yml"
        expected_output_folder: str = "output_folder"
        expected_output_format: SupportedOutputFormat = \
            SupportedOutputFormat.SVG
        expected_script_folder: str = "scripts_folder"
        expected_script_names: List[str] = ["example_script"]
        settings: Settings = settings_fixture
        settings.CONFIG_FILENAME = os.path.dirname(__file__) / \
            Path(fixtures_folder_name) / Path(config_file_name)
        settings.load_config_file()
        assert settings.METADATA.absolute() == \
               Path(expected_metadata_path).absolute(), \
               "Value of metadata path set is not correct."
        assert settings.OUTPUT_FOLDER.absolute() == \
               Path(expected_output_folder).absolute(), \
               "Value of output folder set is not correct."
        assert settings.OUTPUT_FORMAT == expected_output_format, \
               "Value of output format set is not correct."
        assert settings.SCRIPT_FOLDER.absolute() == \
               Path(expected_script_folder).absolute(), \
               "Value of script folder set is not correct."
        assert isinstance(settings.SCRIPT_NAMES, List), \
               "Datatype of list of script names is not a list."
        assert len(settings.SCRIPT_NAMES) == len(expected_script_names), \
               "List size of script names is not as expected."
        assert settings.SCRIPT_NAMES[0] == expected_script_names[0], \
               "First element of list of script names is not as expected."
