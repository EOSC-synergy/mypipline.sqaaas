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

"""Provide pytest test cases for module util."""
import numpy as np
import pytest
from pandas import DataFrame

from hifis_surveyval.core import util

from hifis_surveyval.data_container import DataContainer
from tests.helper.data_structure_helper.data_structure_creator import \
    DataStructureCreator


class TestModuleUtil(object):
    """
    Tests util operations.

    Basic tests for module util are performed in unit test methods of
    this class.
    """

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/core/util/fixtures/"
                "metadata-two-question-collections.yml",
                "tests/core/util/fixtures/test_data_for_module_util.csv",
            ]
        ],
    )
    def test_filter_and_group_series_works(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that grouping and filtering given two series works.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        dataframe_dict = \
            {"id": ["1", "2", "3", "4", "5", "6"],
             "Option1": [True, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN],
             "Option2": [np.NaN, True, np.NaN, np.NaN, np.NaN, np.NaN],
             "Option3": [np.NaN, np.NaN, True, None, np.NaN, np.NaN]}
        expected_frame: DataFrame = DataStructureCreator.\
            create_dataframe_from_dict(dataframe_dict)

        series_q001_loaded = data_container_load_metadata_and_data_fixture.\
            question_for_id("Q001/SQ001").as_series()
        series_q002_loaded = data_container_load_metadata_and_data_fixture.\
            question_for_id("Q002/SQ001").as_series()
        actual_frame = \
            util.filter_and_group_series(series_q001_loaded,
                                         series_q002_loaded.dropna())
        # Make sure that expected and actual DataFrames are equal.
        assert actual_frame.equals(expected_frame), \
            "Expected and actual DataFrames are not equal."

    @pytest.mark.ci
    @pytest.mark.parametrize(
        "metadata_yaml_file_path,test_data_csv_file_path",
        [
            [
                "tests/core/util/fixtures/"
                "metadata-two-question-collections.yml",
                "tests/core/util/fixtures/test_data_for_module_util.csv",
            ]
        ],
    )
    def test_filter_and_group_series_raises_value_error_on_nan_values(
        self, data_container_load_metadata_and_data_fixture: DataContainer
    ) -> None:
        """
        Tests that ValueError is raised if group-by series contains NaN values.

        Args:
            data_container_load_metadata_and_data_fixture (DataContainer):
                Fixture that provides a DataContainer containing metadata and
                data.
        """
        series_q001_loaded = data_container_load_metadata_and_data_fixture.\
            question_for_id("Q001/SQ001").as_series()
        series_q002_loaded = data_container_load_metadata_and_data_fixture.\
            question_for_id("Q002/SQ001").as_series()
        # Make sure that ValueError is raised when facing NaN values in
        # group-by series.
        with pytest.raises(ValueError):
            util.filter_and_group_series(series_q001_loaded,
                                         series_q002_loaded)
