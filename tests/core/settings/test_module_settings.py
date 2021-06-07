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
    def test_setting_verbosity_works(self, settings_fixture: Settings):
        """
        Tests that setting verbosity works fine.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_verbosity: int = logging.INFO
        verbosity_count: int = 2
        settings: Settings = settings_fixture
        settings.set_verbosity(verbosity_count)
        assert settings.VERBOSITY == expected_verbosity, \
               "Value of verbosity set is not correct."

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
               "Format of default value of run timestamp is not correct."

    @pytest.mark.ci
    def test_setting_run_timestamp_works(self, settings_fixture: Settings):
        """
        Tests that setting run timestamp works fine.

        Args:
            settings_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_timestamp_regex: re = \
            r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}'
        arbitrary_timestamp: str = "2021-06-07_12-34-56"
        settings: Settings = settings_fixture
        settings.RUN_TIMESTAMP = arbitrary_timestamp
        assert re.match(expected_timestamp_regex, settings.RUN_TIMESTAMP), \
            "Format of run timestamp set is not as expected."

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
    def test_load_config_file_check_metadata(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with custom metadata file works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_metadata_path: str = "metadata/metadata.yml"
        settings: Settings = settings_custom_config_fixture
        assert settings.METADATA.absolute() == \
               Path(expected_metadata_path).absolute(), \
               "Value of metadata path set is not correct."

    @pytest.mark.ci
    def test_load_config_file_check_output_folder(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with custom output folder works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_output_folder: str = "output_folder"
        settings: Settings = settings_custom_config_fixture
        assert settings.OUTPUT_FOLDER.absolute() == \
               Path(expected_output_folder).absolute(), \
               "Value of output folder set is not correct."

    @pytest.mark.ci
    def test_load_config_file_check_output_format(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with custom output format works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_output_format: SupportedOutputFormat = \
            SupportedOutputFormat.SVG
        settings: Settings = settings_custom_config_fixture
        assert settings.OUTPUT_FORMAT == expected_output_format, \
               "Value of output format set is not correct."

    @pytest.mark.ci
    def test_load_config_file_check_scripts_folder(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with custom scripts folder works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_script_folder: str = "scripts_folder"
        settings: Settings = settings_custom_config_fixture
        assert settings.SCRIPT_FOLDER.absolute() == \
               Path(expected_script_folder).absolute(), \
               "Value of scripts folder set is not correct."

    @pytest.mark.ci
    def test_load_config_file_check_scripts_names_list_datatype(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with script names of type list works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        settings: Settings = settings_custom_config_fixture
        assert isinstance(settings.SCRIPT_NAMES, List), \
               "Datatype of script names is not a list."

    @pytest.mark.ci
    def test_load_config_file_check_scripts_names_list_count(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with custom script names list works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_script_names_count: int = 1
        settings: Settings = settings_custom_config_fixture
        assert len(settings.SCRIPT_NAMES) == expected_script_names_count, \
               "List size of script names is not as expected."

    @pytest.mark.ci
    def test_load_config_file_check_scripts_names_list_entry(
            self, settings_custom_config_fixture: Settings):
        """
        Tests that loading a config file with custom script name works.

        Args:
            settings_custom_config_fixture (Settings):
                New Settings object containing all settings of an analysis run.
        """
        expected_script_name: str = "example_script"
        settings: Settings = settings_custom_config_fixture
        assert settings.SCRIPT_NAMES[0] == expected_script_name, \
               "First element of list of script names is not as expected."
