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

# Contributing

## Please Help to Improve this Project

Any contributions and help to improve this project via issues and merge requests
are most welcome and much appreciated.

## How to Contribute?

There a different ways to contribute to this project:

1. Discuss issues and merge requests
2. Create issues
3. Create merge requests
4. Do software testing

###  Discuss Issues and Merge Requests

You can contribute by participating in discussions you find in issues and 
merge requests.

### Create Issues

If you found a bug in the software or a typo in the documentation or
would like to clarify functional or quality aspects of the software you are
welcome to create issues to get in contact with us.

### Create Merge Requests

If you would like to provide a fix for a bug or a typo in the documentation or
even add or change specific features of the software or specific parts of the
documentation you are welcome to put the suggestion into a separate branch
and create a merge request.
Be aware of the need to test your contributions before opening a merge request.

### Do Software Testing

Sometimes automated test are not sufficient to account for specific corner 
cases and to reveal hidden bugs.
Testing the project manually is always a good approach to make sure that
the project also works for other people.
Even more valuable are of course automated tests.
Please feel free to support the project by providing automated test cases.

## How are Contributors Given Credit for Their Valuable Work?

Please add yourself to the list of contributors in file 
[README.md](README.md#contributors) 
via a merge request if you made significant contributions to this project.
Significant contributions are done by suggesting merge requests that fix
bugs or add features to the project.
Since all other contributions are welcome and may be significant as well 
you can request to be added as a contributor which is then decided on a 
case-by-case basis.

## Code Guidelines

### Code Style

Because this is a Python project you need to adhere to the 
[official Python style guides](https://www.python.org/dev/peps/pep-0008/).

### Linting the Project

Please make sure that changes made are linted with the following command 
before suggesting those changes in merge requests:

```shell
$ poetry run make lint
```

### REUSE Specification Compliance

Each file in this project needs a proper license and copyright header.
Please check that each file you add to the project contains license and 
copyright information and that it thereby meets the
[REUSE Specification](https://reuse.software/spec/).

### GitLab CI Pipeline

Make sure that all GitLab CI pipeline jobs pass on your branch before 
suggesting a merge request to merge your changes into the mainline.

### Software Testing 

During development of your changes please use the existing regression tests
to verify that your changes do not break existing test cases:

```shell
$ poetry run make test
```

Please consider using [pytest](https://docs.pytest.org/) to write 
unit test cases for your suggested changes.
Feel free to add those tests to the GitLab CI pipeline of this project.

## How to Create and Document a Release Tag

As soon as all tasks have been completed regarding the upcoming milestone a 
release tag may be created in GitLab which triggers the release process via CI
pipeline to publish the resulting package on [PyPi.org](https://pypi.org).
The following prerequisites need to be fulfilled:

1. **Change version in file `pyproject.toml`**:
The semantic versioning number in file `pyproject.toml` needs to be adapted
to match the version number of the tag to be created.

2. **Add section to file `CHANGELOG`**:
The file [CHANGELOG](CHANGELOG.md) needs an additional section that 
states the version to be tagged, a link to the release tag (which is available
as soon as the tag has been created), the date of tag creation, a link to a list
of commits done since the last tag, and a lists of all changes and their authors
that were merged into the default branch via Merge Requests since the last
release tag.
This example illustrates how such an entry should look like:
```
## [1.0.0](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/releases/v1.0.0) - 2021-06-18

[List of commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v0.3.0...v1.0.0)

### Changed
- Increase version in file `pyproject.toml` to version `1.0.0`
  ([!96](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/merge_requests/96)
  by [hueser93](https://gitlab.hzdr.de/hueser93)).
```

3. **Create a protected tag:**
The name of a release tag need to start with a `v` followed by a [semantic
version number](https://semver.org) like `v1.0.0`. 
Be aware that only tags that start with a `v` are protected tags and will be
used as a base for the packages to be published.

4. **Provide release notes:**
The tag needs to have a title, a message and release notes. 
These release notes provide a link to the respective entry in file
[CHANGELOG](CHANGELOG.md) and a link to a list of commits done between the last
release and the release to be created next, for example:
```
Release version 1.0.0. Read the changelog for further information.
- [Changelog](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/blob/main/CHANGELOG.md#100-2021-06-18)
- [Commits](https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval/-/compare/v0.3.0...v1.0.0)
```
