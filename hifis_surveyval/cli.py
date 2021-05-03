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

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/7/>`_.
    There is also a very helpful `tutorial video
    <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: hifis_surveyval.cli
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging

import click
import pkg_resources

from hifis_surveyval.core import util
from hifis_surveyval.core.dispatch import Dispatcher
from hifis_surveyval.core.settings import Settings
from hifis_surveyval.hifis_surveyval import HIFISSurveyval

settings: Settings = Settings()


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    default=0,
    show_default=True,
    help="Enable verbose output. "
    "Increase verbosity by setting this option up to 3 times.",
)
def cli(verbose: int) -> None:
    """
    Analyze a given CSV file with a set of independent python scripts.

    Args:
        verbose (int): Indicates the verbosity level on the CLI.
    """
    # NOTE that click takes above documentation for generating help text
    # Thus the documentation refers to the application per se and not the
    # function (as it should)

    settings.set_verbosity(verbose)
    if not settings.VERBOSITY == logging.ERROR:
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )


@cli.command()
def version() -> None:
    """Get the library version."""
    version_string: str = pkg_resources.require("hifis_surveyval")[0].version
    click.echo(click.style(f"{version_string}", bold=True))


@cli.command()
@click.option(
    "--config",
    "-c",
    is_flag=True,
    show_default=True,
    help="Create a default config as file. "
    "Overwrites any existing configuration file.",
)
@click.option(
    "--script",
    "-s",
    is_flag=True,
    show_default=True,
    help="Create an example script in the given script folder. "
    "Overwrites any existing example script file.",
)
def init(config: bool, script: bool) -> None:
    """
    Create a configuration file and an example script in the default locations.

    It will overwrite any existing configuration and example file.

    Args:
        config (bool): Indicates whether to create a configuration file.
        script (bool): Indicates whether to create an example analysis
                       script.
    """
    if not config and not script:
        config = True
        script = True

    if config:
        settings.create_default_config_file()
    if script:
        util.create_example_script(settings)


@click.argument("file_name", type=click.File(mode="r"))
@cli.command()
def analyze(file_name: click.File) -> None:
    """
    Read the given files into global data and metadata objects.

    If the data file can not be parsed by Pandas, an error will be printed and
    the program will abort.
    If the metadata file can not be parsed, an error will be printed and
    the program will abort.

    Args:
        file_name (click.File): File that contains all data for the analysis.
    """
    settings.load_config_file()

    surveyval: HIFISSurveyval = HIFISSurveyval(settings=settings)
    surveyval.prepare_environment()
    logging.info(f"Analyzing file {file_name.name}")
    surveyval.analyze(data_file=file_name)

    dispatcher: Dispatcher = Dispatcher(surveyval=surveyval)
    dispatcher.discover()
    dispatcher.load_all_modules()
