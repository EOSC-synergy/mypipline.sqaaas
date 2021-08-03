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

"""Offering DataContainer helper methods for loading DataContainer objects."""

from typing import Union, List, Optional

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.models.mixins.yaml_constructable import YamlList, YamlDict
from tests.helper.csv_helper.csv_reader import CsvReader
from tests.helper.yaml_helper.yaml_reader import YamlReader


class DataContainerLoader:
    """Provides helper methods to handle DataContainer objects."""

    @staticmethod
    def prepare_data_container(yaml_metadata_file_path: str,
                               csv_data_file_path: Optional[str] = None) \
            -> DataContainer:
        """
        Load a YAML file and a CVS file into a DataContainer object.

        Args:
            yaml_metadata_file_path (str):
                File name of a metadata YAML file to be read in.
            csv_data_file_path (str):
                File name of a data CSV file to be read in.

        Returns:
            DataContainer:
                A newly created DataContainer containing metadata from YAML
                file and optionally data from CSV file.
        """
        data_container: DataContainer = DataContainer(Settings())
        metadata: Union[YamlList, YamlDict] = YamlReader.read_in_yaml_file(
            yaml_metadata_file_path
        )
        data_container.load_metadata(metadata)
        if csv_data_file_path:
            csv_data: List[List[str]] = CsvReader.read_in_data_file(
                csv_data_file_path
            )
            data_container.load_survey_data(csv_data)
        return data_container
