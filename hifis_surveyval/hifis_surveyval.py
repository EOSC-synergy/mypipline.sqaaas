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

"""This project is used to develop analysis scripts for surveys."""
import logging
import sys
from csv import reader
from pathlib import Path

import yaml

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.plotting.matplotlib_plotter import MatplotlibPlotter
from hifis_surveyval.printing.printer import Printer


class HIFISSurveyval:
    """
    Main class for all functionalities.

    Also serves as data storage.
    """

    def __init__(self, settings: Settings):
        """
        Initialize HIFISSurveyval.

        Args:
              settings:
                A Settings container to store the setup configuration
                in. It will be populated with the related settings during the
                initialization of the HIFISSurveyval object.
        """
        #: A global copy-on-read container for providing the survey data
        #: to the analysis functions
        self.dataContainer: DataContainer = DataContainer()

        #: The settings storage
        self.settings: Settings = settings

        # register plotter
        self.plotter: MatplotlibPlotter = MatplotlibPlotter(
            output_format=self.settings.OUTPUT_FORMAT,
            output_path=self.settings.ANALYSIS_OUTPUT_PATH,
        )

        # register printer
        self.printer: Printer = Printer()

    def prepare_environment(self) -> None:
        """
        Prepare the runtime environment.

        * setting sys path to load scripts
        * creating output folder to save images
        """
        # set syspath to later on load scripts
        sys.path.insert(0, str(self.settings.SCRIPT_FOLDER.resolve()))

        # create folder to output the results
        if self.settings.ANALYSIS_OUTPUT_PATH is not None:
            if not self.settings.ANALYSIS_OUTPUT_PATH.exists():
                self.settings.ANALYSIS_OUTPUT_PATH.mkdir(parents=True)

    def load_all_data(self, data_file: Path) -> None:
        """
        Populate the data container with the survey results and metadata.

        Args:
            data_file (click.File): File that contains the data for the
                                    analysis.

        Raises:
            IOError: Exception thrown if data could not be parsed.
            IOError: Exception thrown if metadata could not be parsed.
        """
        # Load the metadata
        logging.info(f"Attempt to load metadata from {self.settings.METADATA}")

        with self.settings.METADATA.open(mode="r") as metadata_io_stream:
            metadata_yaml = yaml.safe_load(metadata_io_stream)
            self.dataContainer.load_metadata(metadata_yaml)

        #  Load the actual survey data
        with data_file.open(mode="r") as data_io_stream:
            csv_reader = reader(data_io_stream)
            self.dataContainer.load_survey_data(csv_data=list(csv_reader))
