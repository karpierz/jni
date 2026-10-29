# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

# distutils: language=c

from __future__ import absolute_import

import platform

if platform.win32_ver()[0]:
    from ctypes import WinDLL as DLL
    try:
        from _ctypes import FreeLibrary as dlclose
    except ImportError:
        def dlclose(handle: int, /) -> None:
            return
else:
    from ctypes  import CDLL    as DLL
    from _ctypes import dlclose as dlclose

from libc.stdint cimport uintptr_t  # noqa: E999

# JNI Types

# JNIEnv_ = cy.struct(
#     functions = const JNINativeInterface_*,
# )
#
# JavaVM_ = cy.struct(
#     functions = const JNIInvokeInterface_*,
# )

# eof jni.h

#from .jni cimport *

#cdef float eggs(float f, unsigned long n):
#    print(cython.cast("char*", b"ccc"))
#    return f * n

#cdef class WaveFunction(JavaVMOption):
#    pass

#cdef extern from "foo_nominal.h":
#
#    ctypedef class foo_extension.Foo [object JavaVMOption]:
#        cdef:
#            int field0 "f0"
#            int field1 "f1"
#            int field2 "f2"
#
#def sum(Foo f) except -1:
#    return f.field0 + f.field1 + f.field2

ctypedef jint (__stdcall *JNI_GetDefaultJavaVMInitArgs_ptr)(void* args)
ctypedef jint (__stdcall *JNI_CreateJavaVM_ptr)(JavaVM** pvm, void** penv, void* args)
ctypedef jint (__stdcall *JNI_GetCreatedJavaVMs_ptr)(JavaVM** pvm, jsize size, jsize* nvms)

def load(dll_path, handle=None, __dlclose=dlclose):

    import ctypes as ct
    import os
    try:
        if isinstance(dll_path, os.PathLike): dll_path = str(dll_path)
        dll = DLL(dll_path, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError("{}".format(exc)) from None

    def JNI_GetDefaultJavaVMInitArgs(args, __dll=dll):
        cdef JNI_GetDefaultJavaVMInitArgs_ptr GetDefaultJavaVMInitArgs = <JNI_GetDefaultJavaVMInitArgs_ptr> \
            <long long>ct.cast(__dll.JNI_GetDefaultJavaVMInitArgs, ct.c_void_p).value
        cdef jint result = GetDefaultJavaVMInitArgs(<void*>args)
        return result

    def JNI_CreateJavaVM(pvm, penv, args, __dll=dll):
        cdef JavaVM** p_pvm  # = pointer(pvm)
        cdef JNIEnv** p_penv # = pointer(penv)
        cdef void*      p_args # = pointer(args)
        cdef JNI_CreateJavaVM_ptr CreateJavaVM = <JNI_CreateJavaVM_ptr> \
            <long long>ct.cast(__dll.JNI_CreateJavaVM, ct.c_void_p).value
        cdef jint result = CreateJavaVM(p_pvm, <void**>p_penv, <void*>p_args)
        #_as_CData(pvm).c_data  = _as_CData(p_pvm[0]).c_data
        #_as_CData(penv).c_data = _as_CData(p_penv[0]).c_data
        return result

    def JNI_GetCreatedJavaVMs(pvm, size, nvms, __dll=dll):
        cdef JNI_GetCreatedJavaVMs_ptr GetCreatedJavaVMs = <JNI_GetCreatedJavaVMs_ptr> \
            <long long>ct.cast(__dll.JNI_GetCreatedJavaVMs, ct.c_void_p).value
        cdef jint result = <long long>GetCreatedJavaVMs#(_itself_or_NULL(pvm), size, nvms)
        return result

    JNI = type("JNI", (), dict(dll=dll, dllclose=classmethod(lambda cls, __dlclose=__dlclose: __dlclose(cls.dll._handle))))
    JNI.GetDefaultJavaVMInitArgs = JNI_GetDefaultJavaVMInitArgs
    JNI.CreateJavaVM             = JNI_CreateJavaVM
    JNI.GetCreatedJavaVMs        = JNI_GetCreatedJavaVMs

    return JNI

#From Jnnius
#
#cdef void create_jnienv() except *:
#    cdef JavaVM* jvm
#    cdef JavaVMInitArgs args
#    cdef JavaVMOption *options
#    cdef int ret
#    cdef bytes py_bytes
#    cdef void *handle
#    import jnius_config
#
#    JAVA_HOME = os.getenv('JAVA_HOME') or find_java_home()
#    if JAVA_HOME is None or JAVA_HOME == '':
#        raise SystemError("JAVA_HOME is not set, and unable to guess JAVA_HOME")
#    cdef str JNIUS_LIB_SUFFIX = get_jnius_lib_location(JNIUS_PLATFORM)
#
#    IF JNIUS_PYTHON3:
#        try:
#            jnius_lib_suffix = JNIUS_LIB_SUFFIX.decode("utf-8")
#        except AttributeError:
#            jnius_lib_suffix = JNIUS_LIB_SUFFIX
#        lib_path = str_for_c(os.path.join(JAVA_HOME, jnius_lib_suffix))
#    ELSE:
#        lib_path = str_for_c(os.path.join(JAVA_HOME, JNIUS_LIB_SUFFIX))
#
#    handle = dlopen(lib_path, RTLD_NOW | RTLD_GLOBAL)
#
#    if handle == NULL:
#        raise SystemError("Error calling dlopen({0}): {1}".format(lib_path, dlerror()))
#
#    cdef void *jniCreateJVM = dlsym(handle, b"JNI_CreateJavaVM")
#
#    if jniCreateJVM == NULL:
#       raise SystemError("Error calling dlfcn for JNI_CreateJavaVM: {0}".format(dlerror()))
#
#    optarr = jnius_config.options
#    optarr.append("-Djava.class.path=" + jnius_config.expand_classpath())
#
#    optarr = [str_for_c(x) for x in optarr]
#    options = <JavaVMOption*>malloc(sizeof(JavaVMOption) * len(optarr))
#    for i, opt in enumerate(optarr):
#        options[i].optionString = <bytes>(opt)
#        options[i].extraInfo = NULL
#
#    args.version = JNI_VERSION_1_6
#    args.options = options
#    args.nOptions = len(optarr)
#    args.ignoreUnrecognized = JNI_FALSE
#
#    ret = (<jint (*)(JavaVM **pvm, void **penv, void *args)> jniCreateJVM)(&jvm, <void **>&_platform_default_env, &args)
#    free(options)
#
#    if ret != JNI_OK:
#        raise SystemError("JVM failed to start: {0}".format(ret))
#
#    jnius_config.vm_running = True
#    import traceback
#    jnius_config.vm_started_at = ''.join(traceback.format_stack())
#
#cdef JNIEnv *get_platform_jnienv() except NULL:
#    if _platform_default_env == NULL:
#        create_jnienv()
#    return _platform_default_env

del platform
del dlclose
