# flake8-in-file-ignores: noqa: E305,E402,E501,E704,N813,N814,N816,W504,    F405

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ParamSpec, TypeVar, TypeAlias, Final  # noqa: F401
from typing_extensions import sentinel
from types  import GenericAlias  # noqa: F401
from collections.abc import Callable
from os import PathLike
import ctypes as ct

from utlx import platform as _platform

__all__ = (
    "JVM", "JEnv", "load", "method", "JNIException", "Throwable",
    # Must be provided by the implementation.
    "DLL", "CFUNC",
    "POINTER", "pointer", "byref", "addressof", "sizeof", "py_object", "memmove", "cast",
    "new", "new_array", "new_cstr", "new_cwstr", "as_cstr", "as_cwstr",
    "to_bytes", "to_unicode", "from_buffer", "is_NULL", "NULL",
    # JNI interface
    "JavaVM", "JNIEnv",
    "jboolean", "jbyte", "jchar", "jshort", "jint", "jlong", "jfloat", "jdouble", "jsize",
    "jobject", "jclass", "jthrowable", "jstring", "jarray", "jbooleanArray", "jbyteArray",
    "jcharArray", "jshortArray", "jintArray", "jlongArray", "jfloatArray", "jdoubleArray",
    "jobjectArray", "jweak", "jvalue", "jfieldID", "jmethodID", "jobjectRefType",
    "JNIInvalidRefType", "JNILocalRefType", "JNIGlobalRefType", "JNIWeakGlobalRefType",
    "JNINativeMethod", "JavaVMOption", "JavaVMInitArgs", "JavaVMAttachArgs",
    "JNI_TRUE", "JNI_FALSE",
    "JNI_COMMIT", "JNI_ABORT",
    "JNI_OK", "JNI_ERR", "JNI_EDETACHED", "JNI_EVERSION", "JNI_ENOMEM", "JNI_EEXIST", "JNI_EINVAL",
    "JDK1_2", "JDK1_4",
    "JNI_VERSION_1_1", "JNI_VERSION_1_2", "JNI_VERSION_1_4", "JNI_VERSION_1_6", "JNI_VERSION_1_8",
    "JNI_VERSION_9",   "JNI_VERSION_10",  "JNI_VERSION_19",  "JNI_VERSION_20",  "JNI_VERSION_21",
    "JNI_VERSION_24",
    "obj",  # for backward compatibility
)
def __dir__() -> list[str]: return list(__all__)  # pragma: no cover

StrPath: TypeAlias = str | PathLike[str]

if TYPE_CHECKING:
    CType: TypeAlias = type
    P = ParamSpec("P")
    R = TypeVar("R")

def DLL(name, handle: int | None = None):
    raise NotImplementedError("Not implemented yet!")
if _platform.is_windows:
    try:
        from _ctypes import FreeLibrary as dlclose
    except ImportError:  # pragma: no cover
        def dlclose(handle: int, /) -> None:
            return
else:
    from _ctypes import dlclose as dlclose  # type: ignore[attr-defined, no-redef]

def CFUNC(restype, *argtypes):
    callback_sign = ((restype.cname if restype is not None else "void") + " __stdcall"
                     + " (" + ", ".join(arg_type.cname for arg_type in argtypes) + ")")
    return __ffi.callback(callback_sign)

__none = sentinel("__none")

def POINTER(ctype):
    raise NotImplementedError("Not implemented yet!")

def pointer(obj):
    raise NotImplementedError("Not implemented yet!")

def byref(obj, offset=0):
    raise NotImplementedError("Not implemented yet!")

def addressof(obj):
    raise NotImplementedError("Not implemented yet!")

def cast(obj, ctype):
    raise NotImplementedError("Not implemented yet!")

def sizeof(obj_or_ctype):
    raise NotImplementedError("Not implemented yet!")

def py_object(obj):
    raise NotImplementedError("Not implemented yet!")

