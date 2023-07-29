#! python

"""
usage: run-dft.py size [ F|I [ d|s [ GPU|CPU ]]]
  size >= 2
  F  = Forward, I = Inverse           (default: Forward)
  d  = double, s = single precision   (default: double precision)
                                    
  (GPU is default target unless none exists or no CuPy)
  
1D complex FFT
"""

import spiralpy as sw
from spiralpy.dftsolver import *
import numpy as np
import sys

def usage():
    print(__doc__.strip())
    sys.exit()

try:
    n = int(sys.argv[1])
except:
    usage()
    
if n < 2:
    usage()

k = SP_FORWARD
if len(sys.argv) > 2:
    if sys.argv[2] == "I":
        k = SP_INVERSE

c_type = 'double'
cxtype = np.cdouble
if len(sys.argv) > 3:
    if sys.argv[3] == "s":
        c_type = 'float'
        cxtype = np.csingle

if len ( sys.argv ) > 4:
    plat_arg = sys.argv[4]
else:
    plat_arg = "GPU"

if plat_arg == 'GPU' and (cp != None):
    platform = SP_HIP if sw.has_ROCm() else SP_CUDA
    forGPU = True
    xp = cp
else:
    platform = SP_CPU
    forGPU = False
    xp = np

opts = { SP_OPT_REALCTYPE : c_type, SP_OPT_PLATFORM : platform }

p1 = DftProblem(n, k)
s1 = DftSolver(p1, opts)

src = np.zeros(n, cxtype)

for i in range (n):
    vr = np.random.random()
    vi = np.random.random()
    src[i] = vr + vi * 1j
    
xp = np
if forGPU:    
    src = cp.asarray(src)
    xp = cp    
        
resP = s1.runDef(src)
resC = s1.solve(src)

diff = xp.max ( np.absolute ( resC - resP ) )
msg = ' ' if diff < 1e-7 else ' NOT '
print ( f'Python/C transforms are{msg}equivalent, diff = {diff}' )
