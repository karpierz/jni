# Copyright (c) 2004-2019 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from __future__ import absolute_import

import sys
from os import path
from setuptools import setup, Extension

USE_CYTHON = True  # command line option, try-import, ...

ext = ".pyx" if USE_CYTHON else ".c"
ext_modules = [Extension(name="jt.jni.cython.jni",
                         sources=["src/jt/jni/cython/jni" + ext])]
if ext == ".pyx":
    from Cython.Build    import cythonize
    from Cython.Compiler import Options
    Options.docstrings         = False
    Options.emit_code_comments = False
    ext_modules = cythonize(ext_modules, language_level=sys.version_info[0])#, force=True)

ext_modules += [Extension(name="jt.jni.capi.jni",
                          sources=["src/jt/jni/capi/jni.c"])] if sys.version_info[0] >= 3 else []

top_dir = path.dirname(path.abspath(__file__))
with open(path.join(top_dir, "src", "jt", "jni", "__about__.py")) as f:
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

    ext_modules = ext_modules,
)
