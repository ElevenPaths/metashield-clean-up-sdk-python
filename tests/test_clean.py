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

    def test_clean_file_and_get_result(self):
        """
        Test cleaning a file only specifying the file and it stream.
        """
        response = self.api.clean_file(self.stream, self.filename)
        clean_id = response.data["cleanId"]

        time.sleep(4)  # wait while file is being cleaned
        response = self.api.get_clean_result(clean_id)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.error)

    def test_clean_file_with_valid_profile_and_get_result(self):
        """
        Test cleaning a file specifying a valid profile id.
        """
        response = self.api.clean_file(self.stream, self.filename, profile_id=settings.DATASET["valid_profile"])
        clean_id = response.data["cleanId"]

        time.sleep(4)  # wait while file is being cleaned
        response = self.api.get_clean_result(clean_id)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.error)

    def test_clean_file_with_pdf_disabled_profile_and_get_result(self):
        """
        Test cleaning a PDF file specifying a profile id with PDF format disabled.
        """
        response = self.api.clean_file(self.stream, self.filename, profile_id=settings.DATASET["pdf_disabled_profile"])
        clean_id = response.data["cleanId"]

        time.sleep(4)  # wait while file is being cleaned
        response = self.api.get_clean_result(clean_id)
        self.assertEqual({}, response.data)
        self.assertEqual(205, response.error.code)
        self.assertEqual(u'The extension is not selected in the profile', response.error.message)

    def test_clean_file_with_disabled_profile_and_get_result(self):
        """
        Test cleaning a file specifying a disabled, but existent, profile id.
        """
        response = self.api.clean_file(self.stream, self.filename, profile_id=settings.DATASET["disabled_profile"])
        self.assertIsNone(response.data)
        self.assertEqual(210, response.error.code)
        self.assertEqual(u'Profile doesn\'t exist', response.error.message)

    def test_clean_file_with_non_existent_profile_and_get_result(self):
        """
        Test cleaning a file specifying a non existent profile id.
        """
        response = self.api.clean_file(self.stream, self.filename, profile_id="non-existent-profile")
        self.assertIsNone(response.data)
        self.assertEqual(210, response.error.code)
        self.assertEqual(u'Profile doesn\'t exist', response.error.message)

    def test_clean_and_analyze_file_and_get_result(self):
        """
        Test analyzing and cleaning a file using default analysis format.
        """
        response = self.api.clean_file(self.stream, self.filename, analyze=True)
        clean_id = response.data["cleanId"]
        analyze_id = response.data["analyzeId"]

        time.sleep(4)  # wait while file is being cleaned and analyzed
        response = self.api.get_clean_result(clean_id)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.error)
        response = self.api.get_analyze_result(analyze_id)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.error)

    def test_try_to_get_clean_result_with_error(self):
        """
        Test requesting a non existent clean result.
        """
        response = self.api.get_clean_result("result-id")
        self.assertEqual({}, response.data)
        self.assertEqual(207, response.error.code)
        self.assertEqual("The result doesn't exist", response.error.message)
