# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

import sys
from pathlib import Path
from setuptools import setup, Extension
import platform
is_graalpy = (platform.python_implementation().lower() == "graalvm")

top_dir  = Path(__file__).resolve().parent
src_dir  = top_dir/"src"
cffi_dir = src_dir/"jni/cffi"
cyth_dir = src_dir/"jni/cython"
capi_dir = src_dir/"jni/capi"

GEN_CFFI = not (cffi_dir/"jni.py").exists()
if GEN_CFFI and not is_graalpy:
    def build_ffi(src_dir, emit_jni_i=False):
        import sys
        import cffi
        sys.path.insert(0, str(src_dir))
        from jni._util import Preprocessor
        sys.path.pop(0)
        jni_h_path = cffi_dir/"jni.h"
        source = jni_h_path.read_text(encoding="utf-8")
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
            jni_i_path = cffi_dir/"jni.i"
            jni_i_path.write_text(source, newline="",
                                  encoding="utf-8")
        ffi = cffi.FFI()
        ffi.set_source("jni", None)
        ffi.cdef("// temporary for cffi")
        ffi.cdef("typedef void* va_list;")
        ffi.cdef(source)
        ffi.compile(tmpdir=str(cffi_dir))
    build_ffi(src_dir)

GEN_CYTHON = (not (cyth_dir/"jni.c").exists() or
              not (cyth_dir/"jni.h").exists())
ext = ".pyx" if GEN_CYTHON else ".c"
ext_modules = [Extension(name="jni.cython.jni", language="c",
                         sources=["src/jni/cython/jni" + ext])]
if GEN_CYTHON:
    from Cython.Build    import cythonize
    from Cython.Compiler import Options
    Options.docstrings         = False
    Options.emit_code_comments = False
    ext_modules = cythonize(ext_modules,
                            language_level=sys.version_info.major,
                            force=True)#, show_all_warnings=True)

platform = ("linux" if sys.platform.startswith("linux") else
            "android" if hasattr(sys, "getandroidapilevel") else sys.platform)
ext_modules += [Extension(name="jni.capi.jni", language="c",
                          include_dirs=["include/jdk", "include/jdk/" + platform],
                          sources=["src/jni/capi/jni.c"])]

setup(ext_modules=ext_modules)
