#!/usr/bin/env python

# survey-analysis-framework
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
.. currentmodule:: test_example
.. moduleauthor:: HIFIS Software <software@hifis.net>

This is a sample test module.
"""

import pytest

"""
This is just an example test suite.  It will check the current project version
numbers against the original version numbers and will start failing as soon as
the current version numbers change.
"""


def test_import_getVersions_originalVersions():
    """
    Arrange: Load the primary module.
    Act: Retrieve the versions.
    Assert: Versions match the version numbers at the time of project creation.
    """
    assert (
        # fmt: off
        # '0.0.1' == survey_analysis.__version__,
        # fmt: on
        "This test is expected to fail when the version increments. "
        "It is here only as an example and you can remove it."
    )

    """
    This is just an example test suite that demonstrates the very useful
    `parameterized` module.  It contains a test in which the squares of the
    first two parameters are added together and passes if that sum equals the
    third parameter.
    """


@pytest.mark.parametrize("a,b,c", [(1, 2, 5), (3, 4, 25)])
def test_ab_addSquares_equalsC(a, b, c):
    """
    Arrange: Acquire the first two parameters (a and b).
    Act: Add the squares of the first two parameters (a and b).
    Assert: The sum of the squares equals the third parameter (c).

    :param a: the first parameter
    :param b: the second parameter
    :param c: the result of adding the squares of a and b
    """
    assert (
        a * a + b * b == c,
        "'c' should be the sum of the squares of 'a' and 'b'. "
        "This is an example test and can be removed.",
    )
