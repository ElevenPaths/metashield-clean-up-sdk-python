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
import importlib

TEST_SETTINGS_MODULE = importlib.import_module(os.getenv('TEST_SETTINGS_MODULE', 'tests.settings_default'))

module_dict = TEST_SETTINGS_MODULE.__dict__
try:
    to_import = TEST_SETTINGS_MODULE.__all__
except AttributeError:
    to_import = [name for name in module_dict if not name.startswith('_')]
globals().update({name: module_dict[name] for name in to_import})


class Settings:
    def __init__(self, entries):
        self.__dict__.update({name: module_dict[name] for name in entries})


settings = Settings(to_import)
