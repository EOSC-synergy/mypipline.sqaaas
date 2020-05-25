# HIFIS Survey Analysis 2020

This project is used to develop analysis scripts for the HIFIS Software survey.

## Getting Started

The project's documentation contains a section to help you
[get started](TODO) as a developer or
user of the analysis scripts.

## Installation
To install the package locally, you can either use [pipenv](https://github.com/pypa/pipenv)
or `pip`. It is common practice to create an individual virtual environment.
In case you're using pipenv, pipenv cares about the creation of the environment.
Refer to the _Using Pip_ installation instruction to see how to create a 
virtual environment manually.

- Using Pipenv:
  ```console
  $ pipenv install
  $ pipenv run survey_analysis --help
  ```
- Using Pip:
  ```console
  $ python3 -m venv .venv
  $ source .venv/bin/activate
  $ pip install -e .
  ```

## Development
If you want to actively contribute changes to the project, you are required to
also install the development packages.
Therefore, use below extended installation options.
- Using Pipenv:
  ```console
  $ pipenv install --dev
  $ pipenv run survey_analysis --help
  ```
- Using Pip:
  ```console
  $ python3 -m venv .venv # Only required if not already done before.
  $ source .venv/bin/activate
  $ pip install -e .[dev]
  ```

This installs some packages that are required for performing quality checks.
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
$ pipenv run survey_analysis analyze data/<data_file_name>.csv
```

It tells the program that you would like to do the analysis,
where to find the analysis scripts, the _metadata_-file as well as 
the _data_-file to be taken into account for the analysis.

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
3. Scripts flag
4. Names flag
5. Output Format flag

#### Help flag

Calling the program with the _help_-flag is the first thing to do
when being encountered with this program.
It outputs a so-called _Usage_-message to the CLI:

```shell script
$ pipenv run survey_analysis --help
Usage: survey_analysis [OPTIONS] COMMAND [ARGS]...

  Analyze a given CSV file with a set of independent python scripts.

Options:
  -v, --verbose             Enable verbose output. Increase verbosity by
                            setting this option up to 3 times.  [default: 0]

  -s, --scripts TEXT        Select the folder containing analysis scripts.
                            [default: scripts]

  -n, --names TEXT          Select the script names contained in the scripts
                            folder as comma-separated list (omitting file
                            endings) which should be executed.  [default: all]

  -f, --output-format TEXT  Designate output format. Supported values are:
                            SCREEN, PDF, PNG, SVG.  [default: screen]

  --help                    Show this message and exit.

Commands:
  analyze  Read the given files into global data and metadata objects.
  version  Get the library version.
```

#### Verbosity flag

The _verbosity_-flag can be provided in order to specify the verbosity
of the output to the CLI.
This flag is called `--verbose` or `-v` for short:

```shell script
$ pipenv run survey_analysis --verbose <COMMAND>
```
```shell script
$ pipenv run survey_analysis -v <COMMAND>
```

The verbosity of the output can be increased even more 
by duplicating the flag `--verbose` or `-v` up to two times:

```shell script
$ pipenv run survey_analysis --verbose --verbose --verbose <COMMAND>
```
```shell script
$ pipenv run survey_analysis -vvv <COMMAND>
```

#### Scripts flag

Beside verbosity there is a _scripts_-flag called `--scripts` or 
`-s` for short:

```shell script
$ pipenv run survey_analysis --scripts "scripts/" <COMMAND>
```
```shell script
$ pipenv run survey_analysis -s "scripts/" <COMMAND>
```

This will tell the program in which folder to look for the actual 
analysis scripts.
In case the _scripts_-flag is omitted it defaults to sub-folder `scripts/`.

#### Names flag

The _names_-flag called `--names` or `-n` for short:

```shell script
$ pipenv run survey_analysis --names "example_script_1" --names "example_script_2" <COMMAND>
```
```shell script
$ pipenv run survey_analysis -n "example_script_1" -n "example_script_2" <COMMAND>
```

This will tell the program which scripts in the scripts folder to execute.
In case the _names_-flag is omitted it defaults to all scripts in the
scripts folder.

#### Output format flag

The user is also able to let the application know in which output format the
diagrams should be generated during the analysis. 
For this purpose there is a flag called `--output-format` or `-f` for short.
Allowed values to this flag are the following:
* SCREEN
* PDF
* PNG
* SVG

On the CLI the actual call looks like this:

```shell script
$ pipenv run survey_analysis --output-format PNG <COMMAND>
```
```shell script
$ pipenv run survey_analysis -f PNG <COMMAND>
```

### Commands

There are two different commands implemented which come with different
flags and parameters:

1. Command _version_
2. Command _analyze_

#### Command _version_
 
The `version` command outputs the version number of 
this CLI-program like so:

```shell script
$ pipenv run survey_analysis version
0.0.1
```

#### Command _analyze_

The more interesting command is the `analyze` command
which comes with a _metadata_-flag `--metadata` or `-m` for short and 
a _data_-parameter.
In case the _metadata_-flag is omitted it assumes the following
path to the metadata file: 
`metadata/HIFIS_Software_Survey_2020_Questions.yml`.
The _data_-parameter can _not_ be omitted and need to be given explicitly
in order to be able to start the analysis.
This is an example of how to do the analysis:

```shell script
$ pipenv run survey_analysis analyze data/<data_file_name>.csv
```

## Contribute with Own Analysis Scripts

### Essential Criteria for Developing Own Analysis Scripts

As you might have read in the previous sections the actual analysis scripts 
reside in a specific folder called `scripts/`.
All scripts in that folder will be automatically discovered by the package 
`survey_analysis` when running the analysis.
In order that the program recognizes the scripts in that folder as
analysis scripts they need to fulfil the following two criteria:

1. The filename need to end on `.py`.
2. The file need to contain a function called `run` without any parameters.

```python
"""
A dummy script for testing the function dispatch

.. currentmodule:: survey_analysis.scripts.dummy
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

def run():
    print("Example Script")
```

If both criteria are satisfied the program will execute the `run`-functions
of the analysis scripts in an arbitrary sequence.

### File-System Structure of Core Component

```shell script
$ tree survey_analysis/
survey_analysis/
├── answer.py
├── cli.py
├── data.py
├── dispatch.py
├── globals.py
├── metadata.py
├── question.py
├── settings.py
└── version.py
```

### Files and Classes Explained

**ToDo**: This section need to be extended to all files and classes
found in package `survey_analysis`.

#### Classes to Represent Questions

File `question.py` contains the following classes:
- `AbstractQuestion`: Abstract class providing properties of a question 
like `id` and `text`.
- `Question`: Non-abstract class inheriting from abstract-base-class
`AbstractQuestion`. It represents a question with associated answers.
- `QuestionCollection`: Non-abstract class inheriting from abstract-base-class
`AbstractQuestion`. It represents a question with associated sub-questions.

#### Class to Represent Answers

File `answer.py` contains class `Answer`.
This class provides properties of an answer like `id` and `text`.

## Resources

Below are some handy resource links.

* [Project Documentation](TODO)
* [Click](https://click.palletsprojects.com/en/7.x) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

