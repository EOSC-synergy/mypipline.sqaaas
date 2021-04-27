<!--
hifis-surveyval
Framework to help developing analysis scripts for the HIFIS Software survey.

SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
-->

# HIFIS-Surveyval

This project is used to develop analysis scripts for the HIFIS Software survey.

## Table of Content

* [Installation](#installation)
* [Getting Started](#getting-started)
* [Development](#development)
* [Start Analysis from Command-Line-Interface](#start-analysis-from-command-line-interface)
* [Contribute with Own Analysis Scripts](#contribute-with-own-analysis-scripts)
* [Resources](#resources)
* [License](#license)

## Getting Started

The project's documentation contains a section to help you
[get started](TODO) 
as a developer or user of the analysis scripts.

## Installation
To install the package locally, you can either use 
[poetry](https://python-poetry.org/)
or `pip`.

### Using pip

```shell
pip install hifis-surveyval
```

After the installation, you can use the tool from the command line with 
`hifis-surveyval --help`.

### Using poetry

```shell
git clone $PATH_TO_THIS_PROJECT
cd hifis-surveyval
poetry install --no-dev
```

After the installation, you can use the tool from the command line with 
`poetry run hifis-surveyval --help`
The following documentation references the pip installation.
You can use the same commands with a poetry installation, if you prefix your 
commands with `poetry run COMMAND`.

## Development
If you want to actively contribute changes to the project, you are required to
also install the development packages.
Therefore, use below extended installation options.

```shell
poetry install
```

Note: Please make sure that a _Python virtual environment_ is created
beforehand in the project folder:

```shell
poetry env use python3
```

_Poetry_ installs some packages that are required for performing quality checks.
Usually they are also performed via GitLab CI, but can also be executed locally.

It is common practice to run some checks locally before pushing them online.
Therefore, execute below commands:
```console
$ # Order your imports
$ isort -rc .
$ make lint
```

## Start Analysis from Command-Line-Interface

The survey analysis package is a program to be executed on the
Command-Line-Interface (CLI).

### Quick Start Example: Run Analysis

In order to run the survey analysis you need to copy the data-CSV-file 
for example from the 
[wiki page](https://gitlab.hzdr.de/hifis/survey-about-current-development-practice/-/wikis/home) 
of the associated GitLab project 
[Survey about current Development Practice](https://gitlab.hzdr.de/hifis/survey-about-current-development-practice)
into a central location like the [data/](data/) sub-folder of your local python 
project and tell the program the path to that data file.

Now you can do the following to start the survey analysis from the CLI:

```shell script
hifis-surveyval init
hifis-surveyval analyze data/<data_file_name>.csv
```

It creates an initial configuration file containing all relevant configuration
options and thereby tells the program when doing the analysis 
where to find the analysis scripts, the _metadata_-file as well as 
the _data_-file to be taken into account for the analysis.
Be aware that these folders _scripts_, _metadata_ and _data_ need to exist.
The output is then put into a folder _output_ if not specified differently.

**Caution:** 
Depending on the Operating System used an issue with the file 
encoding might occur.
There might be data-CSV-files around which are encoded with `UTF-8-BOM`
which causes errors when read in on Windows OS.
In this case you need to change the encoding to `UTF-8` before running
the survey analysis.

### Flags

The program accepts a couple of flags:

1. Help flag
2. Verbosity flag

#### Help flag

Calling the program with the _help_-flag is the first thing to do
when being encountered with this program.
It outputs a so-called _Usage_-message to the CLI:

```shell script
$ hifis-surveyval --help
Usage: hifis-surveyval [OPTIONS] COMMAND [ARGS]...

  Analyze a given CSV file with a set of independent python scripts.

Options:
  -v, --verbose  Enable verbose output. Increase verbosity by setting this
                 option up to 3 times.  [default: 0]

  --help         Show this message and exit.

Commands:
  analyze  Read the given files into global data and metadata objects.
  init     Create a default configuration in a file called hifis-surveyval.yml.
  version  Get the library version.
```

#### Verbosity flag

The _verbosity_-flag can be provided in order to specify the verbosity
of the output to the CLI.
This flag is called `--verbose` or `-v` for short:

```shell script
hifis-surveyval --verbose <COMMAND>
```
```shell script
hifis-surveyval -v <COMMAND>
```

The verbosity of the output can be increased even more 
by duplicating the flag `--verbose` or `-v` up to two times:

```shell script
hifis-surveyval --verbose --verbose --verbose <COMMAND>
```
```shell script
hifis-surveyval -vvv <COMMAND>
```

### Commands

There are three different commands implemented which come with different
flags and parameters:

1. Command _version_
2. Command _init_
3. Command _analyze_

#### Command _version_
 
The `version` command outputs the version number of this CLI-program like so:

```shell script
hifis-surveyval version
```

#### Command _init_

Before you are ready to start the analysis you need to create the
configuration file that is by default named _hifis-surveyval.yml_.
You can do that initially by issuing the _init_ command:

```shell script
hifis-surveyval init
```

This file contains information of the following type:

```
METADATA: metadata/meta.yml
OUTPUT_FOLDER: output
OUTPUT_FORMAT: PNG
SCRIPT_FOLDER: scripts
SCRIPT_NAMES: []
```

First of all, each analysis needs metadata about the questions asked in the
survey and answers that participants may give.
This metadata file is by default located in a folder called _metadata_.

Second, you may specify the output folder which is named _output_ by default.

Third, you may prefer a specific output format like _PNG_, _JPEG_, _SVG_ or 
_SCREEN_.
The default value is _PNG_.
Note: Be aware that other output formats may be created, which depends largely
upon the implementation of the analysis scripts.

Fourth, you may specify the folder which contains the analysis scripts, which
is the _scripts_ folder by default.

Finally, you may select a subset of the analysis scripts available as a list
that ought to be executed.
This list is empty by default, which means that all scripts are executed.

#### Command _analyze_

The more interesting command is the `analyze` command
which comes with a _data_-parameter.
The _data_-parameter can _not_ be omitted and need to be given explicitly
in order to be able to start the analysis.
This is an example of how to do the analysis:

```shell script
hifis-surveyval analyze data/<data_file_name>.csv
```

## Contribute with Own Analysis Scripts

### Essential Criteria for Developing Own Analysis Scripts

As you might have read in the previous sections the actual analysis scripts 
reside in a specific folder called `scripts`.
All scripts in that folder will be automatically discovered by the package 
`hifis-surveyval` when running the analysis.
In order that the program recognizes the scripts in that folder as
analysis scripts they need to fulfill the following two criteria:

1. The filename need to end on `.py`.
2. The file need to contain a function called `run` without any parameters.

```python
"""
A dummy script for testing the function dispatch

.. currentmodule:: hifis_surveyval.scripts.dummy
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

def run():
    print("Example Script")
```

If both criteria are satisfied the program will execute the `run`-functions
of the analysis scripts in an arbitrary order.

### File-System Structure of Core Component

```shell script
$ tree hifis_surveyval/
hifis_surveyval/
├── answer.py
├── cli.py
├── core
│   ├── environment.py
│   ├── __init__.py
│   └── settings.py
├── data.py
├── dispatch.py
├── globals.py
├── __init__.py
├── metadata.py
├── plot.py
├── question.py
└── util.py
```

## Resources

Below are some handy resource links:

* [Project Documentation](TODO)
* [Click](https://click.palletsprojects.com/en/7.x) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

## License

Copyright © 2021 HIFIS Software <support@hifis.net>

This work is licensed under the following license(s):
* Everything else is licensed under [GPL-3.0-or-later](LICENSES/GPL-3.0-or-later.txt)

Please see the individual files for more accurate information.

> **Hint:** We provided the copyright and license information in accordance to the [REUSE Specification 3.0](https://reuse.software/spec/).
