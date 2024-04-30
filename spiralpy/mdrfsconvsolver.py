
from spiralpy import *
from spiralpy.spsolver import *
import numpy as np
import ctypes
import sys

try:
    import cupy as cp
except ModuleNotFoundError:
    cp = None

class MdrfsconvProblem(SPProblem):
    """Define Mdrfsconv problem."""

    def __init__(self, ns):
        """Setup problem specifics for Mdrfsconv solver.
        
        Arguments:
        ns      -- shape (list) of MDRCONV box of reals
        """
        super(MdrfsconvProblem, self).__init__(ns)


class MdrfsconvSolver(SPSolver):
    def __init__(self, problem: MdrfsconvProblem, opts = {}):
        if not isinstance(problem, MdrfsconvProblem):
            raise TypeError("problem must be an MdrfsconvProblem")
        
        typ = 'd'
        self._ftype = np.double
        self._cxtype = np.cdouble
        if opts.get(SP_OPT_REALCTYPE, 0) == 'float':
            typ = 'f'
            self._ftype = np.single
            self._cxtype = np.csingle
        
        ns = 'x'.join([str(n) for n in problem.dimensions()])
        namebase = typ + 'Mdrfsconv_' + ns
            
        opts[SP_OPT_METADATA] = True
        
        super(MdrfsconvSolver, self).__init__(problem, namebase, opts)

        
    def _trace(self):
        """Trace execution for generating Spiral script"""
        self._tracingOn = True
        self._callGraph = []
        (src,sym) = self.buildTestInput()
        self.runDef(src,sym)
        self._tracingOn = False
        for i in range(len(self._callGraph)-1):
            self._callGraph[i] = self._callGraph[i] + ','
            
    def runDef(self, src, sym):
        """Solve using internal Python definition."""

        # Mdrfsconv problem dimensions
        dims = self._problem.dimensions()
        Nd1 = dims[0]
        Nd2 = dims[1]
        Nd3 = dims[2]
        Ns1 = Nd1
        Ns2 = Nd2
        Ns3 = Nd3
        N1 = Nd1 * 2
        N2 = Nd2 * 2
        N3 = Nd3 * 2
        
    
        # Mdrfsconv operations
        In = self.zeroEmbedBox(src, ((Ns1,0),(Ns2,0),(Ns3,0))) # zero pad input data 
        FFT = self.rfftn(In)            # execute real forward dft on rank 3 data      
        P = self.pointwise(FFT, sym) # execute pointwise operation
        IFFT = self.irfftn(P, shape=In.shape)  # execute real backward dft on rank 3 data
        return self.extract(IFFT, ((N1, Nd1),(N2, Nd2),(N3, Nd3)))   # extract data from corner cube
    
    def solve(self, src, sym, dst=None):
        """Call SPIRAL-generated code"""
        
        xp = sp.get_array_module(src)
        
        #slice sym if it's a cube
        shape = sym.shape
        if shape[0] == shape[2]:
            N = shape[0]
            Nx = (N // 2) + 1
            sym = xp.ascontiguousarray(sym[:, :, :Nx])
        
        dims = self._problem.dimensions()
        n1 = dims[0]
        n2 = dims[1]      
        n3 = dims[2]            
        if type(dst) == type(None):
            dst = xp.zeros((n1,n2,n3), src.dtype)
        self._func(dst, src, sym)
        xp.divide(dst, n1*n2*n3*8, out=dst)
        return dst
 
    def _func(self, dst, src, sym):
        """Call the SPIRAL generated main function"""
                
        xp = sp.get_array_module(src)
        
        if xp == np: 
            if self._genCuda or self._genHIP:
                raise RuntimeError('GPU function requires CuPy arrays')
            # NumPy array on CPU
            return self._MainFunc( 
                    dst.ctypes.data_as(ctypes.c_void_p),
                    src.ctypes.data_as(ctypes.c_void_p),
                    sym.ctypes.data_as(ctypes.c_void_p)  )
        else:
            if not self._genCuda and not self._genHIP:
                raise RuntimeError('CPU function requires NumPy arrays')
            # CuPy array on GPU
            dstdev = ctypes.cast(dst.data.ptr, ctypes.POINTER(ctypes.c_void_p))
            srcdev = ctypes.cast(src.data.ptr, ctypes.POINTER(ctypes.c_void_p))
            symdev = ctypes.cast(sym.data.ptr, ctypes.POINTER(ctypes.c_void_p))
            return self._MainFunc(dstdev, srcdev, symdev)
  

    def _writeScript(self, script_file):
        nameroot = self._namebase
        filename = nameroot
        filetype = '.c'
        if self._genCuda:
            filetype = '.cu'
        if self._genHIP:
            filetype = '.cpp'
        
        print("Load(fftx);", file = script_file)
        print("ImportAll(fftx);", file = script_file)
        print("", file = script_file)
        if self._genCuda:
            print("conf := LocalConfig.fftx.confGPU();", file = script_file)
        elif self._genHIP:
            print ( 'conf := FFTXGlobals.defaultHIPConf();', file = script_file )
        else:
            print("conf := LocalConfig.fftx.defaultConf();", file = script_file)

        print("", file = script_file)
        print('t := let(symvar := var("sym", TPtr(TReal)),', file = script_file)
        print("    TFCall(", file = script_file)
        print("        Compose([", file = script_file)
        for i in range(len(self._callGraph)):
            print("            " + self._callGraph[i], file = script_file)
        print("        ]),", file = script_file)
        print('        rec(fname := "' + nameroot + '", params := [symvar])', file = script_file)
        print("    )", file = script_file)
        print(");", file = script_file)
        print("", file = script_file)
        print("opts := conf.getOpts(t);", file = script_file)

        if self._genCuda or self._genHIP:
            print('opts.wrapCFuncs := true;', file = script_file)

        if self._opts.get(SP_OPT_REALCTYPE) == "float":
            print('opts.TRealCtype := "float";', file = script_file)

        if self._printRuleTree:
            print("opts.printRuleTree := true;", file = script_file)

        print("tt := opts.tagIt(t);", file = script_file)
        print("", file = script_file)
        print("c := opts.fftxGen(tt);", file = script_file)
        print('PrintTo("' + filename + filetype + '", opts.prettyPrint(c));', file = script_file)
        print("", file = script_file)
    
    def buildTestInput(self):
        """ Build test input cube """
        
        xp = cp if self._genCuda or self._genHIP else np
        dims = self._problem.dimensions()
        n1 = dims[0]
        n2 = dims[1]
        n3 = dims[2]
        
        testSrc = xp.random.rand(n1,n2,n3).astype(self._ftype)
        
        symIn = xp.random.rand(n1*2,n2*2,n3*2).astype(self._ftype)
        testSym = xp.fft.rfftn(symIn)
        
        #NumPy returns Fortran ordering from FFTs, and always double complex
        if xp == np:
            testSym = np.asanyarray(testSym, dtype=self._cxtype, order='C')        
        
        return (testSrc, testSym)
    
    def _setFunctionMetadata(self, obj):
        obj[SP_KEY_TRANSFORMTYPE] = SP_TRANSFORM_MDRFSCONV
     

    
