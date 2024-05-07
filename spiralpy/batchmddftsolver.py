# spiralpy/batchmddftsolver.py
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

class BatchMddftProblem(SPProblem):
    """Define Batch MDDFT problem."""

    def __init__(self, dims, batchSz, k=SP_FORWARD):
        """Setup problem specifics for Batch MDDFT solver.
        
        Arguments:
        dims      -- dimensions of individual 3D DFT
        batchSz   -- batch size
        k         -- direction, defaulkt SP_FORWARD
        """
        super(BatchMddftProblem, self).__init__(dims, k)
        self._batchSz = batchSz
        
    def szBatch(self):
        return self._batchSz
        

class BatchMddftSolver(SPSolver):
    def __init__(self, problem: BatchMddftProblem, opts = {}):
        if not isinstance(problem, BatchMddftProblem):
            raise TypeError("problem must be a BatchMddftProblem")
 
        b = str(problem.szBatch())
        typ = 'z'
        if opts.get(SP_OPT_REALCTYPE, 0) == 'float':
            typ = 'c'
        ns = 'x'.join([str(n) for n in problem.dimensions()])
        direc = '_fwd_' if problem.direction() == SP_FORWARD else '_inv_'
        namebase = typ + 'batchmddft' + direc + ns + '_' + b
            
        opts[SP_OPT_METADATA] = True
        
        super(BatchMddftSolver, self).__init__(problem, namebase, opts)

    def runDef(self, src):
        """Solve using internal Python definition."""
        
        dims = self._problem.dimensions()
        b = self._problem.szBatch()
        dimsTuple = tuple([b]) + tuple(dims)
        
        xp = get_array_module(src)
        
        if self._problem.direction() == SP_FORWARD:
            out = xp.fft.fftn(src, axes=(1,2,3))
        else:
            out = xp.fft.ifftn(src, axes=(1,2,3))
        
        return out
    
       
    def buildTestInput(self):
        dims = self._problem.dimensions()
        b = self._problem.szBatch()
        dimsTuple = tuple([b]) + tuple(dims)
        
        if self._opts.get(SP_OPT_REALCTYPE) == "float":
            cxtype = np.csingle
        else:
            cxtype = np.cdouble
               
        src = np.ones(dimsTuple, cxtype)
        for  k in range (np.size(src)):
            vr = np.random.random()
            vi = np.random.random()
            src.itemset(k,vr + vi * 1j)
        if self._genCuda or self._genHIP:    
            src = cp.asarray(src)
        
        return src
        
        
    def _trace(self):
        pass
    
    def solve(self, src, dst=None):
        """Call SPIRAL-generated function."""
    
        if type(dst) == type(None):
            xp = get_array_module(src)
            dims = self._problem.dimensions()
            b = self._problem.szBatch()
            dimsTuple = tuple([b]) + tuple(dims)
            dst = xp.zeros(dimsTuple, src.dtype)
        
        self._func(dst, src)
        if self._problem.direction() == SP_INVERSE:
            xp = get_array_module(dst)
            scale = xp.size(dst) / self._problem.szBatch()
            xp.divide(dst, scale, out=dst)
        return dst

    def _writeScript(self, script_file):
        nameroot = self._namebase
        filename = nameroot
        filetype = '.c'
        if self._genCuda:
            filetype = '.cu'
        if self._genHIP:
            filetype = '.cpp'

        print('Load(fftx);', file = script_file)
        print('ImportAll(fftx);', file = script_file) 
        print('', file = script_file)
            
        print('t := let(batch := ' + str(self._problem.szBatch()) + ',', file = script_file)
        print('    apat := When(true, APar, AVec),', file = script_file)
        print('    ns := ' + str(self._problem.dimensions()) + ',', file = script_file)
        print('    k := ' + str(self._problem.direction()) + ',', file = script_file)
        print('    name := "' + nameroot + '",', file = script_file)
        print('    TFCall(TRC(TTensorI(MDDFT(ns, k), batch, apat, apat)),', file = script_file)
        print('        rec(fname := name, params := []))', file = script_file)
        print(');', file = script_file)
        print('', file = script_file)
        
        if self._genCuda:
            print('conf := LocalConfig.fftx.confGPU();', file = script_file)
        elif self._genHIP:
            print ( 'conf := FFTXGlobals.defaultHIPConf();', file = script_file )
        else:
            print('conf := LocalConfig.fftx.defaultConf();', file = script_file)

        print('opts := conf.getOpts(t);', file = script_file)
        if self._genCuda or self._genHIP:
            print('opts.wrapCFuncs := true;', file = script_file)
        if self._opts.get(SP_OPT_REALCTYPE) == "float":
            print('opts.TRealCtype := "float";', file = script_file)    
        if self._printRuleTree:
            print("opts.printRuleTree := true;", file = script_file)
        print('', file = script_file)  

        print('tt := opts.tagIt(t);', file = script_file)
        print('c := opts.fftxGen(tt);', file = script_file)
        print('PrintTo("' + filename + filetype + '", opts.prettyPrint(c));', file = script_file)
        print('', file = script_file)
        
    def _setFunctionMetadata(self, obj):
        obj[SP_KEY_TRANSFORMTYPE] = SP_TRANSFORM_BATMDDFT
        obj[SP_KEY_BATCHSIZE] = self._problem.szBatch()
        


        
    
