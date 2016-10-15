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

import os
import shutil
import sys
from setuptools import setup, Command
from subprocess import Popen, PIPE

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

PARQUET_MR_GIT = "https://github.com/apache/parquet-mr"
PARQUET_TOOLS = "parquet-tools"
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
STAGING_DIR = os.path.realpath(os.path.join(ROOT_DIR, "staging"))
LIB_DIR = os.path.realpath(os.path.join(ROOT_DIR, "lib"))
# Get distribution name based on processed tag and client mode

def get_distribution_name():
    for path in os.listdir(LIB_DIR):
        if path.endswith(".tag") and not path.startswith(".tag"):
            return os.path.splitext(path)[0]
    return "parquet-tools-assembly"

DISTR_NAME = get_distribution_name()

class Assembly(Command):
    description = "Prepare assembly for parquet-tools"
    user_options = [
        ("tag=", "t", "Tag for apache/parquet-mr repository"),
        ("client=", "c", "Include Hadoop dependencies, otherwise assumed that provided at runtime")
    ]

    def initialize_options(self):
        self.tag = None
        self.client = False

    def finalize_options(self):
        if not self.tag:
            print "[ERROR] Tag is required, see %s/tags for available tags" % PARQUET_MR_GIT
            sys.exit(1)
        else:
            print "[INFO] Using tag %s" % self.tag

        if self.client:
            print "[INFO] Include Hadoop dependencies"
        else:
            print "[INFO] Exclude Hadoop dependencies"

    def _tag_name(self, tag, client):
        hadoop = ""
        if client:
            hadoop = "-dh"
        return "parquet-tools-dist-%s%s.tag" % (tag, hadoop)

    def _touch(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    def run(self):
        try:
            repo = Repo()
            # clean up lib directory, remove al jar files in it
            print "[INFO] Clean up %s" % LIB_DIR
            for path in os.listdir(LIB_DIR):
                if path.endswith(".jar") or path.endswith(".tag"):
                    fpath = os.path.join(LIB_DIR, path)
                    os.remove(fpath)
            # clone repository, and get path for repository
            path = repo.clone(PARQUET_MR_GIT, self.tag, STAGING_DIR)
            # build parquet-tools subproject with options depending on client mode
            args = ["-DskipTests"]
            if self.client:
                args.append("-Plocal")
            parquetToolsDir = os.path.join(path, PARQUET_TOOLS)
            repo.package(parquetToolsDir, args)
            # copy artefacts from target into lib
            targetDir = os.path.join(parquetToolsDir, "target")
            for jar in os.listdir(targetDir):
                if jar.startswith(PARQUET_TOOLS) and jar.endswith(".jar"):
                    shutil.copy(os.path.join(targetDir, jar), LIB_DIR)
            # create distribution name file
            name = os.path.join(LIB_DIR, self._tag_name(self.tag, self.client))
            self._touch(name)
        except Exception as err:
            print "[ERROR] %s" % err
            sys.exit(1)

# Common functionality to work with repository
class Repo(object):
    def __init__(self):
        self.git = self._which_cmd("git")
        self.mvn = self._which_cmd("mvn")

    def _which_cmd(self, cmd):
        fqn = None
        with Popen(["which", cmd], stdout=PIPE).stdout as stream:
            fqn = stream.read().strip()
        if not fqn:
            raise StandardError("Could not find %s" % cmd)
        return fqn

    def clone(self, repo, tag, directory):
        if not os.path.isdir(directory):
            raise StandardError("%s is not a valid directory" % directory)
        # create sub-directory for provided tag
        path = os.path.join(directory, tag)
        if os.path.isdir(path):
            print "[INFO] Tag is already copied"
            return path
        print "[INFO] Create directory for tag %s" % path
        code = Popen([self.git, "clone", "-b", tag, "--depth", "1", repo, path]).wait()
        if code is not 0:
            msg = "Failed to clone repository %s into %s, code=%s" % (repo, path, code)
            raise StandardError(msg)
        print "[INFO] Cloned repository into %s" % path
        return path

    def package(self, directory, options):
        args = [self.mvn, "-f", directory, "clean", "package"]
        args += options
        code = Popen(args).wait()
        if code is not 0:
            raise StandardError("Failed to package project in %s, code=%s" % (directory, code))
        print "[INFO] Successfully packaged project in %s" % directory

setup(
    name=DISTR_NAME,
    version=VERSION,
    description="Parquet-tools assembly",
    long_description="Prepare assembly and distribution for parquet-tools",
    author="Ivan Sadikov",
    author_email="ivan.sadikov@github.com",
    url="https://github.com/lightcopy/parquet-tools-assembly",
    platforms=["OS X", "Linux"],
    license="Apache License 2.0",
    cmdclass={
        "assembly": Assembly
    }
)
