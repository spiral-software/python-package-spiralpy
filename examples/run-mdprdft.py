#! python
# examples/run-mdprdft.py
#
# Copyright 2018-2023, Carnegie Mellon University
# All rights reserved.
#
# See LICENSE (https://github.com/spiral-software/python-package-spiralpy/blob/main/LICENSE)


"""
usage: run-mdprdft.py sz [ F|I [ d|s [ GPU|CPU [Fortran]]]
  sz is N or N1,N2,.. all N >= 2, single N implies 3D cube
  F  = Forward, I = Inverse           (default: Forward)
  d  = double, s = single precision   (default: double precision)
  GPU is default target unless none exists or no CuPy
  C ordering is default unless Fortran specified
                                    
  (GPU is default target unless none exists or no CuPy)
  
Three-dimensional real-to-complex FFT (inverse is complex-to-real)
"""

from spiralpy.mdprdftsolver import *
import numpy as np
try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None
import sys

def usage():
    print(__doc__.strip())
    sys.exit()
   
# array dimensions
try:
  nnn = sys.argv[1].split(',')
  n1 = int(nnn[0])
  n2 = (lambda:n1, lambda:int(nnn[1]))[len(nnn) > 1]()
  n3 = (lambda:n2, lambda:int(nnn[2]))[len(nnn) > 2]()
  dims = [n1,n2,n3]
except:
  usage()
  
if any(n < 2 for n in dims):
    usage()

# direction, SP_FORWARD or SP_INVERSE
k = SP_FORWARD    
if len(sys.argv) > 2:
    if sys.argv[2] == "I":
        k = SP_INVERSE
 
# base C type, 'float' or 'double'
c_type = 'double'
ftype = np.double
cxtype = np.cdouble       
if len(sys.argv) > 3:
    if sys.argv[3] == "s":
        c_type = 'float'
        ftype = np.single
        cxtype = np.csingle
        
if len ( sys.argv ) > 4:
    plat_arg = sys.argv[4]
else:
    plat_arg = 'GPU'
    
order = 'C'
if (len ( sys.argv ) > 5) and (sys.argv[5].lower() == 'fortran'):
    order = 'F'

if plat_arg == 'GPU' and (cp != None):
    platform = SP_HIP if sp.has_ROCm() else SP_CUDA
    forGPU = True
    xp = cp
else:
    platform = SP_CPU
    forGPU = False 
    xp = np

opts = { SP_OPT_REALCTYPE : c_type, SP_OPT_PLATFORM : platform }
if order == 'F':
    opts[SP_OPT_COLMAJOR] = True
   
p1 = MdprdftProblem(dims, k)
s1 = MdprdftSolver(p1, opts)

xp = np    
if forGPU:
    xp = cp

if k == SP_FORWARD:
    # build full-size array of real
    src = xp.ones(tuple(dims), ftype)
    for i in range(dims[0]):
        for j in range(dims[1]):
            for k in range(dims[2]):
                vr = np.random.random()
                src[i,j,k] = vr
else:
    # build half-size array of complex
    dims2 = s1.dimensionsCX()
    src = xp.ones(tuple(dims2), cxtype)
    for i in range(dims2[0]):
        for j in range(dims2[1]):
            for k in range(dims2[2]):
                vr = np.random.random()
                vi = np.random.random()
                src[i,j,k] = vr + vi * 1j

dstP = s1.runDef(src)
dstC = s1.solve(src)

diff = xp.max ( xp.absolute ( dstC - dstP ) )
msg = ' ' if diff < 1e-7 else ' NOT '
print ( f'Python/C transforms are{msg}equivalent, diff = {diff}' )
