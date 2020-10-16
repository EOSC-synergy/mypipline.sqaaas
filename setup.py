#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to create the package we'll publish to PyPI.

.. currentmodule:: setup.py
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import importlib.util
import os
from codecs import open  # Use a consistent encoding.
from os import path
from pathlib import Path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get the base version from the library.  (We'll find it in the `version.py`
# file in the src directory, but we'll bypass actually loading up the library.)
vspec = importlib.util.spec_from_file_location(
  "version",
  str(Path(__file__).resolve().parent /
      'survey_analysis'/"version.py")
)
vmod = importlib.util.module_from_spec(vspec)
vspec.loader.exec_module(vmod)
version = getattr(vmod, '__version__')

# If the environment has a build number set...
if os.getenv('buildnum') is not None:
    # ...append it to the version.
    version = "{version}.{buildnum}".format(
        version=version,
        buildnum=os.getenv('buildnum')
    )

setup(
    name='SurveyAnalysis2020',
    description="This project is used to develop analysis scripts for the HIFIS Software survey.",
    long_description=long_description,
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    install_requires=[
        # Include dependencies here
        'click>=7.0,<8',
        'matplotlib>=3.2.0',
        'numpy>=1.18.1',
        'pandas>=1.0.1',
        'pyyaml>=5.3.1',
        'spacy>=2.2.4',
        'wordcloud==1.7.0',
        'plotnine==0.7.1',
        'requests==2.24.0',
        'tabulate==0.8.7'
    ],
    extras_require={
        'dev': [
            'flake8>=3.7.9,<4',
            'flake8-docstrings>=1.5.0,<2',
            'isort>=4.3.21,<5',
            'pytest>=3.4.0,<4',
            'pytest-cov>=2.5.1,<3',
            'pytest-pythonpath>=0.7.2,<1',
            'setuptools>=38.4.0',
            'Sphinx>=2.2.0',
            'sphinx-rtd-theme>=0.4.3,<1',
            'tox>=3.0.0,<4',
            'twine>=1.11.0,<2',
        ]
    },
    entry_points="""
    [console_scripts]
    survey_analysis=survey_analysis.cli:cli
    """,
    python_requires=">=0.0.1",
    license='GPLv3',
    author='HIFIS Software',
    author_email='software@hifis.net',
    url= 'https://gitlab.hzdr.de/hifis/survey-analysis-2020',
    download_url=(
        f'https://gitlab.hzdr.de/hifis/survey-analysis-2020/'
        f'-/archive/{version}/survey-analysis-2020-{version}.tar.gz'
    ),
    keywords=[
        # Add package keywords here.
    ],
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering',
      '''License :: OSI Approved :: GPLv3 License''',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True
)