def memmove(dst, src, count):
    raise NotImplementedError("Not implemented yet!")

def new(ctype, init=__none):
    raise NotImplementedError("Not implemented yet!")
obj = new  # for backward compatibility

def new_array(ctype, size):
    raise NotImplementedError("Not implemented yet!")

def new_cstr(init):
    raise NotImplementedError("Not implemented yet!")

def new_cwstr(init):
    raise NotImplementedError("Not implemented yet!")

def as_cstr(obj):
    raise NotImplementedError("Not implemented yet!")

def as_cwstr(obj):
    raise NotImplementedError("Not implemented yet!")

def to_bytes(obj, size=-1):
    raise NotImplementedError("Not implemented yet!")

def to_unicode(obj, size=-1):
    raise NotImplementedError("Not implemented yet!")

def from_buffer(data):
    raise NotImplementedError("Not implemented yet!")

def is_NULL(jobj):
    raise NotImplementedError("Not implemented yet!")

NULL = ct.c_void_p(0)  # jobject # null constant

itself_or_null = lambda arg: arg
byref_or_null  = lambda arg: arg

#
# JNI Types
#

from .jni import * ; del jni  # type: ignore[import-not-found] # noqa: F403,F821

CSimpleType: TypeAlias = (
    type[jboolean] |
    type[jbyte] |
    type[jchar] |
    type[jshort] |
    type[jint] |
    type[jlong] |
    type[jfloat] |
    type[jdouble]
)

CObjectType: TypeAlias = (
    type[jobject] |
    type[jclass] |
    type[jthrowable] |
    type[jstring]
)

CArrayType: TypeAlias = (
    type[jarray] |
    type[jbooleanArray] |
    type[jbyteArray] |
    type[jcharArray] |
    type[jshortArray] |
    type[jintArray] |
    type[jlongArray] |
    type[jfloatArray] |
    type[jdoubleArray] |
    type[jobjectArray]
)

CType: TypeAlias = CSimpleType | CObjectType | CArrayType

# ...

def JEnv(penv):
    raise NotImplementedError("Not implemented yet!")

def JVM(pjvm):
    raise NotImplementedError("Not implemented yet!")

# ...

# eof jni.h

class Throwable(Exception):  # noqa: N818

    last: Throwable | None = None

    def __init__(self, jthr: jthrowable | None = None, info: jstring | None = None) -> None:
        """Initializer"""
        self._jthr: jthrowable = cast(jthr, jthrowable) if jthr is not None else NULL
        self._info: jstring    = cast(info, jstring)    if info is not None else NULL
        super().__init__(self._jthr, self._info)

    def getJThrowable(self) -> jthrowable:
        return self._jthr

    def getInfo(self) -> jstring:
        return self._info

class JNIException(SystemError):

    reason: dict[int, str] = {
        JNI_OK:        "success",
        JNI_ERR:       "unknown error",
        JNI_EDETACHED: "thread detached from the VM",
        JNI_EVERSION:  "JNI version error",
        JNI_ENOMEM:    "not enough memory",
        JNI_EEXIST:    "VM already created",
        JNI_EINVAL:    "invalid arguments",
    }

    def __init__(self, error: int = JNI_ERR, info: str | None = None) -> None:
        """Initializer"""
        self._error = error
        self._info  = info
        super().__init__(self.getMessage(), self.getError())

    def getMessage(self) -> str:
        prefix = self._info + ": " if self._info else ""
        return prefix + JNIException.reason.get(self._error,
                                                f"unknown error code {self._error}")

    def getError(self) -> int:
        return self._error

