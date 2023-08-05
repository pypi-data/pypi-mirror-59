#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import os
import io
import re

try:
  from setuptools import setup
  from setuptools.command.install import install
  setup
except ImportError:
  from distutils.core import setup
  setup

# Get the long description from the README
def readme():
  with open('README.md') as f:
    return f.read()

# Read, version funcs taken from:
# https://github.com/ellisonbg/altair/blob/master/setup.py
def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()

def version(path):
    """
    Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = version('approxposterior/__init__.py')

# Setup!
setup(name = 'approxposterior',
      version = VERSION,
      description = 'Gaussian Process Approximation to Posterior Distributions',
      long_description = readme(),
      long_description_content_type = 'text/markdown',
      classifiers = [
                      'Development Status :: 5 - Production/Stable',
                      'License :: OSI Approved :: MIT License',
                      'Programming Language :: Python :: 3.5',
                      'Programming Language :: Python :: 3.6',
                      'Programming Language :: Python :: 3.7',
                      'Topic :: Scientific/Engineering :: Astronomy',
                    ],
      url = 'https://github.com/dflemin3/approxposterior',
      author = 'David P. Fleming',
      author_email = 'dflemin3@uw.edu',
      license = 'MIT',
      packages = ['approxposterior'],
      install_requires = ['numpy',
                          'matplotlib >= 2.0.0',
                          'scipy',
                          'george',
                          'emcee >= 3.0',
                          'corner',
                          'sklearn',
                          'pybind11',
                          'pytest',
                          'h5py'],
      include_package_data = True,
      zip_safe = False)
