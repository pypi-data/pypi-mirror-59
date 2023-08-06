""" This module generates manifest files based on Octopus Deploy releases"""

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

import argparse
import json
import sys

from octopose import config, octo


def required_to_deploy_this_project(project, specific_projects):
    return len(specific_projects) == 0 or project in specific_projects


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--versions', default={}, type=json.loads,
                        help="Supply specific versions of projects to be written to the manifest. "
                             "Supplied as a string dictionary. (Will need to escape quotes)")
    parser.add_argument('-e', '--environment', default="local", type=str,
                        help="Create a manifest based on the packages currently deployed to an environment.")
    parser.add_argument('-p', '--projects', nargs='+', default=[], type=str,
                        help="Supply specific projects, to only deploy those projects. "
                             "Supplied with spaces between project names.")
    parser.add_argument('-i', '--ignore', nargs='+', default=[], type=str,
                        help="Supply project names to be ignored from the config.yaml file. Manifest generation will ignore these projects."
                             "Supplied with spaces between project names.")

    args = parser.parse_args(sys.argv[2:])
    specific_versions = args.versions
    env = args.environment
    specific_projects = args.projects
    ignored_projects = args.ignore
    projects = list(config.PROJECTS)

    environments = octo.get_environments()
    if env not in environments:
        print("Please supply a valid environment and try again")
        exit(1)

    missing_projects = []

    if ignored_projects:
        for p in projects[:]:
            if p in sorted(set(ignored_projects)):
                projects.remove(p)

    manifest = {'StagingLocation': config.STAGING, 'Projects': {}}
    for project in projects:
        project_id = octo.get_project_id(project)
        project_detail = {}
        if required_to_deploy_this_project(project, specific_projects):
            if project in specific_versions:
                if specific_versions[project] is None:
                    manifest['Projects'][project] = project_detail = None
                    continue
                release = octo.get_release_for_version(
                    project_id, specific_versions[project])
                project_detail['Version'] = specific_versions[project]
                project_detail['Packages'] = octo.get_specific_package_ids(
                    release)
            elif env != "local":
                release = octo.get_release_for_env(
                    project_id, environments[env])
                if release is not None:
                    project_detail['Version'] = release['Version']
                    packages = octo.get_specific_package_ids(
                        release, environments[env])
                    project_detail['Packages'] = packages
                else:
                    project_detail['Packages'] = octo.get_latest_packages(
                        project_id)
                    missing_projects.append(project)
            else:
                project_detail['Packages'] = octo.get_latest_packages(
                    project_id)

            manifest['Projects'][project] = project_detail

    if missing_projects:
        print(
            'Some projects do not exist on {1}. The manifest contains the latest available package versions for these projects: {0}'.format(
                missing_projects, env), '\n\n', json.dumps(manifest, indent=1))
    else:
        print(json.dumps(manifest, indent=1))
