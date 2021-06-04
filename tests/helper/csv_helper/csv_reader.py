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

"""Offering CSV helper methods for test cases in test case suites."""

import csv
from typing import List


class CsvReader:
    """Provides helper methods to handle CSV files."""

    @classmethod
    def read_in_data_file(cls, file_path: str) -> List[List[str]]:
        """
        Read in test data from CSV file.

        Args:
            file_path (str):
                File name of a data CSV file to be read in.

        Returns:
            List[List[str]]:
                New object containing test data read in from CSV file.
        """
        csv_data: List[List[str]] = []
        with open(file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_ALL)
            for row in reader:
                csv_data.append(row)
        return csv_data
