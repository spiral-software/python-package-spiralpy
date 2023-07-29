#! python

"""
usage: run-mdrconv.py sz [ d|s [ GPU|CPU ]]
    sz is N or N1,N2,N3 all N >= 4, single N implies 3D cube
    d  = double, s = single precision   (default: double precision)
    (GPU is default target unless none exists or no CuPy)                     

Three-dimensional real cyclic convolution
"""

import sys
from spiralpy.mdrconvsolver import *
import numpy as np
try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None

def usage():
    print(__doc__.strip())
    sys.exit()

##  array dimensions
try:
    nnn = sys.argv[1].split(',')
    n1 = int(nnn[0])
    n2 = (lambda:n1, lambda:int(nnn[1]))[len(nnn) > 1]()
    n3 = (lambda:n2, lambda:int(nnn[2]))[len(nnn) > 2]()
    dims = [n1,n2,n3]
except:
    usage()

if any(n < 4 for n in dims):
    usage()

c_type = 'double'
src_type = np.double
if len(sys.argv) > 2:
    if sys.argv[2] == "s":
        c_type = 'float'
        src_type = np.single

if len ( sys.argv ) > 3:
    plat_arg = sys.argv[3]
else:
    plat_arg = 'GPU'

if plat_arg == 'GPU' and (cp != None):
    platform = SP_HIP if sp.has_ROCm() else SP_CUDA
    forGPU = True
    xp = cp
else:
    platform = SP_CPU
    forGPU = False 
    xp = np

opts = {SP_OPT_REALCTYPE : c_type, SP_OPT_PLATFORM : platform}

xp = np
if forGPU:
    xp = cp

p1 = MdrconvProblem(dims)
s1 = MdrconvSolver(p1, opts)

(testIn, symbol) = s1.buildTestInput()

dstP = s1.runDef(testIn, symbol)
dstC = s1.solve(testIn, symbol)

diff = xp.max(xp.absolute(dstC - dstP))
msg = ' ' if diff < 1e-7 else ' NOT '
print ( f'Python/C transforms ({plat_arg}) are{msg}equivalent, diff = {diff}' )


