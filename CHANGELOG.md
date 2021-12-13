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

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Group your changes into these categories:

`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

## [1.5.1](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.5.1) - 2021-12-13

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.5.0...v1.5.1)

### Fixed

- Fix style folder not properly being specified relatively
  ([!159](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/159)
  by [frust45](https://gitlab.hzdr.de/frust45)).

## [1.5.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.5.0) - 2021-12-09

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.4.0...v1.5.0)

### Added

- Allow to configure the default plot style via configuration
  ([!157](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/157)
  by [frust45](https://gitlab.hzdr.de/frust45)).

### Fixed

- Fix custom plot style template generation on init
  ([!156](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/156)
  by [frust45](https://gitlab.hzdr.de/frust45)).

## [1.4.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.4.0) - 2021-12-03

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.3.0...v1.4.0)

### Added

- Add implementation to specify parameters of a color map and fill pattern map
  and use color-blind friendly colors by default
  ([!152](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/152)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add functionality to define custom plot styles for Matplotlib plots
  ([!151](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/151)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Allow mandatory flag in QuestionCollections for multiple-choice QuestionCollections
  ([!148](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/148)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).

## [1.3.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.3.0) - 2021-10-26

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.2.0...v1.3.0)

### Fixed
- Fix full IDs of AnswerOptions to be a concatenation of QuestionCollection ID, Question ID and AnswerOption ID
  ([!146](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/146)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).

### Changed
- Use Python's type hinting in example script 01 about accessing data and metadata
  ([!144](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/144)
  by [hueser93](https://gitlab.hzdr.de/hueser93))

### Added
- Allow AnswerOptions to also have value representations aside from labels
  ([!147](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/147)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).

## [1.2.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.2.0) - 2021-10-07

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.2.0-preview...v1.2.0)

### Fixed
- Reorder steps to now manipulate IDs from CSV data header in the correct order
  ([!139](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/139)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).

### Changed
- Use accessors for properties like text and label in example script 1 - accessing data
  ([!140](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/140)
  by [hueser93](https://gitlab.hzdr.de/hueser93))
- Add Unix swap files to file .gitignore
  ([!136](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/136)
  by [tfoerst1](https://gitlab.hzdr.de/tfoerst1)).
- Adapt file README.md to cover new configuration variables in configuration file
  ([!141](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/141)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

### Added
- Raise exception if _group-by_-argument passed to grouping function contains NaN values
  ([!143](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/143)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Make aspect ratio of plots customizable and add auto-sizing to plotting methods
  ([!142](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/142)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add mixins to offer accessors for model properties and make HIERARCHY_SEPARATOR configurable
  ([!131](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/131)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).

## [1.2.0-preview](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.2.0-preview) - 2021-10-01

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.1.1...v1.2.0-preview)

### Fixed
- Various minor quality fixes: adapt file .gitignore and fix typos
  ([!125](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/125)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Project and repository URL changed and need to be adapted in the documentation
  ([!126](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/126)
  by [hueser93](https://gitlab.hzdr.de/hueser93))
- Automate rewriting of the CSV data file header if Question Collection full IDs are missing the Question ID part
  ([!124](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/124)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Fixing that invalid answers are removed multiple times which results in key errors
  ([!129](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/129)
  by [hueser93](https://gitlab.hzdr.de/hueser93))
- Fixing that answer values are all transformed to True if casted to bool when read in from data
  ([!127](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/127)
  by [hueser93](https://gitlab.hzdr.de/hueser93))
- Fixing example analysis script about accessing data and use ANONYMOUS_QUESTION_ID where necessary
  ([!135](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/135)
  by [hueser93](https://gitlab.hzdr.de/hueser93))
- Replace _ (underscore) with / (slash) as HIERARCHY_SEPARATOR given in data header when reading in data
  ([!134](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/134)
  by [hueser93](https://gitlab.hzdr.de/hueser93))

### Added
- Develop example analysis script with step-by-step explanations to access metadata and data
  ([!128](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/128)
  by [hueser93](https://gitlab.hzdr.de/hueser93))
- Split metadata YAML file up into one file per question collection
  ([!122](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/122)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).

## [1.1.1](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.1.1) - 2021-08-10

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.1.0...v1.1.1)

### Fixed
- Adapt schema that validates IETF language tags in metadata file
  ([!112](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/112)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Improve error handling in a couple of locations
  ([!114](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/114)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Add encoding when processing files
  ([!111](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/111)
  by [KatDwo](https://gitlab.hzdr.de/KatDwo)).
- Fix issue with method that concatenates data-frames
  ([!116](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/116)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Move preprocessing example script into separate file
  ([!117](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/117)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Adapt file README to describe how to quick-start the project and the content of the configuration file
  ([!118](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/118)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Make sure that input data is rejected if it is not CSV
  ([!115](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/115)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Method constructing a series from a given question ID should set the name of the index column
  ([!103](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/103)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Refactor unit test cases to remove duplications and redundancies
  ([!120](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/120)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Implement a helper class to create series or data-frame objects in unit test cases
  ([!121](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/121)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Write unit test cases for module question that test the conversion of a question into a series
  ([!105](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/105)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Write unit test cases for module question_collection that test the conversion of a question_collection into a data-frame
  ([!119](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/119)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Write unit test cases for module data_container that test conversion of IDs of question_collections into a data-frame
  ([!104](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/104)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

## [1.1.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.1.0) - 2021-07-13

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.0.1...v1.1.0)

### Added
- Additional features for preprocessing to mark and filter out specific answers
  ([!106](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/106)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Enable DataContainer to compose a DataFrame from given IDs
  ([!100](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/100)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Add license files for issue templates
  ([!109](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/109)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Write a section in CONTRIBUTING file about how to create and document a tag
  ([!102](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/102)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
  
### Changed
- Exclude release links from link checking
  ([!101](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/101)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Change development status classifier to production/stable 
  ([!97](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/97)
  by [Normo](https://gitlab.hzdr.de/Normo)).
  
## [1.0.1](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.0.1) - 2021-06-21

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v1.0.0...v1.0.1)

### Added
- Missing documentation for preprocess option of the init command
  ([!99](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/99)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).

### Fixed
- Fixed bug where metadata could not be loaded due to missed parenthesis
  ([!98](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/98)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
  
## [1.0.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.0.0) - 2021-06-18

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v0.3.0...v1.0.0)

### Added
- Added an external configuration file to set defaults for an analysis run
  ([!64](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/64)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Create files CONTRIBUTING, CHANGELOG, VERSION and adapt file README
  ([!66](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/66)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Refactor internal structure for OOP-style and add an example analysis script
  ([!67](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/67)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Add unit test cases for module `data_container`
  ([!85](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/85)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add unit test cases for module `question_collection`
  ([!80](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/80)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add unit test cases for module `answer_option`
  ([!83](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/83)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add unit test cases for module `question`
  ([!82](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/82)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Refactor models and adapt them to changed metadata structure and elements
  ([!72](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/72)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Add unit test cases for module `settings`
  ([!76](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/76)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Detect CSV files with gitleaks which is part of the tool SQA
  ([!74](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/74)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Add file `License.md` to provide license information of the project
  ([!90](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/90)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Create a getting started guide for the project
  ([!84](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/84)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Split up object routed to analysis scripts into data container and analysis objects
  ([!91](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/91)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Add capabilities to add a data preprocessing script to the project
  ([!92](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/92)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Add URLs of project to file `pyproject.toml` for PyPi.org
  ([!73](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/73)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Add URL of project documentation to file `pyproject.toml` for PyPi.org
  ([!94](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/94)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Re-enable access to data as pandas DataFrames
  ([!88](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/88)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
  
### Changed
- Change Makefile and GitLab CI pipeline
  ([!68](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/68)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Improve inline documentation and API documentation
  ([!69](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/69)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Replace default branch names in GitLab CI pipeline with variable `CI_DEFAULT_BRANCH`
  ([!89](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/89)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Generate and publish project documentation on merges into default branch `main`
  ([!93](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/93)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Adapt file CHANGELOG to document changes made during the developments
  ([!95](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/95)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Increase version in file `pyproject.toml` to version `1.0.0`
  ([!96](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/96)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

### Fixed
- Enable GitLab CI job trigger to run on merges into default branch
  ([!70](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/70)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Fix infinite recursion in method `add_answer` in module `question`
  ([!81](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/81)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add missing `__init__.py` files to unit test case packages
  ([!87](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/87)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

## [0.3.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v0.3.0) - 2021-04-22

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v0.1.0...v0.3.0)

### Added
- Add SQA tool for software quality assessments during GitLab CI pipeline
  ([!60](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/60)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Publish project on PyPi.org as `hifis-surveyval`
  ([!63](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/63)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

### Changed
- Replace Pipenv by Poetry and add file `pyproject.toml` to project
  ([!59](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/59)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Rename project to `HIFIS-Surveyval`
  ([!62](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/62)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).

## [0.1.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v0.1.0) - 2021-04-12

- Initial version of the project.
