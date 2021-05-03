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
This is the test module for the project's command-line interface module.

To learn more about testing Click applications, visit the link below.
http://click.pocoo.org/5/testing/
"""
import os
import shutil
from pathlib import Path

import pkg_resources
import pytest

# fmt: on
from click.testing import CliRunner, Result

# fmt: off
from hifis_surveyval import cli
from hifis_surveyval.core.settings import Settings


@pytest.fixture(scope='function')
def settings():
    """Set up and tear down for testing settings."""
    settings: Settings = Settings()
    shutil.rmtree(settings.SCRIPT_FOLDER, ignore_errors=True)
    try:
        os.remove(settings.CONFIG_FILENAME)
    except FileNotFoundError:
        pass

    yield settings

    shutil.rmtree(settings.SCRIPT_FOLDER, ignore_errors=True)
    try:
        os.remove(settings.CONFIG_FILENAME)
    except FileNotFoundError:
        pass


def test_version_displays_library_version():
    """
    Arrange/Act: Run the `version` subcommand.

    Assert: The output matches the library version.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["version"])
    version_ = pkg_resources.require("hifis_surveyval")[0].version
    assert (version_
            in result.output.strip()
            ), "Version number should match library version."


def test_verbose_output():
    """
    Arrange/Act: Run the `version` subcommand with the '-v' flag.

    Assert: The output indicates verbose logging is enabled.
    """
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli.cli, ["-v", "version"])
    assert ("Verbose" in result.output.strip()), \
        "Verbose logging should be indicated in output."


def test_init_config(settings):
    """
    Arrange/Act: Run the `init -c` subcommand.

    Assert: The default config file is created.
    """
    runner: CliRunner = CliRunner()
    runner.invoke(cli.cli, ["init", "-c"])
    assert (Path(settings.CONFIG_FILENAME).exists()), \
        "The default config file should be created at default path."


def test_init_example_script(settings):
    """
    Arrange/Act: Run the `init -s` subcommand.

    Assert: The default script folder is created.
    Assert: The example script file is created.
    """
    runner: CliRunner = CliRunner()
    runner.invoke(cli.cli, ["init", "-s"])
    assert (Path(settings.SCRIPT_FOLDER).is_dir()), \
        "The default script folder should be created at default path."
    assert (Path(f"{settings.SCRIPT_FOLDER}/example_script.py").exists()), \
        "The default config file should be created at default path."


def test_init(settings):
    """
    Arrange/Act: Run the `init` subcommand.

    Assert: The default config file is created.
    Assert: The default script folder is created.
    Assert: The example script file is created.
    """
    runner: CliRunner = CliRunner()
    runner.invoke(cli.cli, ["init"])
    assert (Path(settings.CONFIG_FILENAME).exists()), \
        "The default config file should be created at default path."
    assert (Path(settings.SCRIPT_FOLDER).is_dir()), \
        "The default script folder should be created at default path."
    assert (Path(f"{settings.SCRIPT_FOLDER}/example_script.py").exists()), \
        "The default config file should be created at default path."
