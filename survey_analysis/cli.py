#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.
    There is also a very helpful `tutorial video
    <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: survey_analysis.cli
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
import sys
from pathlib import Path

import click
import pandas

from survey_analysis import dispatch
from survey_analysis import globals
from .__init__ import __version__


@click.group()
@click.option("--verbose", "-v",
              count=True,
              default=0,
              help="Enable verbose output. "
                   "Repeat up to 3 times for increased effect")
@click.option("--scripts", "-s",
              default="scripts",
              help="Select the folder containing analysis scripts")
def cli(verbose: int, scripts: str):
    """
    Analyze a given CSV file with a set of independent python scripts.
    """
    # NOTE that click takes above documentation for generating help text
    # Thus the documentation refers to the application per se and not the
    # function (as it should)
    set_verbosity(verbose)

    # TODO check if the script folder exists
    logging.info(f"Selected script folder {scripts}")
    globals.settings.script_folder = Path(scripts)
    sys.path.insert(0, scripts)


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@click.argument("file_name", type=click.File(mode="r"))
def analyze(file_name):
    """
    Read the given data file into a global data object.

    If the file can not be parsed by Pandas, an error will be printed and
    the program will abort.
    """
    logging.info(f"Analyzing file {file_name.name}")
    try:
        frame: pandas.DataFrame = pandas.read_csv(file_name)
        logging.debug(str(frame))

        # Put the Data Frame into the global container
        globals.dataContainer.set_raw_data(frame)
    except IOError:
        logging.error("Could not parse the given file as CSV")
        exit(1)

    dispatcher = dispatch.Dispatcher(globals.settings.script_folder)

    dispatcher.load_module("dummy")


def set_verbosity(verbose_count: int):
    """
    Interpret the verbosity option count and set the log levels accordingly
    The used log level is also stored in the settings.

    Args:
        verbose_count: the amount of verbose option triggers
    """

    verbosity_options = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG
        ]

    max_index = len(verbosity_options) - 1

    # Clamp verbose_count to accepted values
    # Note that it shall not be possible to unset the verbosity.
    option_index = 0 if verbose_count < 0 \
        else max_index if verbose_count > max_index \
        else verbose_count

    new_level: int = verbosity_options[option_index]
    logging.basicConfig(level=new_level)
    globals.settings.verbosity = new_level

    if not new_level == logging.ERROR:
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
                )
            )
