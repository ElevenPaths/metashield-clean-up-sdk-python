# -*- coding: utf-8 -*-

# Copyright (C) Telefonica Digital | ElevenPaths
#
# This library is free software you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import time
import unittest

from sdklib.util.files import guess_filename_stream

from metashield_clean_up.api import MetashieldCleanUp
from conf import settings


class TestMetashieldAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename, cls.stream = guess_filename_stream("tests/resources/file.pdf")
        MetashieldCleanUp.set_default_host(settings.HOST)
        if settings.PROXY is not None:
            MetashieldCleanUp.set_default_proxy(settings.PROXY)
        cls.api = MetashieldCleanUp(settings.DATASET["app_id"], settings.DATASET["secret_key"])

    @classmethod
    def tearDownClass(cls):
        pass

    def test_analyze_file_default_format(self):
        """
        Test to analyze a file using the default format
        """
        response = self.api.analyze_file(self.stream, self.filename)
        analyze_id = response.data["analyzeId"]

        time.sleep(5)  # wait while file is being analyzed
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertNotEqual({}, response.data)
        self.assertIsNone(response.error)

    def test_analyze_file_format_list_metadata(self):
        """
        Test to analyze a  file using a List format
        """
        response = self.api.analyze_file(self.stream, self.filename, self.api.ANALYZE_FORMAT_LIST_METADATA)
        analyze_id = response.data["analyzeId"]

        time.sleep(5)  # wait while file is being analyzed
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertNotEqual({}, response.data)
        self.assertIsNone(response.error)

    def test_analyze_file_format_metadata_name_basic(self):
        """
        Test to analyze a file suing NameBasic format
        """
        response = self.api.analyze_file(self.stream, self.filename, self.api.ANALYZE_FORMAT_METADATA_NAME_BASIC)
        analyze_id = response.data["analyzeId"]

        time.sleep(5)  # wait while file is being analyzed
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertNotEqual({}, response.data)
        self.assertIsNone(response.error)

    def test_analyze_file_format_metadata_name_simplify(self):
        """
        Test to analyze a file using NameSimplify format
        """
        response = self.api.analyze_file(self.stream, self.filename, self.api.ANALYZE_FORMAT_METADATA_NAME_SIMPLIFY)
        analyze_id = response.data["analyzeId"]

        time.sleep(5)  # wait while file is being analyzed
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertNotEqual({}, response.data)
        self.assertIsNone(response.error)

    def test_analyze_file_format_filename_simplify(self):
        """
        Test to analyze a file using FilenameSimplify format
        """
        response = self.api.analyze_file(self.stream, self.filename, self.api.ANALYZE_FORMAT_FILENAME_SIMPLIFY)
        analyze_id = response.data["analyzeId"]

        time.sleep(5)  # wait while file is being analyzed
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertNotEqual({}, response.data)
        self.assertIsNone(response.error)

    def test_analyze_file_format_category_simplify(self):
        """
        Test to analyze a file using CategorySimplify format
        """
        response = self.api.analyze_file(self.stream, self.filename, self.api.ANALYZE_FORMAT_CATEGORY_SIMPLIFY)
        analyze_id = response.data["analyzeId"]

        time.sleep(5)  # wait while file is being analyzed
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertNotEqual({}, response.data)
        self.assertIsNone(response.error)

    def test_analyze_file_format_non_existent(self):
        """
        Test to analyze a file using CategorySimplify format
        """
        with self.assertRaises(ValueError) as error:
            self.api.analyze_file(self.stream, self.filename, u'invalid-format')

        self.assertTrue(u'analyze_format must be a valid metadata format' in error.exception)

    def test_try_to_get_analyze_result_non_existent(self):
        """
        Test requesting a non existent analysis result.
        """
        response = self.api.get_analyze_result("7118e1c4952b44a7b5ee9cdb46f73f09")
        self.assertEqual({}, response.data)
        self.assertEqual(207, response.error.code)
        self.assertEqual("The result doesn't exist", response.error.message)

    def test_try_to_get_analyze_result_invalid(self):
        """
        Test requesting a non existent analysis result with invalid analyzeId format.
        """
        response = self.api.get_analyze_result("result-id")
        self.assertEqual({}, response.data)
        self.assertEqual(207, response.error.code)
        self.assertEqual("The result doesn't exist", response.error.message)
