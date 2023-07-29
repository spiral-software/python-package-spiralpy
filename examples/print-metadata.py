"""
Print meta data in shared library files in spiralpy .libs directory 
and in directories specified in SP_LIBRARY_PATH
"""

import os
import site
import spiralpy
from spiralpy.metadata import *
from pprint import *

package = 'spiralpy'            ## must set this as the example has no access to __package__
libsDir = os.path.join(site.USER_BASE, SP_SHARE_DIR, package, SP_LIBSDIR)

dirlist = [libsDir]

libpath = os.getenv(SP_LIBRARY_PATH)
if libpath != None:
    sep = ';' if sys.platform == 'win32' else ':'
    paths = libpath.split(sep)
    dirlist = dirlist + paths

md = []
for libdir in dirlist:    
    md = md + metadataInDir(libdir)

pprint(md)
