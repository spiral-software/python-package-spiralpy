# spiralpy/dftsolver.py
#
# Copyright 2018-2023, Carnegie Mellon University
# All rights reserved.
#
# See LICENSE (https://github.com/spiral-software/python-package-spiralpy/blob/main/LICENSE)


from spiralpy import *
from spiralpy.spsolver import *
import numpy as np
try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None
import ctypes
import sys
import random

class DftProblem(SPProblem):
    """Define 1D DFT problem."""

    def __init__(self, n, k=SP_FORWARD, batchDims=[1,1], readStride=1, writeStride=1):
        """Setup problem specifics for 1D DFT solver.
        
        Arguments:
        k           -- direction
        n           -- dimension of 1D DFT
        batchDims   -- dimensions of batch
        readStride  -- unit (1) or block (!=1)
        writeStride -- unit (1) or block (!=1)
        """
        super(DftProblem, self).__init__([n], k)
        self._batchDims = batchDims
        self._readStride = readStride
        self._writeStride = writeStride


class DftSolver(SPSolver):
    def __init__(self, problem: DftProblem, opts = {}):
        if not isinstance(problem, DftProblem):
            raise TypeError("problem must be a DftProblem")
        
        typ = 'z'
        if opts.get(SP_OPT_REALCTYPE, 0) == 'float':
            typ = 'c'
        n = str(problem.dimN())
        c = '_'
        namebase = ''
        if problem.direction() == SP_FORWARD:
            namebase = typ + 'dft_fwd' + c + n
        else:
            namebase = typ + 'dft_inv' + c + n
            
        dims = problem._batchDims
        bat = np.prod(dims)
        if bat > 1:
            namebase = namebase + c + 'b' + 'x'.join([str(n) for n in dims])
            namebase = namebase + ('p' if problem._writeStride == 1 else 'v')
            namebase = namebase + ('p' if problem._readStride == 1 else 'v')
            
        opts[SP_OPT_METADATA] = True
        super(DftSolver, self).__init__(problem, namebase, opts)

    def runDef(self, src):
        """Solve using internal Python definition."""
        
        xp = get_array_module(src)

        ax = -1 if self._problem._readStride == 1 else 0
        
        if self._problem.direction() == SP_FORWARD:
            dst = xp.fft.fft(src, axis=ax)
        else:
            dst = xp.fft.ifft(src, axis=ax)
            
        if self._problem._writeStride != self._problem._readStride:
            if self._problem._writeStride != 1:
                # Par Vec
                # new shape is inverse of src
                revdims = src.shape[::-1]
                drt = dst.reshape(np.asarray(revdims[1:]).prod(), revdims[0]).transpose()
                dst = drt.reshape(revdims)
            else:
                # Vec Par
                dims = dst.shape
                drt = dst.reshape(dims[0], np.asarray(dims[1:]).prod()).transpose()
                dst = drt.reshape(dims[::-1])

        return dst
        
    def _trace(self):
        pass

    def solve(self, src, dst=None):
        """Call SPIRAL-generated function."""
        if type(dst) == type(None):
            xp = get_array_module(src)
            if self._problem._writeStride == self._problem._readStride:
                dst = xp.zeros_like(src)
            else:
                # reverse dims
                dims = src.shape[::-1]
                dst = xp.zeros(dims,src.dtype)
        self._func(dst, src)
        return dst

    def _writeScript(self, script_file):
        filename = self._namebase
        nameroot = self._namebase
        filetype = '.c'
        if self._genCuda:
            filetype = '.cu'
        if self._genHIP:
            filetype = '.cpp'
        
        print("Load(fftx);", file = script_file)
        print("ImportAll(fftx);", file = script_file)

        print('', file = script_file)
        
        dft_def = 'DFT(N, ' + str(self._problem.direction()) + ')'
        if self._problem.direction() == SP_INVERSE:
            dft_def = 'Scale(1/N, ' + dft_def + ')'
        
        bdims = self._problem._batchDims
        #bdims_str = '[Ind({0}), Ind({1}), Ind(1)]'.format(bdims[0],bdims[1])
        bdims_str = str(np.prod(bdims))
        
        W = 'APar' if self._problem._writeStride == 1 else 'AVec'
        R = 'APar' if self._problem._readStride == 1 else 'AVec'
        
        print('t := let(', file = script_file) 
        print('    name := "' + nameroot + '",', file = script_file)
        print('    N  := ' + str(self._problem.dimN()) + ',', file = script_file)
        print('    TFCall(TRC(TTensorI(' + dft_def + ', ' + bdims_str + ' ,' + W + ', ' + R +')), rec(fname := name, params := []))', file = script_file)
        print(');', file = script_file)
        
        if self._genCuda:
            print("conf := LocalConfig.fftx.confGPU();", file = script_file) 
        elif self._genHIP:
            print ( 'conf := FFTXGlobals.defaultHIPConf();', file = script_file )
        else:
            print("conf := LocalConfig.fftx.defaultConf();", file = script_file) 

        print("opts := conf.getOpts(t);", file = script_file)
        if self._genCuda or self._genHIP:
            print('opts.wrapCFuncs := true;', file = script_file)

        if self._opts.get(SP_OPT_REALCTYPE) == "float":
            print('opts.TRealCtype := "float";', file = script_file)

        if self._printRuleTree:
            print("opts.printRuleTree := true;", file = script_file)

        print('Add(opts.includes, "<float.h>");',  file = script_file)
        print("tt := opts.tagIt(t);", file = script_file)
        print("", file = script_file)
        print("c := opts.fftxGen(tt);", file = script_file)
        print('PrintTo("' + filename + filetype + '", opts.prettyPrint(c));', file = script_file)
        print("", file = script_file)
    
    def _setFunctionMetadata(self, obj):
        bdims = self._problem._batchDims
        if np.prod(bdims) > 1:
            obj[SP_KEY_TRANSFORMTYPE] = SP_TRANSFORM_BATDFT
            obj[SP_KEY_BATCHSIZE] = int(np.prod(bdims))
            obj[SP_KEY_READSTRIDE]  = SP_STR_UNIT if self._problem._readStride  == 1 else SP_STR_BLOCK
            obj[SP_KEY_WRITESTRIDE] = SP_STR_UNIT if self._problem._writeStride == 1 else SP_STR_BLOCK
        else:
            obj[SP_KEY_TRANSFORMTYPE] = SP_TRANSFORM_DFT



