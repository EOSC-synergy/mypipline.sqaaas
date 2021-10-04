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

from typing import List, Union

import pytest

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.models.mixins.yaml_constructable import YamlDict, YamlList
from tests.helper.csv_helper.csv_reader import CsvReader
from tests.helper.data_container_helper.data_container_loader import \
    DataContainerLoader
from tests.helper.yaml_helper.yaml_reader import YamlReader


@pytest.fixture(scope="function")
def data_container_fixture() -> DataContainer:
    """
    Get a new DataContainer object.

    Returns:
        DataContainer:
            New DataContainer object containing an empty DataFrame object.
    """
    return DataContainer(Settings())


@pytest.fixture(scope="function")
def read_in_metadata_yaml_file(
    metadata_yaml_file_path: str,
) -> Union[YamlList, YamlDict]:
    """
    Read in a YAML file and create a dictionary out of it.

    Args:
        metadata_yaml_file_path (str):
            File name of a metadata YAML file to be read in.

    Returns:
        YamlDict:
            Dictionary of a read-in metadata YAML file.
    """
    metadata_yaml: Union[YamlList, YamlDict] = YamlReader.read_in_yaml_file(
        metadata_yaml_file_path
    )
    return metadata_yaml


@pytest.fixture(scope="function")
def read_in_data_csv_file(test_data_csv_file_path: str) -> List[List[str]]:
    """
    Read in test data from CSV file.

    Args:
        test_data_csv_file_path (str):
            File name of a data CSV file to be read in.

    Returns:
        List[List[str]]:
            New object containing test data read in from CSV file.
    """
    csv_data: List[List[str]] = CsvReader.read_in_data_file(
        test_data_csv_file_path
    )
    return csv_data


@pytest.fixture(scope="function")
def data_container_load_metadata_fixture(metadata_yaml_file_path: str) \
        -> DataContainer:
    """
    Read in a YAML file and create a dictionary out of it.

    Args:
        metadata_yaml_file_path (str):
            File name of a metadata YAML file to be read in.

    Returns:
        DataContainer:
            DataContainer containing metadata from YAML file.
    """
    data_container: DataContainer = \
        DataContainerLoader.prepare_data_container(metadata_yaml_file_path)
    return data_container


@pytest.fixture(scope="function")
def data_container_load_metadata_and_data_fixture(
    metadata_yaml_file_path: str, test_data_csv_file_path: str
) -> DataContainer:
    """
    Read in a YAML file and create a dictionary out of it.

    Args:
        metadata_yaml_file_path (str):
            File name of a metadata YAML file to be read in.
        test_data_csv_file_path (str):
            File name of a metadata CSV file to be read in.

    Returns:
        DataContainer:
            DataContainer containing metadata from YAML file and data from
            CSV file.
    """
    data_container: DataContainer = \
        DataContainerLoader.prepare_data_container(metadata_yaml_file_path,
                                                   test_data_csv_file_path)
    return data_container


@pytest.fixture(scope="function")
def settings_fixture() -> Settings:
    """
    Get a new Settings object.

    Returns:
        Settings:
            New Settings object containing settings of an analysis run.
    """
    return Settings()
