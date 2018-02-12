#! /usr/bin/env python
#
# Copyright (C) 2017 Chris Holdgraf
# <choldgraf@berkeley.edu>
#
# Adapted from MNE-Python

import os
import setuptools
from numpy.distutils.core import setup

version = "0.1"

descr = """Tools to preprocess, clean, and otherwise manipulate Jupyter Notebooks."""

DISTNAME = 'nbclean'
DESCRIPTION = descr
MAINTAINER = 'Chris Holdgraf'
MAINTAINER_EMAIL = 'choldgraf@gmail.com'
URL = 'https://github.com/choldgraf/nbclean'
LICENSE = 'BSD (3-clause)'
DOWNLOAD_URL = 'https://github.com/choldgraf/nbclean'
VERSION = version


if __name__ == "__main__":
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          include_package_data=False,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          download_url=DOWNLOAD_URL,
          long_description=open('README.md').read(),
          zip_safe=False,  # the package can run out of an .egg file
          classifiers=['Intended Audience :: Science/Research',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved',
                       'Programming Language :: Python',
                       'Topic :: Software Development',
                       'Topic :: Scientific/Engineering',
                       'Operating System :: OSX'],
          platforms='any',
          packages=['nbclean'],
          install_requires=["nbformat", "nbgrader", "numpy", "tqdm"],
          package_data={},
          scripts=[])
