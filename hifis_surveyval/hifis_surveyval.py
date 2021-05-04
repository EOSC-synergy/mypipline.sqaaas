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
from typing import Dict, List, Set

import click
import pandas
from pandas import DataFrame, concat

from hifis_surveyval.core.metadata import MetaDataHandler
from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.models.question import AbstractQuestion, Question
from hifis_surveyval.plotting.matplotlib_plotter import MatplotlibPlotter
from hifis_surveyval.printing.printer import Printer


class HIFISSurveyval:
    """
    Main class for all functionalities.

    Also serves as data storage.
    """

    def __init__(self, settings: Settings):
        """Initialize HIFISSurveyval."""
        #: A global copy-on-read container for providing the survey data
        #: to the analysis functions
        self.dataContainer: DataContainer = DataContainer()

        #: All the survey questions and their associated answers
        self.survey_questions: Dict[str, AbstractQuestion] = {}

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
        sys.path.insert(0, self.settings.SCRIPT_FOLDER)

        # create folder to output the results
        if self.settings.ANALYSIS_OUTPUT_PATH is not None:
            if not self.settings.ANALYSIS_OUTPUT_PATH.exists():
                self.settings.ANALYSIS_OUTPUT_PATH.mkdir(parents=True)

    def analyze(self, data_file: click.File) -> None:
        """
        Run the analysis.

        Args:
            data_file (click.File): File that contains the data for the
                                    analysis.

        Raises:
            IOError: Exception thrown if data could not be parsed.
            IOError: Exception thrown if metadata could not be parsed.
        """
        try:
            frame: DataFrame = pandas.read_csv(
                data_file,
                true_values=self.settings.TRUE_VALUES,
                false_values=self.settings.FALSE_VALUES,
            )

            logging.debug("\n" + str(frame))

            # Put the Data Frame into the global container
            self.dataContainer.set_raw_data(frame)
        except IOError:
            logging.error("Could not parse the given file as CSV")
            exit(1)

        logging.info(f"Attempt to load metadata from {self.settings.METADATA}")

        # Load survey metadata from given YAML file.
        # register metadata handler
        metadata_handler: MetaDataHandler = MetaDataHandler(
            data_source=self.dataContainer
        )
        try:
            self.survey_questions = (
                metadata_handler.construct_questions_from_metadata(
                    self.settings.METADATA
                )
            )

            # When debugging, print all parsed Questions
            if self.settings.VERBOSITY == logging.DEBUG:
                logging.debug("Parsed Questions:")
                for question in self.survey_questions.values():
                    logging.debug(question)

            metadata_handler.fetch_participant_answers()
        except IOError:
            logging.error("Could not parse the metadata file as YAML.")
            exit(1)

    def question_ids_to_dataframe(
        self, question_ids: Set[str] = set()
    ) -> DataFrame:
        """
        Combine multiple questions into a single pandas DataFrame.

        It replaces all question collections with their
        sub questions and ignores all invalid identifiers.

        In case the argument is omitted, all questions will be loaded.

        Args:
            question_ids (Set[str]): A list containing question IDs as string.

        Returns:
            DataFrame: A joint data frame containing the columns for each
                       question_id.
        """
        if not question_ids:  # if arg question_ids is empty, use full list
            question_ids = set(self.survey_questions.keys())

        questions: Set[Question] = set()

        for question_id in question_ids:
            try:
                question: AbstractQuestion = self.survey_questions[question_id]
                item: List[Question]
                for item in question.flatten():
                    questions.add(item)
            except KeyError:
                logging.error(
                    f"When constructing data frame from multiple questions: "
                    f"{question_id} is not a valid ID"
                )
                continue

        item: Question
        questions_as_dataframe: DataFrame = concat(
            list(item.as_series(filter_invalid=False) for item in questions),
            axis=1,
            join="outer",
        )

        return questions_as_dataframe
