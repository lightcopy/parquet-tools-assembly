#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#
# Copyright 2016 sadikovi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
from setuptools import setup, Command

# assembly version
VERSION = "0.1.0"

# Currently Python 2.7 is supported
PYTHON_VERSION_MAJOR = 2
PYTHON_VERSION_MINOR = 7
if sys.version_info.major != PYTHON_VERSION_MAJOR or sys.version_info.minor != PYTHON_VERSION_MINOR:
    print "[ERROR] Only Python %s.%s is supported" % (PYTHON_VERSION_MAJOR, PYTHON_VERSION_MINOR)
    sys.exit(1)

# Run only on OS X and Linux
if not (sys.platform.startswith("darwin") or sys.platform.startswith("linux")):
    print "[ERROR] Only OS X and Linux are supported"
    sys.exit(1)

setup(
    name="parquet-tools-assembly",
    version=VERSION,
    description="Parquet-tools assembly",
    long_description="Prepare assembly and distribution for parquet-tools",
    author="Ivan Sadikov",
    author_email="ivan.sadikov@github.com",
    url="https://github.com/lightcopy/parquet-tools-assembly",
    platforms=["OS X", "Linux"],
    license="Apache License 2.0"
)
