##  Copyright (c) 2018-2023, Carnegie Mellon University
##  All rights reserved.
##
##  See LICENSE file for full information
##  SPDX-License-Identifier: BSD-2-Clause

##  SpiralPy/setup.py

from setuptools import setup, find_packages
import codecs
import os.path
import glob

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

def find_example_files():
    examples_dir = 'examples'
    example_files = glob.glob(os.path.join(examples_dir, '*.py'))
    example_files = example_files + glob.glob(os.path.join(examples_dir, 'test-many.sh'))
    example_files = example_files + glob.glob(os.path.join(examples_dir, '../README.md'))
    return [('share/spiralpy/examples', example_files)]

setup(
    name="spiralpy",
    version=get_version("spiralpy/__init__.py"),
    license="BSD-2-Clause",
    description="A Python front end to specify high-level numerical computations",
    long_description="Python front end for the SPIRAL project's Spiralpy system, which compiles high-level specifications of numerical computations into hardware-specific optimized code.  It supports a variety of CPU's as well as Nvidia and AMD GPU's on systems running Linux, Windows, or MacOS.",
    url="https://github.com/spiral-software/python-package-spiralpy",
    project_urls={
        "Source Code": "https://github.com/spiral-software/python-package-spiralpy",
    },
    author="SpiralGen Inc.",
    author_email="Patrick.Broderick@spiralgen.com",
    python_requires=">=3.7",
    packages=find_packages(),
    include_package_data=True,
    data_files=find_example_files(),
)
