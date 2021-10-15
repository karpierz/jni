# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

# distutils: language=c

from __future__ import absolute_import

import os
import platform
import ctypes as ct

if platform.win32_ver()[0]:
    from ctypes  import WinDLL      as DLL
    from _ctypes import FreeLibrary as dlclose
else:
    from ctypes  import CDLL    as DLL
    from _ctypes import dlclose as dlclose

from libc.stdint cimport uintptr_t

# JNI Types

cdef class _CData:
    pass

cdef class jint(_CData):
    cdef public c_jint value

    def __init__(self, val=0):
        self.value = val

    def __bool__(self):
        return self.value != 0

cdef class jlong(_CData):
    cdef public c_jlong value

    def __init__(self, val=0):
        self.value = val

    def __bool__(self):
        return self.value != 0

cdef class jbyte(_CData):
    cdef public c_jbyte value

    def __init__(self, val=0):
        self.value = val

    def __bool__(self):
        return self.value != 0

cdef class jboolean(_CData):
    cdef c_jboolean val

    def __init__(self, val=0):
        self.val = val

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        self.val = val

    def __bool__(self):
        return self.val != 0

cdef class jchar(_CData):
    cdef c_jchar val

    def __init__(self, val=u"\0"):
        self.val = <c_jchar>ord(val)

    @property
    def value(self):
        return chr(self.val)

    @value.setter
    def value(self, val):
        self.val = <c_jchar>ord(val)

    def __bool__(self):
        return self.val != 0

cdef class jshort(_CData):
    cdef public c_jshort value

    def __init__(self, val=0):
        self.value = val

    def __bool__(self):
        return self.value != 0

cdef class jfloat(_CData):
    cdef public c_jfloat value

    def __init__(self, val=0.0):
        self.value = val

    def __bool__(self):
        return self.value != 0.0

cdef class jdouble(_CData):
    cdef public c_jdouble value

    def __init__(self, val=0.0):
        self.value = val

    def __bool__(self):
        return self.value != 0.0

jsize = jint

cdef class jobject(_CData):
    cdef c_jobject val

    def __init__(self, val=None):
        self.val = <c_jobject><uintptr_t>val if val is not None else NULL

    @property
    def value(self):
        return int(<uintptr_t>self.val) if self.val is not NULL else None

    @value.setter
    def value(self, val):
        self.val = <c_jobject><uintptr_t>val if val is not None else NULL

    def __bool__(self):
        return self.val != NULL

jclass        = jobject
jthrowable    = jobject
jstring       = jobject
jarray        = jobject
jbooleanArray = jarray
jcharArray    = jarray
jbyteArray    = jarray
jshortArray   = jarray
jintArray     = jarray
jlongArray    = jarray
jfloatArray   = jarray
jdoubleArray  = jarray
jobjectArray  = jarray
jweak         = jobject

cdef class jvalue(_CData):
    cdef c_jvalue this

    @property
    def z(self):
        return self.this.z

    @z.setter
    def z(self, val):
        self.this.z = val.val if isinstance(val, jboolean) else val

    @property
    def b(self):
        return self.this.b

    @b.setter
    def b(self, val):
        self.this.b = val.val if isinstance(val, jbyte) else val

    @property
    def c(self):
        return chr(self.this.c)

    @c.setter
    def c(self, val):
        self.this.c = val.val if isinstance(val, jchar) else <c_jchar>ord(val)

    @property
    def s(self):
        return self.this.s

    @s.setter
    def s(self, val):
        self.this.s = val.val if isinstance(val, jshort) else val

    @property
    def i(self):
        return self.this.i

    @i.setter
    def i(self, val):
        self.this.i = val.val if isinstance(val, jint) else val

    @property
    def j(self):
        return self.this.j

    @j.setter
    def j(self, val):
        self.this.j = val.val if isinstance(val, jlong) else val

    @property
    def f(self):
        return self.this.f

    @f.setter
    def f(self, val):
        self.this.f = val.val if isinstance(val, jfloat) else val

    @property
    def d(self):
        return self.this.d

    @d.setter
    def d(self, val):
        self.this.d = val.val if isinstance(val, jdouble) else val

    @property
    def l(self):
        return int(<uintptr_t>self.this.l) if self.this.l is not NULL else None

    @l.setter
    def l(self, val):
        self.this.l = (<c_jobject>val.val if isinstance(val, jobject) else
                       <c_jobject><uintptr_t>val if val is not None else NULL)

