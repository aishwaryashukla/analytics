"""
<add description here>

(c)  2018 BlackRock.  All rights reserved.
"""

import datetime
import os
import subprocess
import sys
from importlib import import_module
from setuptools import setup


PKG_NAME = 'python_flask_example'
BUILD_META = 'build-meta'
VERSION_PY_FILE = os.path.join(PKG_NAME, 'version.py')
DEFAULT_PKG_VERSION = '0.0.1.dev1'
PKG_VERSION = DEFAULT_PKG_VERSION
PKG_VERSION_FILE = 'pkg_version.txt'

# Clear this flag to ignore the version specified in PKG_VERSION_FILE
# and use the DEFAULT_PKG_VERSION that's hard-coded in this script.
USE_PKG_VERSION_FILE = True


def set_pkg_version_from_file():
    """Obtain package version from a flat file created by the build system.

    Value may either be hard-coded in this file or provided at build time.
    """
    global PKG_VERSION

    try:
        version = open(PKG_VERSION_FILE).readline().rstrip('\n')
        if version:
            PKG_VERSION = version
    except Exception as e:
        print('Could not read {}: {}\nUsing default package version.'.
              format(PKG_VERSION_FILE, e.__class__.__name__, e),
              file=sys.stderr, flush=True
              )


def get_git_revision():
    """Determine git revision for this build

    :return: git revision (SHA-1 for commit)
    """
    git_revision = 'Unknown'
    if os.path.exists('.git'):
        build_host_git = ''
        try:
            # Git is not in a standard location in our Build
            # environment, so we have to try finding it via token.
            util = import_module('blkcore.util')
            build_host_git = util.get_token('SRPT.GIT_BIN')
            # get_token will return None rather than raise error on failure.
            if build_host_git is None:
                build_host_git = ''
        except ImportError:
            pass
        if os.access(build_host_git, os.X_OK):
            git = build_host_git
        else:
            git = 'git'
        cmd = [git, 'rev-parse', 'HEAD']
        try:
            git_revision = subprocess.check_output(cmd, universal_newlines=True).rstrip('\n')
        except Exception as e:
            # A number of things can go wrong trying to obtain the
            # git revision, so we need to be lenient.
            print('Could not determine git revision: {} - {!s}'.
                  format(e.__class__.__name__, e), file=sys.stderr, flush=True
                  )

    return git_revision


def write_version_py():
    """Write build version so it can be accessed at runtime.
    """
    content = """\"\"\"
THIS FILE IS GENERATED AT BUILD TIME

(c)  {} BlackRock.  All rights reserved.
\"\"\"

version = '{}'
git_revision = '{}'
"""

    now = datetime.datetime.now()
    with open(VERSION_PY_FILE, 'w') as f:
        f.write(content.format(now.year, PKG_VERSION, get_git_revision()))


if USE_PKG_VERSION_FILE:
    set_pkg_version_from_file()
write_version_py()

pkgs = [PKG_NAME]
pkg_data = {}

# IMPORTANT: Do not remove BUILD_META from the list of packages
#            for package projects. This information is required
#            by SRPT if you want to create a release element and
#            release your package.
#
if os.path.exists(BUILD_META):
    pkgs.append(BUILD_META)
    pkg_data[BUILD_META] = ['*']

setup(name=PKG_NAME,
      version=PKG_VERSION,
      packages=pkgs,
      package_data=pkg_data,
      description='<add short description here>',
      install_requires=open('requirements.txt').read().splitlines(),
      long_description="""
      <add long description here>
      """,
      classifiers=['Intended Audience :: BlackRock Internal Use Only',
                   'License :: Other/Proprietary License',
                   ],
      license="""
      This software is the intellectual property of BlackRock.
      """,
      maintainer='morrpat',
      maintainer_email='morrpat@blackrock.com',
      url='https://webster.bfm.com/publish/seg/pythondocs/python_flask_example/index.html')
