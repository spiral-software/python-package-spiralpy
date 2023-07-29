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

__version__ = '1.0.1'

# # internal names

# SP_LIBSDIR  = '.libs'

# # environment varibles

# SP_KEEPTEMP      = 'SP_KEEPTEMP'
# SP_LIBRARY_PATH  = 'SP_LIBRARY_PATH'
# SP_PRINTRULETREE = 'SP_PRINTRULETREE'
# SP_WORKDIR       = 'SP_WORKDIR'

# # options

# SP_OPT_COLMAJOR         = 'colmajor'
# SP_OPT_KEEPTEMP         = 'keeptemp'
# SP_OPT_METADATA         = 'metadata'
# SP_OPT_MPI              = 'mpi'
# SP_OPT_PLATFORM         = 'platform'
# SP_OPT_PRINTRULETREE    = 'printruletree'
# SP_OPT_REALCTYPE        = 'realctype'

# # transform direction, 'k'

# SP_FORWARD  = -1
# SP_INVERSE  = 1

# # platforms

# SP_CPU  = 'CPU'
# SP_CUDA = 'CUDA'
# SP_HIP  = 'HIP'

# # metadata

# SP_METADATA_START   = '!!START_METADATA!!'
# SP_METADATA_END     = '!!END_METADATA!!'
# SP_METAFILE_EXT     = '_meta.c'
# SP_METAVAR_EXT      = '_metadata'

# SP_STR_DOUBLE       = 'Double'
# SP_STR_SINGLE       = 'Single'

# SP_STR_FORWARD      = 'Forward'
# SP_STR_INVERSE      = 'Inverse'

# SP_STR_BLOCK        = 'Block'
# SP_STR_UNIT         = 'Unit'

# SP_STR_C            = 'C'
# SP_STR_FORTRAN      = 'Fortran'


# SP_TRANSFORM_BATDFT     = 'BATDFT'
# SP_TRANSFORM_BATMDDFT   = 'BATMDDFT'
# SP_TRANSFORM_DFT        = 'DFT'
# SP_TRANSFORM_MDDFT      = 'MDDFT'
# SP_TRANSFORM_MDRCONV    = 'MDRCONV'
# SP_TRANSFORM_MDRFSCONV  = 'MDRFSCONV'
# SP_TRANSFORM_MDPRDFT    = 'MDPRDFT'
# SP_TRANSFORM_UNKNOWN    = 'UNKNOWN'

# SP_KEY_BATCHSIZE        = 'BatchSize'
# SP_KEY_DESTROY          = 'Destroy'
# SP_KEY_DIMENSIONS       = 'Dimensions'
# SP_KEY_DIRECTION        = 'Direction'
# SP_KEY_EXEC             = 'Exec'
# SP_KEY_FILENAME         = 'Filename'
# SP_KEY_FUNCTIONS        = 'Functions'
# SP_KEY_INIT             = 'Init'
# SP_KEY_METADATA         = 'Metadata'
# SP_KEY_NAMES            = 'Names'
# SP_KEY_ORDER            = 'Order'
# SP_KEY_PLATFORM         = 'Platform'
# SP_KEY_PRECISION        = 'Precision'
# SP_KEY_READSTRIDE       = 'ReadStride'
# SP_KEY_SPIRALBUILDINFO  = 'SpiralBuildInfo'
# SP_KEY_TRANSFORMS       = 'Transforms'
# SP_KEY_TRANSFORMTYPE    = 'TransformType'
# SP_KEY_TRANSFORMTYPES   = 'TransformTypes'
# SP_KEY_WRITESTRIDE      = 'WriteStride'

# if sys.platform == 'win32':
#     SP_SHLIB_EXT = '.dll'
# elif sys.platform == 'darwin':
#     SP_SHLIB_EXT = '.dylib'
# else:
#     SP_SHLIB_EXT = '.so'

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

