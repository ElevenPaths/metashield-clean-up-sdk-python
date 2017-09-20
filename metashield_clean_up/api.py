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

"""
This library offers an API to use Metashield Clean-up Online in a python environment.
"""

from sdklib.http import HttpSdk
from sdklib.http.authorization import X11PathsAuthentication
from sdklib.http.renderers import MultiPartRenderer
from sdklib.http.response import Api11PathsResponse


class MetashieldCleanUp(HttpSdk):
    """
    Metashield Cleanup API class
    """
    DEFAULT_HOST = "https://metashieldclean-up.elevenpaths.com"

    response_class = Api11PathsResponse

    PROFILE_ID_11PATHS_HEADER_NAME = "X-11paths-Profile-Id"
    ANALYZE_11PATHS_HEADER_NAME = "X-11paths-Analyze"
    ANALYZE_FORMAT_11PATHS_HEADER_NAME = "X-11paths-Analyzeformat"

    API_CLEAN_FILE_URL = "/ExternalApi/CleanFile"
    API_ANALYZE_FILE_URL = "/ExternalApi/AnalyzeFile"
    API_CLEAN_RESULT_URL = "/ExternalApi/GetCleanResult"
    API_ANALYZE_RESULT_URL = "/ExternalApi/GetAnalyzeResult"

    ANALYZE_FORMAT_LIST_METADATA = "ListMetadata"
    ANALYZE_FORMAT_METADATA_NAME_BASIC = "MetadataNameBasic"
    ANALYZE_FORMAT_METADATA_NAME_SIMPLIFY = "MetadataNameSimplify"
    ANALYZE_FORMAT_FILENAME_SIMPLIFY = "FileNameSimplify"
    ANALYZE_FORMAT_CATEGORY_SIMPLIFY = "CategorySimplify"

    VALID_METADATA_FORMATS = (
        ANALYZE_FORMAT_LIST_METADATA,
        ANALYZE_FORMAT_METADATA_NAME_BASIC,
        ANALYZE_FORMAT_METADATA_NAME_SIMPLIFY,
        ANALYZE_FORMAT_FILENAME_SIMPLIFY,
        ANALYZE_FORMAT_CATEGORY_SIMPLIFY
    )

    def __init__(self, app_id, secret_key):
        """
        Initialize the Metashield SDK with provided user information.

        :param app_id: User appId to be used
        :param secret_key: User secretKey to be used
        """
        super(MetashieldCleanUp, self).__init__()
        self.app_id = app_id
        self.secret_key = secret_key
        self.authentication_instances += (X11PathsAuthentication(self.app_id, self.secret_key),)

    def clean_file(self, file_stream, filename, profile_id=None, analyze=False,
                   analyze_format=ANALYZE_FORMAT_LIST_METADATA):
        """
        Sends a file to Metashield Cleanup through its API to be cleaned and returns a response with the cleanId.

        :param file_stream: The stream/content of file
        :param filename: The file name
        :param profile_id: The profile id to be used. Default: None
        :param analyze: Sets if metadata should be analyzed
        :param analyze_format: Analysis format to be used on metadata analysis
        :return: Response of the request. If is correct, cleanId and analysisId attributes are inside data parameter.
        """
        headers = self.default_headers()
        if profile_id is not None:
            headers[self.PROFILE_ID_11PATHS_HEADER_NAME] = profile_id
        if analyze:
            headers[self.ANALYZE_11PATHS_HEADER_NAME] = "True"
            if analyze_format not in self.VALID_METADATA_FORMATS:
                raise ValueError("analyze_format must be a valid metadata format")
            else:
                headers[self.ANALYZE_FORMAT_11PATHS_HEADER_NAME] = analyze_format

        return self.post(self.API_CLEAN_FILE_URL, headers=headers, files={"file": (filename, file_stream)},
                         renderer=MultiPartRenderer())

    def get_clean_result(self, result_id):
        """
        Requests for cleaned file with specified cleanId through Metashield Cleanup API and returns the response with
        the file content in base64 format.

        :param result_id: The clean id obtained on request to clean
        :return: Response of the request. If is correct, the file content is inside the data parameter dict, with the
                    cleanId as key.
        """
        return self.get(self.API_CLEAN_RESULT_URL, query_params={"cleanId": result_id})

    def analyze_file(self, file_stream, filename, analyze_format=ANALYZE_FORMAT_LIST_METADATA):
        """
        Sends a file to Metashield Cleanup through its API to be analyzed and returns a response with the analyzeId.

        :param file_stream: The stream/content of file
        :param filename: The file name
        :param analyze_format: Analysis format to be used on metadata analysis
        :return: Response of the request. If is correct, analysisId attribute is inside data parameter.
        """
        headers = self.default_headers()
        if analyze_format is None or analyze_format not in self.VALID_METADATA_FORMATS:
            raise ValueError("analyze_format must be a valid metadata format")
        else:
            headers[self.ANALYZE_FORMAT_11PATHS_HEADER_NAME] = analyze_format

        return self.post(self.API_ANALYZE_FILE_URL, headers=headers, files={"file": (filename, file_stream)},
                         renderer=MultiPartRenderer())

    def get_analyze_result(self, result_id):
        """
        Request for analysis result with specified analyzeId through Metashield Cleanup API and returns the response
        with the data in JSON format.

        :param result_id: The analysis id obtained on request to analyze
        :return: Response of the request. If is correct, the analysis content is inside the data parameter dict, with
                    analyzeId as key.
        """
        return self.get(self.API_ANALYZE_RESULT_URL, query_params={"analyzeId": result_id})
