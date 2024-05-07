# SpiralPy Package
#
# Copyright 2018-2023, Carnegie Mellon University
# All rights reserved.
#
# See LICENSE (https://github.com/spiral-software/python-package-spiralpy/blob/main/LICENSE)

"""Spiral Python Interface

This is the Python front end for the SPIRAL project's (http://www.spiralgen.com) Python to
Spiral (SpiralPy) interface, which compiles high-level specifications of numerical computations
into hardware-specific optimized code.  It supports a variety of CPU's as well as Nvidia and
AMD GPU's on systems running Linux, Windows, or MacOS.

SpiralPy originated under the DARPA PAPPA (Performant Automation of Parallel Program Assembly)
program, see: https://www.darpa.mil/program/performant-automation-of-parallel-program-assembly.
The program focused on ways reduce the complexity of building software that takes advantage of the
massive parallelism of advanced high-preformance computing systems.  Further work continued as
part of FFTX, see https://spiral-software.github.io/fftx/introduction.html, under the Exascale
Computing Project (https://www.exascaleproject.org/).

SpiralPy, implemented as a Python package, uses the SPIRAL code generation system to translate
NumPy-based specifications to generated code, then compiles that code into a loadable library.

Modules:
 -  batchmddftsolver:   Batch, multi-dimensional DFT solver
 -  dftsolver:          One Dimension DFT solver
 -  hockneysolver:      Hockney problem solver
 -  mddftsolver:        Multi-dimensional DFT solver
 -  mdprdftsolver:      Multi-dimensional packed real DFT (MDPRDFT) solver
 -  mdrconvsolver:      Three-dimensional Real Cyclic Convolution
 -  mdrfsconvsolver:    Three-dimensional Free Space Convolution
 -  metadata:           Extract metadata from binary file (i.e., library)
 -  spiral:             Handle interface to SPIRAL code generator
 -  spsolver:           Base classes for SpiralPy
 -  stepphasesolver:    StepPhase problem solver

"""

from .spiral import *

import sys
import numpy as _numpy

try:
    import cupy as _cupy
except ModuleNotFoundError:
    _cupy = None

__version__ = '1.0.3'


from .constants import *

def get_array_module(*args):
    if _cupy != None:
        return _cupy.get_array_module(*args)
    else:
        return _numpy


def has_ROCm():
    if _cupy != None:
        return (_cupy._environment.get_rocm_path() != None)
    else:
        return False

