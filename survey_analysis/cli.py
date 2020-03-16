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

import click
import pandas

from .__init__ import __version__
from .data import initialize_global_data

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbosity: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v",
              count=True,
              help="Enable verbose output. "
                   "Repeat up to 4 times for increased effect")
@pass_info
def cli(info: Info, verbose: int):
    """
    Set the output verbosity.

    If an invalid value is passed, it will default to the maximum verbosity.
    """
    assert (verbose >= 0), "Verbosity option parsed into an invalid value"
    info.verbosity = verbose

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


@cli.command()
@pass_info
def hello(_: Info):
    """Say 'hello' to the nice people."""
    click.echo(f"survey_analysis says 'hello'")


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
    logging.log(level=logging.INFO,
                msg="Analyzing file {name}".format(name=file_name.name))
    try:
        frame: pandas.DataFrame = pandas.read_csv(file_name)
        logging.log(level=logging.DEBUG,
                    msg=str(frame))

        # Put the Data Frame into the global container
        initialize_global_data(frame)
    except IOError:
        logging.log(level=logging.ERROR,
                    msg="Could not parse the given file as CSV")
        exit(1)
