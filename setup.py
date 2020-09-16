# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
from os import path
from io import open
from glob import glob
from setuptools import setup, Extension

top_dir = path.dirname(path.abspath(__file__))

GEN_CFFI = not path.exists("src/jni/cffi/jni.py")
if GEN_CFFI:
    def build_ffi(src_dir, emit_jni_i=False):
        import sys
        from os import path
        import cffi
        sys.path.insert(0, src_dir)
        from jni._util import Preprocessor
        sys.path.pop(0)
        with open(path.join(src_dir, "jni/cffi/jni.h"),
                  "r", encoding="utf-8") as f:
            source = f.read()
        source = Preprocessor().preprocess(source,
            define_macros = (
                ("JNICALL",   ""),
                ("JNIIMPORT", ""),
                ("JNIEXPORT", ""),
            ),
            undef_macros = (
                "_JAVASOFT_JNI_H_",
                "__cplusplus",
                "JNI_TYPES_ALREADY_DEFINED_IN_JNI_MD_H",
                "_JNI_IMPLEMENTATION_",
            ))
        if emit_jni_i:
            with open(path.join(src_dir, "jni/cffi/jni.i"),
                      "w", encoding="utf-8") as f:
                print(source, file=f)
        ffi = cffi.FFI()
        ffi.set_source("jni", None)
        ffi.cdef("// temporary for cffi")
        ffi.cdef("typedef void* va_list;")
        ffi.cdef(source)
        ffi.compile(tmpdir=path.join(src_dir, "jni/cffi"))
    build_ffi(path.join(top_dir, "src"))

GEN_CYTHON = (not path.exists("src/jni/cython/jni.c") or
              not path.exists("src/jni/cython/jni.h"))
ext = ".pyx" if GEN_CYTHON else ".c"
ext_modules = [Extension(name="jni.cython.jni",
                         language="c",
                         sources=["src/jni/cython/jni" + ext])]
if GEN_CYTHON:
    from Cython.Build    import cythonize
    from Cython.Compiler import Options
    Options.docstrings         = False
    Options.emit_code_comments = False
    ext_modules = cythonize(ext_modules, language_level=sys.version_info.major,
                            force=True)#, show_all_warnings=True)

platform = "linux" if sys.platform.startswith("linux") else sys.platform
ext_modules += [Extension(name="jni.capi.jni",
                          language="c",
                          include_dirs=["src/jni/capi/java/jdk/include/"+ platform],
                          sources=["src/jni/capi/jni.c"])]

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

    ext_modules = ext_modules,
)