cdef class jfieldID(_CData):
    cdef c_jfieldID val

    def __init__(self, val=None):
        self.val = <c_jfieldID><uintptr_t>val if val is not None else NULL

    @property
    def value(self):
        return int(<uintptr_t>self.val) if self.val is not NULL else None

    @value.setter
    def value(self, val):
        self.val = <c_jfieldID><uintptr_t>val if val is not None else NULL

    def __bool__(self):
        return self.val != NULL

cdef class jmethodID(_CData):
    cdef c_jmethodID val

    def __init__(self, val=None):
        self.val = <c_jmethodID><uintptr_t>val if val is not None else NULL

    @property
    def value(self):
        return int(<uintptr_t>self.val) if self.val is not NULL else None

    @value.setter
    def value(self, val):
        self.val = <c_jmethodID><uintptr_t>val if val is not None else NULL

    def __bool__(self):
        return self.val != NULL

# Return values from jobjectRefType

#from .jni cimport jobjectRefType as c_jobjectRefType
#jobjectRefType = c._jobjectType
#jobjectRefType = c_jobjectRefType

# null constant

cdef c_jobject NULL = <c_jobject>0
#isNULL = lambda jobj, __NULL=NULL: jobj == __NULL

# JNI Native Method Interface.

cdef class JNINativeMethod(_CData):
    cdef c_JNINativeMethod this

    @property
    def name(self):
        return self.this.name if self.this.name is not NULL else None

    @name.setter
    def name(self, val):
        self.this.name = <char*>val if val is not None else NULL

    @property
    def signature(self):
        return self.this.signature if self.this.signature is not NULL else None

    @signature.setter
    def signature(self, val):
        self.this.signature = <char*>val if val is not None else NULL

    @property
    def fnPtr(self):
        return int(<uintptr_t>self.this.fnPtr) if self.this.fnPtr is not NULL else None

    @fnPtr.setter
    def fnPtr(self, val):
        self.this.fnPtr = (<void*>val.val if isinstance(val, jobject) else
                           <void*><uintptr_t>val if val is not None else NULL)

cdef class JNIEnv(_CData):
    cdef c_JNIEnv this
# [...] !!!

# JNI Invocation Interface.

cdef class JavaVM(_CData):
    cdef c_JavaVM this
# [...] !!!

cdef class JavaVMOption(_CData):
    cdef c_JavaVMOption this

    @property
    def optionString(self):
        return self.this.optionString if self.this.optionString is not NULL else None

    @optionString.setter
    def optionString(self, val):
        self.this.optionString = <char*>val if val is not None else NULL

    @property
    def extraInfo(self):
        return int(<uintptr_t>self.this.extraInfo) if self.this.extraInfo is not NULL else None

    @extraInfo.setter
    def extraInfo(self, val):
        self.this.extraInfo = (<void*>val.val if isinstance(val, jobject) else
                               <void*><uintptr_t>val if val is not None else NULL)

cdef class JavaVMInitArgs(_CData):
    cdef c_JavaVMInitArgs this

    @property
    def version(self):
        return self.this.version

    @version.setter
    def version(self, val):
        self.this.version = val.val if isinstance(val, jint) else val

    @property
    def nOptions(self):
        return self.this.nOptions

    @nOptions.setter
    def nOptions(self, val):
        self.this.nOptions = val.val if isinstance(val, jint) else val

    options = property(lambda self:      getattr(self.this, "options"),
                       lambda self, val: setattr(self.this, "options", val))

    @property
    def ignoreUnrecognized(self):
        return self.this.ignoreUnrecognized

    @ignoreUnrecognized.setter
    def ignoreUnrecognized(self, val):
        self.this.ignoreUnrecognized = val.val if isinstance(val, jboolean) else val

cdef class JavaVMAttachArgs(_CData):
    cdef c_JavaVMAttachArgs this

    @property
    def version(self):
        return self.this.version

    @version.setter
    def version(self, val):
        self.this.version = val.val if isinstance(val, jint) else val

    @property
    def name(self):
        return self.this.name if self.this.name is not NULL else None

    @name.setter
    def name(self, val):
        self.this.name = <char*>val if val is not None else NULL

    @property
    def group(self):
        return int(<uintptr_t>self.this.group) if self.this.group is not NULL else None

    @group.setter
    def group(self, val):
        self.this.group = (<c_jobject>val.val if isinstance(val, jobject) else
                           <c_jobject><uintptr_t>val if val is not None else NULL)

# eof jni.h

#from .jni cimport *
#import cython

