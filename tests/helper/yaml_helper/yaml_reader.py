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

"""Offering YAML helper methods for test cases in test case suites."""

import yaml

from hifis_surveyval.models.mixins.yaml_constructable import YamlDict


class YamlReader:
    """Provides helper method to handle YAML files."""

    @classmethod
    def read_in_yaml_file(cls, yaml_file_path: str) -> YamlDict:
        """
        Read in a YAML file and create a dictionary out of it.

        Args:
            yaml_file_path (str):
                File name of a YAML file to be read in.

        Returns:
            YamlDict:
                Dictionary of a read-in YAML file.
        """
        metadata_yaml: YamlDict = {}
        with open(yaml_file_path, 'r') as file:
            metadata_yaml = yaml.load(stream=file, Loader=yaml.FullLoader)
        return metadata_yaml
