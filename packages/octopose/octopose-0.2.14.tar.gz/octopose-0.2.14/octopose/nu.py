""" This module calls through to nuget to install NuGet packages"""

# MIT License
#
# Copyright (c) 2018 Huddle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

from octopose import config


class Nu:
    def __init__(self, subprocess_runner):
        """Nu interacts with nuget.exe by running commands in a subprocess"""
        self.subprocess_runner = subprocess_runner
        self.nuget_exe = "{0}\\third_party\\NuGet.exe".format(
            os.path.dirname(os.path.abspath(__file__)))

    def get_deployable(self, name, version, staging_location):
        """ Get deployables from pacakage sources for local deployment. """
        for source in config.PACKAGE_SOURCES:
            args = "{0} install {1} -Source {2} -OutputDirectory {3}".format(self.nuget_exe, name, source,
                                                                             staging_location)
            if version is not None:
                args = args + " -Version {0}".format(version)

            self.subprocess_runner.run(args, "Getting of {0} at version {1} failed".format(
                name, version), self.nuget_exe)
