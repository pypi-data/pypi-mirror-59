#!/usr/bin/env python
# -*- coding:utf-8 -*-

# NOTE(StaticCube) Guidelines for Major.Minor.Micro
# - Major means an API contract change
# - Minor means API bugfix or new functionality
# - Micro means change of any kind (unless significant enough for a minor/major).

import io
from setuptools import setup

setup(
  name = 'python-synology',
  packages = ['SynologyDSM'], # this must be the same as the name above
  version = '0.4.0',
  description = 'Python API for communication with Synology DSM',
  author = 'FG van Zeelst (StaticCube)',
  author_email = 'GitHub@StaticCube.com',
  url = 'https://github.com/StaticCube/python-synology/',
  download_url = 'https://github.com/StaticCube/python-synology/tarball/0.4.0',
  keywords = ['synology-dsm', 'synology'],
  classifiers = [],
  install_requires=['requests>=1.0.0']
)
