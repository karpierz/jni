# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
import ctypes as ct
import cython

def defined(varname, __getframe=sys._getframe):
    frame = __getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

def from_oid(oid, __cast=ct.cast, __py_object=ct.py_object):
    return __cast(oid, __py_object).value if oid else None

from .jni import * ; del jni  # noqa


CFUNC = lambda *args, **kwargs: object()

__none = object()

POINTER   = lambda ctype,                __cyth=cython: __cyth.pointer(ctype)
pointer   = lambda obj,                  __cyth=cython: __cyth.address(obj)
byref     = lambda obj, offset=0,        __cyth=cython: __ffi.new(POINTER(__ffi.typeof(obj)), obj)  # !!! zamplementowac offset !!!
addressof = lambda obj,                  __cyth=cython: __cyth.address(obj)
cast      = lambda obj, ctype,           __cyth=cython: __cyth.cast(ctype, obj)
sizeof    = lambda obj_or_ctype,         __cyth=cython: __cyth.sizeof(obj_or_ctype)
# sizeof  = lambda obj_or_ctype,         __cyth=cython: __cyth.sizeof(obj_or_ctype)
py_object = lambda obj,                  __cyth=cython: __ffi.new_handle(obj)
memmove   = lambda dst, src, count,      __cyth=cython: __ffi.memmove(dst, src, count)
obj       = lambda ctype, init=__none,   __cyth=cython: (__ffi.new(__ffi.getctype(ctype)+"*", None if init is __none else init)[0]
                                                         if ctype.kind != "primitive" else
                                                         __ffi.cast(ctype, 0 if init is __none else init))
new         = lambda ctype, init=__none, __cyth=cython: __ffi.new(__ffi.getctype(ctype)+"*", None if init is __none else init)
new_array   = lambda ctype, size,        __cyth=cython: __ffi.new(__ffi.getctype(ctype)+"[]", size)
new_cstr    = lambda init,               __cyth=cython: __ffi.new("char[]", init)
as_cstr     = lambda obj,                __cyth=cython: __ffi.cast("char*", __ffi.from_buffer(obj))
to_bytes    = lambda obj, size=-1,       __cyth=cython: __ffi.string(obj, size) if size >= 0 else __ffi.string(obj)
to_unicode  = to_bytes
from_buffer = lambda data,               __cyth=cython: __ffi.from_buffer(data)

# null constant

NULL   = cython.NULL
isNULL = lambda jobj, __NULL=NULL: jobj == __NULL  # noqa: N816

#
# Decorator for defining Java native method in Python
#

def method(signature, **kwargs):
    ret_type, arg_types = __parse_signature(signature)
    fun_name = kwargs.get("name", "").encode("utf-8")
    fun_sign = signature.encode("utf-8")
    # !!!FunProto = CFUNC(ret_type, POINTER(JNIEnv), jobject, *arg_types)

    def wrapper(fun):
        native_meth = JNINativeMethod()
        native_meth.name      = fun_name or fun.__name__.encode("utf-8")
        native_meth.signature = fun_sign
        native_meth.fnPtr     = None  # !!!cast(FunProto(fun), jobject) # ct.c_void_p
        return native_meth

    return wrapper

def __parse_signature(signature):

    if signature[0] != "(":
        raise JNIException(JNI_EINVAL, info="jni.method")

    args_sig, sep, ret_sig = signature[1:].partition(")")
    if not sep or not ret_sig:
        raise JNIException(JNI_EINVAL, info="jni.method")

    sig = ret_sig + args_sig

    arg_types = []
    while sig:

        dim = 0
        while sig[dim] == "[": dim += 1
        sig = sig[dim:]

        ch = sig[0]
        if ch in "ZBCSIJFD" or (ch == "V" and dim == 0 and not arg_types):
            sig = sig[1:]
            if dim == 0:
                arg_types.append(__native_types[ch])
            elif dim == 1:
                arg_types.append(__native_array_types[ch])
            else:
                arg_types.append(jobjectArray)
        elif ch == "L":
            cname, sig = sig[1:].split(";", 1)
            if dim == 0:
                arg_types.append(__object_types.get(cname, jobject))
            else:
                arg_types.append(jobjectArray)
        else:
            raise JNIException(JNI_EINVAL, info="jni.method")

    return arg_types[0], tuple(arg_types[1:])


__native_types = {
    "V": None,
    "Z": jboolean,
    "B": jbyte,
    "C": jchar,
    "S": jshort,
    "I": jint,
    "J": jlong,
    "F": jfloat,
    "D": jdouble
}

__native_array_types = {
    "Z": jbooleanArray,
    "B": jbyteArray,
    "C": jcharArray,
    "S": jshortArray,
    "I": jintArray,
    "J": jlongArray,
    "F": jfloatArray,
    "D": jdoubleArray
}

__object_types = {
    "java/lang/String": jstring,
    "java/lang/Class":  jclass
}

del sys
del ct
del cython
