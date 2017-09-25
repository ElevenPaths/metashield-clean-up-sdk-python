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

import os


# Default settings
HOST = "https://metashieldclean-up.elevenpaths.com"
PROXY = os.getenv('PROXY', None)

# Dictionary containing settings for each environment
DATASET = {
    "app_id": "REPLACE_APP_ID_HERE",
    "secret_key": "REPLACE_SECRET_KEY_HERE",
    "valid_profile_id": "REPLACE_VALID_PROFILE_ID_HERE",
    "disabled_profile_id": "REPLACE_DISABLE_PROFILE_ID_HERE",
    "pdf_disabled_profile_id": "REPLACE_PDF_DISABLED_PROFILE_ID_HERE"
}
