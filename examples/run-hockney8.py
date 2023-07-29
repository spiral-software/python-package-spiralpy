#! python

"""
usage: run-hockney8.py

  (no arguments)
  
size 8 Hockney convolution on CPU
"""

from spiralpy.hockneysolver import *
import numpy as np

p1 = HockneyProblem(8,3,5)
s1 = HockneySolver(p1, {SP_OPT_PLATFORM : SP_CPU, SP_OPT_PRINTRULETREE : True})

input_data = s1.buildTestInput()

output_Py = s1.runDef(input_data)
output_C = s1.scale(s1.solve(input_data))

diff = np.max ( np.absolute (  output_Py - output_C ))
msg = ' ' if diff < 1e-7 else ' NOT '
print ( f'Python/C transforms are{msg}equivalent, diff = {diff}' )
