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

"""Offering data structure helper methods for series and data frame objects."""

from pandas import Series, DataFrame
from typing import List, Dict, Union


class DataStructureCreator:
    """Provides helper methods to create data structure objects."""

    @staticmethod
    def create_series_from_dict(
            data: Dict[str, Union[bool, str, int, float]],
            data_column_name: str, index_column_name: str = "id") -> Series:
        """
        Create Series object from data structure dictionary.

        Args:
            data (Dict[str, Union[bool, str, int, float]]):
                Data structure to be passed in to be used as Series data.
            data_column_name (str):
                Name of the data column.
            index_column_name (str):
                Name of the index column, defaults to "id".

        Returns:
            Series:
                A newly created Series containing the data passed in.
        """
        series: Series = Series(data=data)
        series.name = data_column_name
        series.index.name = index_column_name
        return series

    @staticmethod
    def create_dataframe_from_dict(
            data: Dict[str, List[Union[bool, str, int, float]]],
            index_column_name: str = "id") -> DataFrame:
        """
        Create DataFrame object from data structure dictionary.

        Args:
            data (Dict[str, List[Union[bool, str, int, float]]]):
                Data structure to be passed in to be used as Series data.
            index_column_name (str):
                Name of the index column, defaults to "id".

        Returns:
            DataFrame:
                A newly created DataFrame containing the data passed in.
        """
        data_frame: DataFrame = DataFrame(data=data)
        data_frame.set_index(keys=[index_column_name], inplace=True)
        return data_frame
