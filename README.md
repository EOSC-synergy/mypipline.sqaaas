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

This install some packages that are required for performing quality checks.
Usually they are also performed via GitLab CI, but can also be executed locally.

It is common practice to run some checks locally before pushing them online.
Therefore, execute below commands:
```console
$ make lint
```

## Resources

Below are some handy resource links.

* [Project Documentation](TODO)
* [Click](https://click.palletsprojects.com/en/7.x) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

