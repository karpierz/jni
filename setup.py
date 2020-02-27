# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
from os import path
from io import open
from glob import glob
from setuptools import setup, Extension

USE_CYTHON = False  # command line option, try-import, ...

ext = ".pyx" if USE_CYTHON else ".c"
ext_modules = [Extension(name="jni.cython.jni",
                         sources=["src/jni/cython/jni" + ext])]
if ext == ".pyx":
    from Cython.Build    import cythonize
    from Cython.Compiler import Options
    Options.docstrings         = False
    Options.emit_code_comments = False
    ext_modules = cythonize(ext_modules, language_level=sys.version_info[0])#, force=True)

ext_modules += [Extension(name="jni.capi.jni",
                          sources=["src/jni/capi/jni.c"])]

top_dir = path.dirname(path.abspath(__file__))
with open(glob(path.join(top_dir, "src/*/__about__.py"))[0],
          encoding="utf-8") as f:
    class about: exec(f.read(), None)

setup(
    name             = about.__title__,
    version          = about.__version__,
    description      = about.__summary__,
    url              = about.__uri__,
    download_url     = about.__uri__,

    author           = about.__author__,
    author_email     = about.__email__,
    maintainer       = about.__maintainer__,
    maintainer_email = about.__email__,
    license          = about.__license__,

    #ext_modules = ext_modules,
)