def load(dll_path: StrPath | None = None, *, handle: int | None = None,
         __dlclose: Callable[[int], None] = dlclose) -> type:

    raise NotImplementedError("Not implemented yet!")

    import os
    try:
        dll = DLL(os.fspath(dll_path) if dll_path is not None else None, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError(f"{exc}") from None

    def proto(restype: type | None, func: Callable[P, R], *argtypes: type | None) -> Callable[P, R]:
        func.restype  = restype   # type: ignore[attr-defined]
        func.argtypes = argtypes  # type: ignore[attr-defined]
        return func

    JNI = type("JNI", (), dict(dll=dll, dllclose=classmethod(lambda cls, __dlclose=__dlclose: __dlclose(cls.dll._handle))))
    JNI.GetDefaultJavaVMInitArgs = proto(jint, dll.JNI_GetDefaultJavaVMInitArgs, POINTER(JavaVMInitArgs))
    JNI.CreateJavaVM             = proto(jint, dll.JNI_CreateJavaVM,             POINTER(POINTER(JavaVM)), POINTER(POINTER(JNIEnv)), POINTER(JavaVMInitArgs))
    JNI.GetCreatedJavaVMs        = proto(jint, dll.JNI_GetCreatedJavaVMs,        POINTER(POINTER(JavaVM)), jsize, POINTER(jsize))

    return JNI

#
# Decorator for defining Java native method in Python
#

def method(signature: str, *,
           name: str | None = None) -> Callable[[Callable[P, R]], JNINativeMethod]:
    arg_types, res_type = __parse_signature(signature)
    fun_name = kwargs.get("name", "").encode()
    fun_sign = signature.encode()
    # !!!FunProto = CFUNC(res_type, POINTER(JNIEnv), jobject, *arg_types)

    def wrapper(fun: Callable[P, R]):
        native_meth = JNINativeMethod()
        native_meth.name      = fun_name or fun.__name__.encode()
        native_meth.signature = fun_sign
        native_meth.fnPtr     = None  # !!!cast(FunProto(fun), jobject) # ct.c_void_p
        return native_meth

    return wrapper

def __parse_signature(signature: str) -> tuple[tuple[CType, ...], CType | None]:

    if signature == "" or signature[0] != "(":
        raise JNIException(JNI_EINVAL, info="jni.method")

    args_sig, sep, ret_sig = signature[1:].partition(")")
    if not sep or not ret_sig:
        raise JNIException(JNI_EINVAL, info="jni.method")

    sig = ret_sig + args_sig

    jarg_types: list[CType | None] = []
    while sig:

        dim = 0
        while sig[dim] == "[": dim += 1
        sig = sig[dim:]

        ch = sig[0]
        if ch == "V" and dim == 0 and not jarg_types:
            sig = sig[1:]
            jarg_types.append(__native_simple_types[ch])
        elif ch in "ZBCSIJFD":
            sig = sig[1:]
            if dim == 0:
                jarg_types.append(__native_simple_types[ch])
            elif dim == 1:
                jarg_types.append(__native_array_types[ch])
            else:
                jarg_types.append(jobjectArray)
        elif ch == "L":
            cname, sig = sig[1:].split(";", 1)
            if dim == 0:
                jarg_types.append(__object_types.get(cname, jobject))
            else:
                jarg_types.append(jobjectArray)
        else:
            raise JNIException(JNI_EINVAL, info="jni.method")

    arg_types: list[CType]  = jarg_types[1:]  # type: ignore[assignment]
    res_type:  CType | None = jarg_types[0]
    return tuple(arg_types), res_type

__native_simple_types: Final[dict[str, CSimpleType | None]] = {
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

__native_array_types: Final[dict[str, CArrayType]] = {
    "Z": jbooleanArray,
    "B": jbyteArray,
    "C": jcharArray,
    "S": jshortArray,
    "I": jintArray,
    "J": jlongArray,
    "F": jfloatArray,
    "D": jdoubleArray
}

__object_types: Final[dict[str, CObjectType]] = {
    "java/lang/String": jstring,
    "java/lang/Class":  jclass
}

del itself_or_null
del byref_or_null
del dlclose
del _platform
