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

import click
import pandas

from survey_analysis import dispatch
from survey_analysis import globals
from .__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Settings(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbosity: int = 0
        self.script_folder: str = "scripts"


# pass_settings is a decorator for functions that pass 'Settings' objects.
#: pylint: disable=invalid-name
pass_settings = click.make_pass_decorator(Settings, ensure=True)


@click.group()
@click.option("--verbose", "-v",
              count=True,
              help="Enable verbose output. "
                   "Repeat up to 4 times for increased effect")
@click.option("--scripts", "-s",
              default="scripts.",
              help="Select the folder containing analysis scripts")
@pass_settings
def cli(settings: Settings, verbose: int, scripts: str):
    """
    Analyze a given CSV file with a set of independent python scripts.
    """
    # NOTE that click takes above documentation for generating help text
    # Thus the documentation refers to the application per se and not the
    # function (as it should)

    # Clamp verbosity to accepted values
    if verbose < 0:
        verbose = 0
    elif verbose > 4:
        verbose = 4

    settings.verbosity = verbose

    # Use the verbosity count to determine the logging level
    new_level = LOGGING_LEVELS.get(verbose, logging.DEBUG)
    logging.basicConfig(level=new_level)

    if verbose:
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
                )
            )

    # TODO check if the script folder exists
    logging.log(level=logging.INFO,
                msg=f"Selected script folder {scripts}")
    settings.script_folder = scripts
    sys.path.insert(0, scripts)


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@click.argument("file_name", type=click.File(mode="r"))
@pass_settings
def analyze(settings: Settings, file_name):
    """
    Read the given data file into a global data object.

    If the file can not be parsed by Pandas, an error will be printed and
    the program will abort.
    """
    logging.log(level=logging.INFO,
                msg=f"Analyzing file {file_name.name}")
    try:
        frame: pandas.DataFrame = pandas.read_csv(file_name)
        logging.log(level=logging.DEBUG,
                    msg=str(frame))

        # Put the Data Frame into the global container
        globals.dataContainer.set_raw_data(frame)
    except IOError:
        logging.log(level=logging.ERROR,
                    msg="Could not parse the given file as CSV")
        exit(1)

    dispatcher = dispatch.Dispatcher(settings.script_folder)
    dispatcher.load_module("dummy")