#addressof = lambda obj,             __cyth=cython: __cyth.address(obj)
#cast      = lambda obj, type,       __cyth=cython: __cyth.cast(type, obj)
#sizeof    = lambda obj_or_type,     __cyth=cython: __cyth.sizeof(obj_or_type)

#cdef cast(type, obj):
#    return cython.cast(type, obj)

#cdef float eggs(float f, unsigned long n):
#    print(cython.cast("char*", b"ccc"))
#    return f * n

#cdef class WaveFunction(c_JavaVMOption):
#    pass

#cdef extern from "foo_nominal.h":
#
#    ctypedef class foo_extension.Foo [object c_JavaVMOption]:
#        cdef:
#            int field0 "f0"
#            int field1 "f1"
#            int field2 "f2"
#
#def sum(Foo f) except -1:
#    return f.field0 + f.field1 + f.field2

#from pprint import pprint
#pprint(vars())

#cdef class Shrubbery:
#    def __new__(self, int w, int l):
#        self.width = w
#        self.length = l

#cdef class JB_Env:
#
#    cdef:
#        c_JNIEnv *env
#
#    def __init__(self):
#        self.env = NULL
#        
#    def __repr__(self):
#        return "<JB_Env at 0x%x>"%(<size_t>(self.env))
#        
#    def __dealloc__(self):
#        self.env = NULL
#        
#    def get_version(self):
#        '''Return the version number as a major / minor version tuple'''
#        cdef:
#            int version
#        version = self.env[0].GetVersion(self.env)
#        return (int(version / 65536), version % 65536)

cdef class Throwable(Exception):

    last = None

    cdef c_jthrowable _cause
    cdef c_jstring    _info

    #def __cinit__(self, c_jthrowable cause=NULL, c_jstring info=NULL):
    #    self._cause = cause
    #    self._info  = info
    #    #super(Throwable, self).__init__(self._cause, self._info)

    cdef c_jthrowable getCause(self):
        return self._cause

    cdef c_jstring getInfo(self):
        return self._info

class JNIException(SystemError):

    reason = {
        JNI_OK:        u"success",
        JNI_ERR:       u"unknown error",
        JNI_EDETACHED: u"thread detached from the VM",
        JNI_EVERSION:  u"JNI version error",
        JNI_ENOMEM:    u"not enough memory",
        JNI_EEXIST:    u"VM already created",
        JNI_EINVAL:    u"invalid arguments",
    }

    def __init__(self, error=JNI_ERR, info=None):
        self._error = error
        self._info  = info
        super().__init__(self.getMessage(), self.getError())

    def getMessage(self):
        prefix = self._info + ": " if self._info else ""
        return prefix + JNIException.reason.get(self._error,
                                                u"unknown error code {0}".format(self._error))

    def getError(self):
        return self._error

ctypedef c_jint (__stdcall *JNI_GetDefaultJavaVMInitArgs_ptr)(void* args)
ctypedef c_jint (__stdcall *JNI_CreateJavaVM_ptr)(c_JavaVM** pvm, void** penv, void* args)
ctypedef c_jint (__stdcall *JNI_GetCreatedJavaVMs_ptr)(c_JavaVM** pvm, c_jsize size, c_jsize* nvms)

def load(dll_path, handle=None, __dlclose=dlclose):

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
        cdef c_jint result = GetDefaultJavaVMInitArgs(<void*>args)
        return result

    def JNI_CreateJavaVM(pvm, penv, args, __dll=dll):
        cdef c_JavaVM** p_pvm  # = pointer(pvm)
        cdef c_JNIEnv** p_penv # = pointer(penv)
        cdef void*      p_args # = pointer(args)
        cdef JNI_CreateJavaVM_ptr CreateJavaVM = <JNI_CreateJavaVM_ptr> \
            <long long>ct.cast(__dll.JNI_CreateJavaVM, ct.c_void_p).value
        cdef c_jint result = CreateJavaVM(p_pvm, <void**>p_penv, <void*>p_args)
        #_as_CData(pvm).c_data  = _as_CData(p_pvm[0]).c_data
        #_as_CData(penv).c_data = _as_CData(p_penv[0]).c_data
        return result

    def JNI_GetCreatedJavaVMs(pvm, size, nvms, __dll=dll):
        cdef JNI_GetCreatedJavaVMs_ptr GetCreatedJavaVMs = <JNI_GetCreatedJavaVMs_ptr> \
            <long long>ct.cast(__dll.JNI_GetCreatedJavaVMs, ct.c_void_p).value
        cdef c_jint result = <long long>GetCreatedJavaVMs#(_itself_or_NULL(pvm), size, nvms)
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
