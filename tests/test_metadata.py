#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provides unit tests for class Metadata.

Unit tests for class Metadata.

.. currentmodule:: tests.test_metadata
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""


# from survey_analysis.metadata import Metadata
import pytest


@pytest.mark.skip("UUT has changed, test needs to be updated.")
class TestMetadata(object):
    """
    Tests metadata operations.

    Basic tests for class Metadata are performed in unit test methods of
    this class.
    """

    def setup_method(self):
        """
        Set up test fixture.

        Test fixture initializes the metadata object before each test case
        method is executed.
        """
        self.metadata = Metadata()

    def teardown_method(self):
        """
        Tear down test fixture.

        Test fixture is unset by removing the metadata object after each
        test case method has been executed.
        """
        self.metadata = None

    def test_get_metadata_dict_by_id_key(self):
        """
        Test whether dictionary with metadata of a question is returned.

        A YAML file with test data is given and loaded, so that the resulting
        data in the metadata dictionary can be compared with expected data.
        """
        filename_yaml: str = 'tests/fixtures/metadata_one_entry.yml'
        self.metadata.set_metadata_yaml_filename(filename_yaml)
        self.metadata.load_metadata_from_yaml_file()
        expected_metadata: typ.Dict[str] = {
            'question': 'My question is ... ?',
            'sub-items': {
                'SQ001': {
                    'text': 'This is the topic of the sub-item ...',
                    'answers': {
                        'A1': 'Answer1',
                        'A2': 'Answer2'
                    },
                    'type': 'Single-Choice'
                }
            },
            'type': 'Multiple-Choice'
        }
        id_key: str = 'G1234'
        actual_metadata: typ.Dict[str] = \
            self.metadata.get_metadata_dict_by_id_key(id_key)
        assert (actual_metadata['sub-items']['SQ001']['answers']['A1'] ==
                expected_metadata['sub-items']['SQ001']['answers']['A1']), \
            'Metadata content is not valid.'
