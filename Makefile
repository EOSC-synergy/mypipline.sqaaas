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

.DEFAULT_GOAL := build
.PHONY: build publish package coverage test lint docs
PROJ_SLUG = hifis_surveyval
CLI_NAME = hifis-surveyval
LINTER = flakehell lint
SHELL = bash

build:
	poetry build

lint:
	poetry run $(LINTER) $(PROJ_SLUG) tests/

test:
	poetry run py.test --cov-report term --cov=$(PROJ_SLUG) tests/

coverage: lint
	poetry run py.test --cov-report html --cov=$(PROJ_SLUG) tests/

docs: coverage
	cd docs && poetry run make html

package: clean docs
	poetry build

clean :
	rm -rf dist \
	rm -rf docs/build \
	rm -rf *.egg-info
	poetry run coverage erase

reformat:
	poetry run isort .
	poetry run black --line-length 79 .
