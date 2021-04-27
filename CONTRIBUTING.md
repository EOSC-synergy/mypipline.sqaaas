<!--
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

Please add yourself to the list of contributors via a merge request if you made
significant contributions to this project.
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
