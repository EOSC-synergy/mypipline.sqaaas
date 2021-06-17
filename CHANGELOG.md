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

## Unreleased

## [1.0.0](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/releases/v1.0.0) - 2021-06-18

[List of commits](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/compare/v0.3.0...v1.0.0)

### Added
- Added an external configuration file to set defaults for an analysis run
  ([!64](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/64)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Create files CONTRIBUTING, CHANGELOG, VERSION and adapt file README
  ([!66](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/66)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Refactor internal structure for OOP-style and add an example analysis script
  ([!67](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/67)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Add unit test cases for module `data_container`
  ([!85](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/85)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add unit test cases for module `question_collection`
  ([!80](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/80)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add unit test cases for module `answer_option`
  ([!83](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/83)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add unit test cases for module `question`
  ([!82](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/82)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Refactor models and adapt them to changed metadata structure and elements
  ([!72](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/72)
  by [erxleb87](https://gitlab.hzdr.de/erxleb87)).
- Add unit test cases for module `settings`
  ([!76](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/76)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Detect CSV files with gitleaks which is part of the tool SQA
  ([!74](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/74)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Add file `License.md` to provide license information of the project
  ([!90](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/90)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Create a getting started guide for the project
  ([!84](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/84)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Split up object routed to analysis scripts into data container and analysis objects
  ([!91](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/91)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Add capabilities to add a data preprocessing script to the project
  ([!92](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/92)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Add URLs of project to file `pyproject.toml` for PyPi.org
  ([!73](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/73)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Add URL of project documentation to file `pyproject.toml` for PyPi.org
  ([!94](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/94)
  by [Normo](https://gitlab.hzdr.de/Normo)).
  
### Changed
- Change Makefile and GitLab CI pipeline
  ([!68](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/68)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Improve inline documentation and API documentation
  ([!69](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/69)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Replace default branch names in GitLab CI pipeline with variable `CI_DEFAULT_BRANCH`
  ([!89](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/89)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Generate and publish project documentation on merges into default branch `main`
  ([!93](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/93)
  by [Normo](https://gitlab.hzdr.de/Normo)).
- Adapt file CHANGELOG to document changes made during the developments
  ([!95](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/95)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

### Fixed
- Enable GitLab CI job trigger to run on merges into default branch
  ([!70](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/70)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Fix infinite recursion in method `add_answer` in module `question`
  ([!81](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/81)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
- Add missing `__init__.py` files to unit test case packages
  ([!87](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/87)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

## [0.3.0](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/releases/v0.3.0) - 2021-04-22

[List of commits](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/compare/v0.1.0...v0.3.0)

### Added
- Add SQA tool for software quality assessments during GitLab CI pipeline
  ([!60](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/60)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Publish project on PyPi.org as `hifis-surveyval`
  ([!63](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/63)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).

### Changed
- Replace Pipenv by Poetry and add file `pyproject.toml` to project
  ([!59](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/59)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).
- Rename project to `HIFIS-Surveyval`
  ([!62](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/merge_requests/62)
  by [mdolling-gfz](https://gitlab.hzdr.de/mdolling-gfz)).

## [0.1.0](https://gitlab.hzdr.de/hifis/surveys/hifis-surveyval/-/releases/v0.1.0) - 2021-04-12

- Initial version of the project.
