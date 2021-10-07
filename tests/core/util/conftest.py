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

from hifis_surveyval.data_container import DataContainer
from tests.helper.data_container_helper.data_container_loader import \
    DataContainerLoader


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
