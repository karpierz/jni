# flake8-in-file-ignores: noqa: E305,E501,N813,N814,N816,W504

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ParamSpec, TypeVar, TypeAlias, Final, Generic, Any
from typing_extensions import sentinel, Buffer
from types  import GenericAlias  # noqa: F401
from collections.abc import Callable
from dataclasses import dataclass
from os import PathLike
import ctypes as ct

from .jni import ffi

__all__ = (
    "JVM", "JEnv", "load", "method", "JNIException", "Throwable",
    # Must be provided by the implementation.
    "DLL", "CFUNC",
    "POINTER", "pointer", "byref", "addressof", "sizeof", "py_object", "memmove", "cast",
    "obj", "new", "new_array", "new_cstr", "new_cwstr", "as_cstr", "as_cwstr", "to_bytes",
    "to_unicode", "from_buffer", "isNULL", "NULL",
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
)

StrPath: TypeAlias = str | PathLike[str]

if TYPE_CHECKING:
    import _cffi_backend
    CLib:  TypeAlias = _cffi_backend.Lib
    FFI:   TypeAlias = _cffi_backend.FFI
    # CType: TypeAlias = _cffi_backend.FFI.CType
    # CData: TypeAlias = _cffi_backend.FFI.CData
    P = ParamSpec("P")
    R = TypeVar("R")
    FR = TypeVar("FR")
    CFuncType: TypeAlias = Callable[[Callable[..., FR]], Callable[..., FR]]
    T = TypeVar("T", covariant=True)

    class _Pointer(Generic[T]):
        def __class_getitem__(cls, item: type) -> type: ...  # noqa: E704
        #    return POINTER(item)
        def __getitem__(self, index: int) -> T: ...  # noqa: E704
    Pointer: TypeAlias = _Pointer

# if sys.platform == "win32":
#     dlopen(name: str, flags: int = ...) -> _cffi_backend.Lib: ...
# else:
#     dlopen(name: str | None, flags: int = 0) -> _cffi_backend.Lib: ...
def DLL(name: str | None, handle: FFI.CData | None = None) -> CLib:
    assert name is not None or handle is not None
    return ffi.dlopen(name if name is not None else handle)  # type: ignore[arg-type]

#   dlclose(lib: _cffi_backend.Lib) -> None: ...
def dlclose(handle: CLib) -> None:
    return ffi.dlclose(handle)

#   callback(cdecl: str | FFI.CType) -> CFuncType[FR]: ...
def CFUNC(restype: FFI.CType | None, *argtypes: FFI.CType) -> CFuncType[FR]:
    callback_sign = ((restype.cname if restype is not None else "void") + " __stdcall"
                     + " (" + ", ".join(arg_type.cname for arg_type in argtypes) + ")")
    return ffi.callback(callback_sign)

tmap: dict[type, FFI.CType] = {}
__none = sentinel("__none")

# _CT = TypeVar("_CT", bound=_CData)
# @overload
# def POINTER(type: None, /) -> type[c_void_p]: ...
# @overload
# def POINTER(type: type[_CT], /) -> type[_Pointer[_CT]]: ...
#
# def pointer(obj: _CT, /) -> _Pointer[_CT]: ...

#   getctype(cdecl: str | FFI.CType) -> str: ...
#   typeof(cdecl: str | FFI.CData | types.BuiltinFunctionType | types.FunctionType) -> FFI.CType: ...
def POINTER(ctype: str | FFI.CType | type, __tmap: dict[type, FFI.CType] = tmap) -> FFI.CType:
    return ffi.typeof(ffi.getctype(__tmap.get(ctype, ctype)) + "*")  # type: ignore[arg-type]

#   typeof(cdecl: str | FFI.CData | types.BuiltinFunctionType | types.FunctionType) -> FFI.CType: ...
#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
def pointer(obj: str | FFI.CData) -> FFI.CData:
    return ffi.new(POINTER(ffi.typeof(obj)), obj)

#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
def byref(obj: str | FFI.CData, offset: int = 0) -> FFI.CData:
    return ffi.new(POINTER(ffi.typeof(obj)), obj)  # !!! zamiplementowac offset !!!

#   addressof(cdata: FFI.CData) -> FFI.CData: ...
def addressof(obj: FFI.CData) -> FFI.CData:
    return ffi.addressof(obj)

#   cast(cdecl: str | FFI.CType, source: FFI.CData | int) -> FFI.CData: ...
def cast(obj: FFI.CData | int, ctype: str | FFI.CType) -> FFI.CData:
    return ffi.cast(ctype, obj)

#   sizeof(cdecl: str | FFI.CData) -> int: ...
def sizeof(obj_or_ctype: str | FFI.CData) -> int:
    return ffi.sizeof(obj_or_ctype)

#   new_handle(x: Any) -> FFI.CData: ...
def py_object(obj: object) -> FFI.CData:
    return ffi.new_handle(obj)

#  memmove(dest: FFI.CData | Buffer, src: FFI.CData | Buffer, n: int) -> None: ...
def memmove(dst: FFI.CData | Buffer, src: FFI.CData | Buffer, count: int) -> None:
    return ffi.memmove(dst, src, count)

#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
#   getctype(cdecl: str | FFI.CType) -> str: ...
#   cast(cdecl: str | FFI.CType, source: FFI.CData | int) -> FFI.CData: ...
def obj(ctype: FFI.CType, init: FFI.CData | int | sentinel = __none) -> FFI.CData:
    return (ffi.new(ffi.getctype(ctype) + "*",
                    None if init is __none else init)[0]
            if ctype.kind != "primitive" else
            ffi.cast(ctype, 0 if init is __none else init))  # type: ignore[arg-type]

#   getctype(cdecl: str | FFI.CType) -> str: ...
#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
def new(ctype: str | FFI.CType, init: FFI.CData | int | sentinel = __none) -> FFI.CData:
    return ffi.new(ffi.getctype(ctype) + "*",
                   None if init is __none else init)

#   getctype(cdecl: str | FFI.CType) -> str: ...
#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
def new_array(ctype: str | FFI.CType, size: int) -> FFI.CData:
    return ffi.new(ffi.getctype(ctype) + "[]", size)

#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
def new_cstr(init: object) -> FFI.CData:
    return ffi.new("char[]", init)

#   new(cdecl: str | FFI.CType, init=None) -> FFI.CData: ...
def new_cwstr(init: object) -> FFI.CData:
    return ffi.new("wchar_t[]", init)

#   cast(cdecl: str | FFI.CType, source: FFI.CData | int) -> FFI.CData: ...
#   from_buffer(cdecl: Buffer) -> FFI.CData: ...
def as_cstr(obj: Buffer) -> FFI.CData:
    return ffi.cast("char*", ffi.from_buffer(obj))

#   cast(cdecl: str | FFI.CType, source: FFI.CData | int) -> FFI.CData: ...
#   from_buffer(cdecl: Buffer) -> FFI.CData: ...
def as_cwstr(obj: Buffer) -> FFI.CData:
    return ffi.cast("wchar_t*", ffi.from_buffer(obj))

#   string(cdata: FFI.CData, maxlen: int = -1) -> bytes | str: ...
def to_bytes(obj: FFI.CData, size: int = -1) -> bytes:
    result = ffi.string(obj, size) if size >= 0 else ffi.string(obj)
    return result.encode() if isinstance(result, str) else result

#   string(cdata:   FFI.CData, maxlen: int = -1) -> bytes | str: ...
def to_unicode(obj: FFI.CData, size: int = -1) -> str:
    result = ffi.string(obj, size) if size >= 0 else ffi.string(obj)
    return result.decode() if isinstance(result, bytes) else result

#   from_buffer(cdecl: Buffer) -> FFI.CData: ...
#   from_buffer(cdecl: str | FFI.CType, python_buffer: Buffer) -> FFI.CData: ...
def from_buffer(data: Buffer) -> FFI.CData:
    return ffi.from_buffer(data)

def isNULL(jobj: object) -> bool:
    return bool(jobj == ffi.NULL)

def itself_or_null(arg: Any) -> Any:
    return ffi.NULL if arg is None else arg

def byref_or_null(arg:  Any) -> Any:
    return ffi.NULL if arg is None else byref(arg)

class _CData(ct.Structure):
    _fields_ = (  # PyObject_HEAD
    ("ob_refcnt",     ct.c_ssize_t),
    ("ob_type",       ct.c_void_p),
    # CData body
    ("c_type",        ct.py_object),  # CTypeDescrObject*
    ("c_data",        ct.c_void_p),   # char*
    ("c_weakreflist", ct.py_object),  # PyObject*
)
__as_CData = lambda obj, __ct=ct, __CData=_CData: \
                    __ct.cast(id(obj), __ct.POINTER(__CData))[0]
del _CData

#
# JNI Types
#

# jni_md.h contains the machine-dependent typedefs for jbyte, jint
# and jlong

if TYPE_CHECKING:
    class jboolean: ...
    class jbyte: ...
    class jchar: ...
    class jshort: ...
    class jint: ...
    class jlong: ...
    class jfloat: ...
    class jdouble: ...
    class jsize: ...
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
else:
    jboolean = ffi.typeof("jboolean")
    jbyte    = ffi.typeof("jbyte")
    jchar    = ffi.typeof("jchar")
    jshort   = ffi.typeof("jshort")
    jint     = ffi.typeof("jint")
    jlong    = ffi.typeof("jlong")
    jfloat   = ffi.typeof("jfloat")
    jdouble  = ffi.typeof("jdouble")
    jsize    = ffi.typeof("jsize")

class _jobject: pass
if TYPE_CHECKING:
    jobject:    TypeAlias = Pointer[_jobject]
    jclass:     TypeAlias = jobject
    jthrowable: TypeAlias = jobject
    jstring:    TypeAlias = jobject
    CObjectType: TypeAlias = (
        type[jobject] |
        type[jclass] |
        type[jthrowable] |
        type[jstring]
    )
    jarray:        TypeAlias = jobject
    jbooleanArray: TypeAlias = jarray
    jbyteArray:    TypeAlias = jarray
    jcharArray:    TypeAlias = jarray
    jshortArray:   TypeAlias = jarray
    jintArray:     TypeAlias = jarray
    jlongArray:    TypeAlias = jarray
    jfloatArray:   TypeAlias = jarray
    jdoubleArray:  TypeAlias = jarray
    jobjectArray:  TypeAlias = jarray
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

    jweak: TypeAlias = jobject
else:
    jobject       = ffi.typeof("jobject")
    jclass        = ffi.typeof("jclass")
    jthrowable    = ffi.typeof("jthrowable")
    jstring       = ffi.typeof("jstring")
    jarray        = ffi.typeof("jarray")
    jbooleanArray = ffi.typeof("jbooleanArray")
    jbyteArray    = ffi.typeof("jbyteArray")
    jcharArray    = ffi.typeof("jcharArray")
    jshortArray   = ffi.typeof("jshortArray")
    jintArray     = ffi.typeof("jintArray")
    jlongArray    = ffi.typeof("jlongArray")
    jfloatArray   = ffi.typeof("jfloatArray")
    jdoubleArray  = ffi.typeof("jdoubleArray")
    jobjectArray  = ffi.typeof("jobjectArray")

    jweak         = ffi.typeof("jweak")

if TYPE_CHECKING:
    CType: TypeAlias = CSimpleType | CObjectType | CArrayType

NULL: FFI.CData = ffi.NULL  # null constant # added

if TYPE_CHECKING:
    class jvalue: ...

    class jfieldID: ...

    class jmethodID: ...
else:
    jvalue = ffi.typeof("jvalue")

    jfieldID = ffi.typeof("jfieldID")

    jmethodID = ffi.typeof("jmethodID")

# Return values from jobjectRefType

if TYPE_CHECKING:
    class jobjectRefType: ...
else:
    jobjectRefType = ffi.typeof("jobjectRefType")
JNIInvalidRefType:    Final[int] = jobjectRefType.relements["JNIInvalidRefType"]
JNILocalRefType:      Final[int] = jobjectRefType.relements["JNILocalRefType"]
JNIGlobalRefType:     Final[int] = jobjectRefType.relements["JNIGlobalRefType"]
JNIWeakGlobalRefType: Final[int] = jobjectRefType.relements["JNIWeakGlobalRefType"]

#
# jboolean constants
#

JNI_FALSE: Final[int] = ffi.integer_const("JNI_FALSE")
JNI_TRUE:  Final[int] = ffi.integer_const("JNI_TRUE")

#
# possible return values for JNI functions.
#

JNI_OK:        Final[int] = ffi.integer_const("JNI_OK")         # success
JNI_ERR:       Final[int] = ffi.integer_const("JNI_ERR")        # unknown error
JNI_EDETACHED: Final[int] = ffi.integer_const("JNI_EDETACHED")  # thread detached from the VM
JNI_EVERSION:  Final[int] = ffi.integer_const("JNI_EVERSION")   # JNI version error
JNI_ENOMEM:    Final[int] = ffi.integer_const("JNI_ENOMEM")     # not enough memory
JNI_EEXIST:    Final[int] = ffi.integer_const("JNI_EEXIST")     # VM already created
JNI_EINVAL:    Final[int] = ffi.integer_const("JNI_EINVAL")     # invalid arguments

#
# used in ReleaseScalarArrayElements
#

JNI_COMMIT: Final[int] = ffi.integer_const("JNI_COMMIT")
JNI_ABORT:  Final[int] = ffi.integer_const("JNI_ABORT")

#
# JNI Native Method Interface.
#

# used in RegisterNatives to describe native method name, signature,
# and function pointer.

if TYPE_CHECKING:
    class JNINativeMethod: ...
else:
    JNINativeMethod = ffi.typeof("JNINativeMethod")

@dataclass
class JNINativeInterface_:
    pass

# We use inlined functions for C++ so that programmers can write:
#
#    env->FindClass("java/lang/String")
#
# in C++ rather than:
#
#    (*env)->FindClass(env, "java/lang/String")
#
# in C.

class JNIEnv:
    __slots__ = ("functions",)

    if TYPE_CHECKING:
        functions: Any
    else:
        functions: Pointer[JNINativeInterface_]

    __itself_or_null = itself_or_null
    __byref_or_null  = byref_or_null

    def _handle_JNIException(self, err: int) -> None:
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def _handle_JavaException(self) -> Throwable:
        env = self.functions
        fun = self.functions[0]
        jthr = fun.ExceptionOccurred(env)
        fun.ExceptionClear(env)
        jexc = cast(fun.NewGlobalRef(env, jthr), jthrowable)
        fun.DeleteLocalRef(env, jthr)
        self.ExceptionClear()
        Throwable.last = thr = Throwable(jexc)  # !!!, fname)
        raise thr

    # Java version

    def GetVersion(self) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetVersion(env)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java class handling

    def DefineClass(self, name: bytes, loader: jobject, buf: Pointer[jbyte], blen: jsize | int) -> jclass:
        env = self.functions
        fun = self.functions[0]
        ret: jclass = fun.DefineClass(env, name, loader, cast(buf, "const jbyte*"), blen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FindClass(self, name: bytes) -> jclass:
        env = self.functions
        fun = self.functions[0]
        ret: jclass = fun.FindClass(env, name)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetSuperclass(self, sub: jclass) -> jclass | None:
        env = self.functions
        fun = self.functions[0]
        ret = fun.GetSuperclass(env, sub)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret if not isNULL(ret) else None

    def IsAssignableFrom(self, sub: jclass, sup: jclass) -> bool:
        env = self.functions
        fun = self.functions[0]
        return bool(fun.IsAssignableFrom(env, sub, sup))

    # Java exceptions handling

    def Throw(self, obj: jthrowable) -> None:
        env = self.functions
        fun = self.functions[0]
        ret = fun.Throw(env, obj)
        if ret != 0: self._handle_JNIException(ret)

    def ThrowNew(self, clazz: jclass, msg: bytes) -> None:
        env = self.functions
        fun = self.functions[0]
        ret = fun.ThrowNew(env, clazz, msg)
        if ret != 0: self._handle_JNIException(ret)

    def ExceptionOccurred(self) -> jthrowable | None:
        env = self.functions
        fun = self.functions[0]
        ret = fun.ExceptionOccurred(env)
        return ret if not isNULL(ret) else None

    def ExceptionDescribe(self) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ExceptionDescribe(env)

    def ExceptionClear(self) -> None:
        env = self.functions
        fun = self.functions[0]
        if Throwable.last:
            jthr = Throwable.last.getJThrowable()
            if jthr: fun.DeleteGlobalRef(env, jthr)
            Throwable.last = None
        fun.ExceptionClear(env)

    def FatalError(self, msg: bytes) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.FatalError(env, msg)

    def ExceptionCheck(self) -> bool:
        env = self.functions
        fun = self.functions[0]
        return bool(fun.ExceptionCheck(env))

    # JVM Call frame

    def PushLocalFrame(self, capacity: jint | int) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.PushLocalFrame(env, capacity)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def PopLocalFrame(self, result: jobject | None = None) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.PopLocalFrame(env, result if result is not None else NULL)
        return ret

    # Java references handling

    def NewGlobalRef(self, lobj: jobject) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.NewGlobalRef(env, lobj)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteGlobalRef(self, gref: jobject) -> None:
        env = self.functions
        fun = self.functions[0]
        if gref: fun.DeleteGlobalRef(env, gref)

    def NewLocalRef(self, ref: jobject) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.NewLocalRef(env, ref)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteLocalRef(self, obj: jobject) -> None:
        env = self.functions
        fun = self.functions[0]
        if obj: fun.DeleteLocalRef(env, obj)

    def NewWeakGlobalRef(self, obj: jobject) -> jweak:
        env = self.functions
        fun = self.functions[0]
        ret: jweak = fun.NewWeakGlobalRef(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteWeakGlobalRef(self, ref: jweak) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.DeleteWeakGlobalRef(env, ref)

    def EnsureLocalCapacity(self, capacity: jint | int) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.EnsureLocalCapacity(env, capacity)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java objects handling

    def AllocObject(self, clazz: jclass) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.AllocObject(env, clazz)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObject(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.NewObjectA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectClass(self, obj: jobject) -> jclass:
        env = self.functions
        fun = self.functions[0]
        ret: jclass = fun.GetObjectClass(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectRefType(self, obj: jobject) -> int:
        # New in JNI 1.6
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetObjectRefType(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def IsInstanceOf(self, obj: jobject, clazz: jclass) -> bool:
        env = self.functions
        fun = self.functions[0]
        return bool(fun.IsInstanceOf(env, obj, clazz))

    def IsSameObject(self, obj1: jobject, obj2: jobject) -> bool:
        env = self.functions
        fun = self.functions[0]
        return bool(fun.IsSameObject(env, obj1, obj2))

    # Call Java instance method

    def GetMethodID(self, clazz: jclass, name: bytes, sig: bytes) -> jmethodID:
        env = self.functions
        fun = self.functions[0]
        ret: jmethodID = fun.GetMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallObjectMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.CallObjectMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallBooleanMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> bool:
        env = self.functions
        fun = self.functions[0]
        ret = fun.CallBooleanMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallByteMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallByteMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallCharMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> str:
        env = self.functions
        fun = self.functions[0]
        ret: str = fun.CallCharMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallShortMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallShortMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallIntMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallIntMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallLongMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallLongMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallFloatMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.CallFloatMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallDoubleMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.CallDoubleMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallVoidMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.CallVoidMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... nonvirtually

    def CallNonvirtualObjectMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.CallNonvirtualObjectMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualBooleanMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> bool:
        env = self.functions
        fun = self.functions[0]
        ret = fun.CallNonvirtualBooleanMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallNonvirtualByteMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualByteMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualCharMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> str:
        env = self.functions
        fun = self.functions[0]
        ret: str = fun.CallNonvirtualCharMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualShortMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualShortMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualIntMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualIntMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualLongMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualLongMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualFloatMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.CallNonvirtualFloatMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualDoubleMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.CallNonvirtualDoubleMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualVoidMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.CallNonvirtualVoidMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java instance fields

    def GetFieldID(self, clazz: jclass, name: bytes, sig: bytes) -> jfieldID:
        env = self.functions
        fun = self.functions[0]
        ret: jfieldID = fun.GetFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectField(self, obj: jobject, fieldID: jfieldID) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.GetObjectField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetBooleanField(self, obj: jobject, fieldID: jfieldID) -> bool:
        env = self.functions
        fun = self.functions[0]
        ret = fun.GetBooleanField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetByteField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetByteField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharField(self, obj: jobject, fieldID: jfieldID) -> str:
        env = self.functions
        fun = self.functions[0]
        ret: str = fun.GetCharField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetShortField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetIntField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetLongField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatField(self, obj: jobject, fieldID: jfieldID) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.GetFloatField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleField(self, obj: jobject, fieldID: jfieldID) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.GetDoubleField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java instance fields

    def SetObjectField(self, obj: jobject, fieldID: jfieldID, value: jobject) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetObjectField(env, obj, fieldID, JNIEnv.__itself_or_null(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanField(self, obj: jobject, fieldID: jfieldID, value: jboolean | bool) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetBooleanField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteField(self, obj: jobject, fieldID: jfieldID, value: jbyte | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetByteField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharField(self, obj: jobject, fieldID: jfieldID, value: jchar | str) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetCharField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortField(self, obj: jobject, fieldID: jfieldID, value: jshort | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetShortField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntField(self, obj: jobject, fieldID: jfieldID, value: jint | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetIntField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongField(self, obj: jobject, fieldID: jfieldID, value: jlong | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetLongField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatField(self, obj: jobject, fieldID: jfieldID, value: jfloat | float) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetFloatField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleField(self, obj: jobject, fieldID: jfieldID, value: jdouble | float) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetDoubleField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Call Java static method

    def GetStaticMethodID(self, clazz: jclass, name: bytes, sig: bytes) -> jmethodID:
        env = self.functions
        fun = self.functions[0]
        ret: jmethodID = fun.GetStaticMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticObjectMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.CallStaticObjectMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticBooleanMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> bool:
        env = self.functions
        fun = self.functions[0]
        ret = fun.CallStaticBooleanMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallStaticByteMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallStaticByteMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticCharMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> str:
        env = self.functions
        fun = self.functions[0]
        ret: str = fun.CallStaticCharMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticShortMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallStaticShortMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticIntMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallStaticIntMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticLongMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.CallStaticLongMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticFloatMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.CallStaticFloatMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticDoubleMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.CallStaticDoubleMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticVoidMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.CallStaticVoidMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java static fields

    def GetStaticFieldID(self, clazz: jclass, name: bytes, sig: bytes) -> jfieldID:
        env = self.functions
        fun = self.functions[0]
        ret: jfieldID = fun.GetStaticFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticObjectField(self, clazz: jclass, fieldID: jfieldID) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.GetStaticObjectField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticBooleanField(self, clazz: jclass, fieldID: jfieldID) -> bool:
        env = self.functions
        fun = self.functions[0]
        ret = fun.GetStaticBooleanField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetStaticByteField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStaticByteField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticCharField(self, clazz: jclass, fieldID: jfieldID) -> str:
        env = self.functions
        fun = self.functions[0]
        ret: str = fun.GetStaticCharField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticShortField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStaticShortField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticIntField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStaticIntField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticLongField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStaticLongField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticFloatField(self, clazz: jclass, fieldID: jfieldID) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.GetStaticFloatField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticDoubleField(self, clazz: jclass, fieldID: jfieldID) -> float:
        env = self.functions
        fun = self.functions[0]
        ret: float = fun.GetStaticDoubleField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java static fields

    def SetStaticObjectField(self, clazz: jclass, fieldID: jfieldID, value: jobject) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticObjectField(env, clazz, fieldID, JNIEnv.__itself_or_null(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticBooleanField(self, clazz: jclass, fieldID: jfieldID, value: jboolean | bool) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticBooleanField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticByteField(self, clazz: jclass, fieldID: jfieldID, value: jbyte | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticByteField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticCharField(self, clazz: jclass, fieldID: jfieldID, value: jchar | str) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticCharField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticShortField(self, clazz: jclass, fieldID: jfieldID, value: jshort | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticShortField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticIntField(self, clazz: jclass, fieldID: jfieldID, value: jint | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticIntField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticLongField(self, clazz: jclass, fieldID: jfieldID, value: jlong | int) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticLongField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticFloatField(self, clazz: jclass, fieldID: jfieldID, value: jfloat | float) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticFloatField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticDoubleField(self, clazz: jclass, fieldID: jfieldID, value: jdouble | float) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetStaticDoubleField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java strings handling

    def NewString(self, unicode: str, slen: jsize | int) -> jstring:
        env = self.functions
        fun = self.functions[0]
        ret: jstring = fun.NewString(env, unicode, slen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringLength(self, str: jstring) -> int:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStringLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringChars(self, str: jstring, isCopy: Pointer[jboolean] | None = None) -> Pointer[jchar]:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetStringChars(env, str, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringChars(self, str: jstring, chars: Pointer[jchar]) -> None:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseStringChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewStringUTF(self, utf: bytes) -> jstring:
        env = self.functions
        fun = self.functions[0]
        ret: jstring = fun.NewStringUTF(env, utf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFLength(self, str: jstring) -> int:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStringUTFLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFLengthAsLong(self, str: jstring) -> int:  # noqa: A002
        # Since: JDK/JRE 24.0
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetStringUTFLengthAsLong(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFChars(self, str: jstring, isCopy: Pointer[jboolean] | None = None) -> Pointer[ct.c_char]:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[ct.c_char] = fun.GetStringUTFChars(env, str, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringUTFChars(self, str: jstring, chars: Pointer[ct.c_char]) -> None:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseStringUTFChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringRegion(self, str: jstring, start: jsize | int, len: jsize | int, buf: Pointer[jchar]) -> None:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        fun.GetStringRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringUTFRegion(self, str: jstring, start: jsize | int, len: jsize | int, buf: Pointer[ct.c_char]) -> None:  # noqa: A002
        env = self.functions
        fun = self.functions[0]
        fun.GetStringUTFRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetStringCritical(self, string: jstring, isCopy: Pointer[jboolean] | None = None) -> Pointer[jchar]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetStringCritical(env, string, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringCritical(self, string: jstring, cstring: Pointer[jchar]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseStringCritical(env, string, cstring)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java arrays handling

    def GetArrayLength(self, array: jarray) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetArrayLength(env, array)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObjectArray(self, size: jsize | int, clazz: jclass, init: jobject | None = None) -> jobjectArray:
        env = self.functions
        fun = self.functions[0]
        ret: jobjectArray = fun.NewObjectArray(env, size, clazz, JNIEnv.__itself_or_null(init))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectArrayElement(self, array: jobjectArray, index: jsize | int) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.GetObjectArrayElement(env, array, index)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def SetObjectArrayElement(self, array: jobjectArray, index: jsize | int, value: jobject) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetObjectArrayElement(env, array, index, JNIEnv.__itself_or_null(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewBooleanArray(self, size: jsize | int) -> jbooleanArray:
        env = self.functions
        fun = self.functions[0]
        ret: jbooleanArray = fun.NewBooleanArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewByteArray(self, size: jsize | int) -> jbyteArray:
        env = self.functions
        fun = self.functions[0]
        ret: jbyteArray = fun.NewByteArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewCharArray(self, size: jsize | int) -> jcharArray:
        env = self.functions
        fun = self.functions[0]
        ret: jcharArray = fun.NewCharArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewShortArray(self, size: jsize | int) -> jshortArray:
        env = self.functions
        fun = self.functions[0]
        ret: jshortArray = fun.NewShortArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewIntArray(self, size: jsize | int) -> jintArray:
        env = self.functions
        fun = self.functions[0]
        ret: jintArray = fun.NewIntArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewLongArray(self, size: jsize | int) -> jlongArray:
        env = self.functions
        fun = self.functions[0]
        ret: jlongArray = fun.NewLongArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewFloatArray(self, size: jsize | int) -> jfloatArray:
        env = self.functions
        fun = self.functions[0]
        ret: jfloatArray = fun.NewFloatArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewDoubleArray(self, size: jsize | int) -> jdoubleArray:
        env = self.functions
        fun = self.functions[0]
        ret: jdoubleArray = fun.NewDoubleArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetBooleanArrayElements(self, array: jbooleanArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jboolean]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jboolean] = fun.GetBooleanArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetByteArrayElements(self, array: jbyteArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jbyte]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jbyte] = fun.GetByteArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharArrayElements(self, array: jcharArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jchar]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetCharArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortArrayElements(self, array: jshortArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jshort]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jshort] = fun.GetShortArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntArrayElements(self, array: jintArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jint]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jint] = fun.GetIntArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongArrayElements(self, array: jlongArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jlong]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jlong] = fun.GetLongArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatArrayElements(self, array: jfloatArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jfloat]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jfloat] = fun.GetFloatArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleArrayElements(self, array: jdoubleArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jdouble]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[jdouble] = fun.GetDoubleArrayElements(env, array, JNIEnv.__itself_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseBooleanArrayElements(self, array: jbooleanArray, elems: Pointer[jboolean], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseBooleanArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseByteArrayElements(self, array: jbyteArray, elems: Pointer[jbyte], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseByteArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseCharArrayElements(self, array: jcharArray, elems: Pointer[jchar], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseCharArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseShortArrayElements(self, array: jshortArray, elems: Pointer[jshort], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseShortArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseIntArrayElements(self, array: jintArray, elems: Pointer[jint], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseIntArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseLongArrayElements(self, array: jlongArray, elems: Pointer[jlong], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseLongArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseFloatArrayElements(self, array: jfloatArray, elems: Pointer[jfloat], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseFloatArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseDoubleArrayElements(self, array: jdoubleArray, elems: Pointer[jdouble], mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleaseDoubleArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetBooleanArrayRegion(self, array: jbooleanArray, start: jint | int, size: jint | int, buf: Pointer[jboolean]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetByteArrayRegion(self, array: jbyteArray, start: jint | int, size: jint | int, buf: Pointer[jbyte]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetCharArrayRegion(self, array: jcharArray, start: jint | int, size: jint | int, buf: Pointer[jchar]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetShortArrayRegion(self, array: jshortArray, start: jint | int, size: jint | int, buf: Pointer[jshort]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetIntArrayRegion(self, array: jintArray, start: jint | int, size: jint | int, buf: Pointer[jint]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetLongArrayRegion(self, array: jlongArray, start: jint | int, size: jint | int, buf: Pointer[jlong]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetFloatArrayRegion(self, array: jfloatArray, start: jint | int, size: jint | int, buf: Pointer[jfloat]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetDoubleArrayRegion(self, array: jdoubleArray, start: jint | int, size: jint | int, buf: Pointer[jdouble]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.GetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanArrayRegion(self, array: jbooleanArray, start: jint | int, size: jint | int, buf: Pointer[jboolean]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteArrayRegion(self, array: jbyteArray, start: jint | int, size: jint | int, buf: Pointer[jbyte]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharArrayRegion(self, array: jcharArray, start: jint | int, size: jint | int, buf: Pointer[jchar]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortArrayRegion(self, array: jshortArray, start: jint | int, size: jint | int, buf: Pointer[jshort]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntArrayRegion(self, array: jintArray, start: jint | int, size: jint | int, buf: Pointer[jint]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongArrayRegion(self, array: jlongArray, start: jint | int, size: jint | int, buf: Pointer[jlong]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatArrayRegion(self, array: jfloatArray, start: jint | int, size: jint | int, buf: Pointer[jfloat]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleArrayRegion(self, array: jdoubleArray, start: jint | int, size: jint | int, buf: Pointer[jdouble]) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.SetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetPrimitiveArrayCritical(self, array: jarray, isCopy: Pointer[jboolean] | None = None) -> ct.c_void_p:
        env = self.functions
        fun = self.functions[0]
        ret = fun.GetPrimitiveArrayCritical(env, array, JNIEnv.__byref_or_null(isCopy))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ct.c_void_p(ret)

    def ReleasePrimitiveArrayCritical(self, array: jarray, carray: ct.c_void_p, mode: jint | int = 0) -> None:
        env = self.functions
        fun = self.functions[0]
        fun.ReleasePrimitiveArrayCritical(env, array, carray, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java native methods handling

    def RegisterNatives(self, clazz: jclass, methods: Pointer[JNINativeMethod], nMethods: jint | int) -> int:
        env = self.functions
        fun = self.functions[0]
        # Required due to bug in jvm:
        # https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6493522
        fun.GetMethodID(env, clazz, b"notify", b"()V")
        ret: int = 0  # fun.RegisterNatives(env, clazz, methods, nMethods)
        # print("RegisterNatives:ret:", ret)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def UnregisterNatives(self, clazz: jclass) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.UnregisterNatives(env, clazz)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java object monitoring

    def MonitorEnter(self, obj: jobject) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.MonitorEnter(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def MonitorExit(self, obj: jobject) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.MonitorExit(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java direct buffer handling

    def NewDirectByteBuffer(self, address: Pointer[ct.c_char], capacity: jlong | int) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.NewDirectByteBuffer(env, from_buffer(address), capacity)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferAddress(self, buf: jobject) -> Pointer[ct.c_char]:
        env = self.functions
        fun = self.functions[0]
        ret: Pointer[ct.c_char] = fun.GetDirectBufferAddress(env, buf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferCapacity(self, buf: jobject) -> int:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetDirectBufferCapacity(env, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java reflection support

    def FromReflectedMethod(self, method: jobject) -> jmethodID:
        env = self.functions
        fun = self.functions[0]
        ret: jmethodID = fun.FromReflectedMethod(env, method)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FromReflectedField(self, field: jobject) -> jfieldID:
        env = self.functions
        fun = self.functions[0]
        ret: jfieldID = fun.FromReflectedField(env, field)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedMethod(self, cls: jclass, methodID: jmethodID, isStatic: jboolean | bool) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.ToReflectedMethod(env, cls, methodID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedField(self, cls: jclass, fieldID: jfieldID, isStatic: jboolean | bool) -> jobject:
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.ToReflectedField(env, cls, fieldID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java VM Interface

    def GetJavaVM(self, vm: Pointer[Pointer[JavaVM]]) -> None:
        env = self.functions
        fun = self.functions[0]
        ret: int = fun.GetJavaVM(env, vm)
        if ret != 0: self._handle_JNIException(ret)

    # Module Features

    def GetModule(self, clazz: jclass) -> jobject:
        # Since: JDK/JRE 9.0
        env = self.functions
        fun = self.functions[0]
        ret: jobject = fun.GetModule(env, clazz)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Virtual threads

    def IsVirtualThread(self, obj: jobject) -> bool:
        # Since: JDK/JRE 19.0
        env = self.functions
        fun = self.functions[0]
        ret = fun.IsVirtualThread(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

tmap[JNIEnv] = ffi.typeof("JNIEnv")

def JEnv(penv: Pointer[JNIEnv]) -> JNIEnv:
    env: JNIEnv = JNIEnv()
    env.functions = penv
    return env

#
# JNI Invocation Interface.
#

@dataclass
class JNIInvokeInterface_:
    pass

class JavaVM:
    __slots__ = ("functions",)

    if TYPE_CHECKING:
        functions: Any
    else:
        functions: Pointer[JNIInvokeInterface_]

    __itself_or_null = itself_or_null
    __as_cdata = globals()["__as_CData"]

    def _handle_JNIException(self, err: int) -> None:
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def DestroyJavaVM(self) -> None:
        jvm = self.functions
        fun = self.functions[0]
        ret = fun.DestroyJavaVM(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThread(self, penv: Pointer[Pointer[JNIEnv]], args: Pointer[JavaVMAttachArgs] | None = None) -> None:
        jvm = self.functions
        fun = self.functions[0]
        p_penv = pointer(penv)
        ret = fun.AttachCurrentThread(jvm, cast(p_penv, "void**"), JavaVM.__itself_or_null(args))
        if ret != JNI_OK: self._handle_JNIException(ret)
        JavaVM.__as_cdata(penv).c_data = JavaVM.__as_cdata(p_penv[0]).c_data

    def AttachCurrentThreadAsDaemon(self, penv: Pointer[Pointer[JNIEnv]], args: Pointer[JavaVMAttachArgs] | None = None) -> None:
        jvm = self.functions
        fun = self.functions[0]
        p_penv = pointer(penv)
        ret = fun.AttachCurrentThreadAsDaemon(jvm, cast(p_penv, "void**"), JavaVM.__itself_or_null(args))
        if ret != JNI_OK: self._handle_JNIException(ret)
        JavaVM.__as_cdata(penv).c_data = JavaVM.__as_cdata(p_penv[0]).c_data

    def DetachCurrentThread(self) -> None:
        jvm = self.functions
        fun = self.functions[0]
        ret = fun.DetachCurrentThread(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def GetEnv(self, penv: Pointer[Pointer[JNIEnv]], version: jint | int) -> None:
        jvm = self.functions
        fun = self.functions[0]
        p_penv = pointer(penv)
        ret = fun.GetEnv(jvm, cast(p_penv, "void**"), version)
        if ret != JNI_OK: self._handle_JNIException(ret)
        JavaVM.__as_cdata(penv).c_data = JavaVM.__as_cdata(p_penv[0]).c_data

tmap[JavaVM] = ffi.typeof("JavaVM")

def JVM(pjvm: Pointer[JavaVM]) -> JavaVM:
    jvm: JavaVM = JavaVM()
    jvm.functions = pjvm
    return jvm


# optionString may be any option accepted by the JVM, or one of the
# following:
#
# -D<name>=<value>          Set a system property.
# -verbose[:class|gc|jni]   Enable verbose output, comma-separated. E.g.
#                           "-verbose:class" or "-verbose:gc,class"
#                           Standard names include: gc, class, and jni.
#                           All nonstandard (VM-specific) names must begin
#                           with "X".
# vfprintf                  extraInfo is a pointer to the vfprintf hook.
# exit                      extraInfo is a pointer to the exit hook.
# abort                     extraInfo is a pointer to the abort hook.
#
if TYPE_CHECKING:
    class JavaVMOption: ...

    class JavaVMInitArgs: ...

    class JavaVMAttachArgs: ...
else:
    JavaVMOption = ffi.typeof("JavaVMOption")

    JavaVMInitArgs = ffi.typeof("JavaVMInitArgs")

    JavaVMAttachArgs = ffi.typeof("JavaVMAttachArgs")

# These will be VM-specific.

JDK1_2: Final[int] = ffi.integer_const("JDK1_2")
JDK1_4: Final[int] = ffi.integer_const("JDK1_4")

# End VM-specific.

# JNI version constants

JNI_VERSION_1_1: Final[int] = ffi.integer_const("JNI_VERSION_1_1")
JNI_VERSION_1_2: Final[int] = ffi.integer_const("JNI_VERSION_1_2")
JNI_VERSION_1_4: Final[int] = ffi.integer_const("JNI_VERSION_1_4")
JNI_VERSION_1_6: Final[int] = ffi.integer_const("JNI_VERSION_1_6")
JNI_VERSION_1_8: Final[int] = ffi.integer_const("JNI_VERSION_1_8")
JNI_VERSION_9:   Final[int] = ffi.integer_const("JNI_VERSION_9")
JNI_VERSION_10:  Final[int] = ffi.integer_const("JNI_VERSION_10")
JNI_VERSION_19:  Final[int] = ffi.integer_const("JNI_VERSION_19")
JNI_VERSION_20:  Final[int] = ffi.integer_const("JNI_VERSION_20")
JNI_VERSION_21:  Final[int] = ffi.integer_const("JNI_VERSION_21")
JNI_VERSION_24:  Final[int] = ffi.integer_const("JNI_VERSION_24")

# eof jni.h

class Throwable(Exception):  # noqa: N818

    last: Throwable | None = None

    def __init__(self, jthr: jthrowable | None = None, info: jstring | None = None) -> None:
        """Initializer"""
        self._jthr: jthrowable = cast(jthr if jthr is not None else NULL, jthrowable)
        self._info: jstring    = cast(info if info is not None else NULL, jstring)
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

def load(dll_path: StrPath | None = None, *, handle=None,  # type: ignore[no-untyped-def]
         __dlclose=dlclose, __itself_or_null=itself_or_null, __as_cdata=__as_CData) -> type:

    import os
    try:
        dll = DLL(os.fspath(dll_path) if dll_path is not None else None, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError(f"{exc}") from None

    dllclose = classmethod(lambda cls, __dlclose=__dlclose: __dlclose(cls.dll))

    def JNI_GetDefaultJavaVMInitArgs(args: Pointer[JavaVMInitArgs],
                                     __dll: CLib = dll) -> jint:
        result: jint = __dll.JNI_GetDefaultJavaVMInitArgs(  # type: ignore[attr-defined]
                                                          cast(args, "void*"))
        return result

    def JNI_CreateJavaVM(pvm: Pointer[Pointer[JavaVM]], penv: Pointer[Pointer[JNIEnv]],
                         args: Pointer[JavaVMInitArgs], __dll: CLib = dll) -> jint:
        p_pvm  = pointer(pvm)
        p_penv = pointer(penv)
        p_args = pointer(args)
        result: jint = __dll.JNI_CreateJavaVM(p_pvm,  # type: ignore[attr-defined]
                                              cast(p_penv, "void**"),
                                              cast(p_args, "void*"))
        __as_cdata(pvm).c_data  = __as_cdata(p_pvm[0]).c_data
        __as_cdata(penv).c_data = __as_cdata(p_penv[0]).c_data
        return result

    def JNI_GetCreatedJavaVMs(pvm: Pointer[Pointer[JavaVM]], size: jsize, nvms: Pointer[jsize],
                              __dll: CLib = dll) -> jint:
        result: jint = __dll.JNI_GetCreatedJavaVMs(  # type: ignore[attr-defined]
                                                   __itself_or_null(pvm),
                                                   size, nvms)
        return result

    JNI = type("JNI", (), dict(dll=dll, dllclose=dllclose,
               GetDefaultJavaVMInitArgs = JNI_GetDefaultJavaVMInitArgs,
               CreateJavaVM = JNI_CreateJavaVM,
               GetCreatedJavaVMs = JNI_GetCreatedJavaVMs,))

    return JNI

#
# Decorator for defining Java native method in Python
#

def method(signature: str, *,
           name: str | None = None) -> Callable[[Callable[P, R]], JNINativeMethod]:
    arg_types, res_type = __parse_signature(signature)
    fun_name = name.encode() if name is not None else None
    fun_sign = signature.encode()
    FunProto = CFUNC(res_type, POINTER(JNIEnv), jobject, *arg_types)

    def wrapper(fun: Callable[P, R],
                __fun_name:  Any = None,
                __fun_sign:  Any = None,
                __fun_proto: Any = None) -> JNINativeMethod:
        __fun_name  = new_cstr(fun_name or fun.__name__.encode())
        __fun_sign  = new_cstr(fun_sign)
        __fun_proto = cast(FunProto(fun), "void*")
        native_meth = new(JNINativeMethod)[0]
        native_meth.name      = __fun_name
        native_meth.signature = __fun_sign
        native_meth.fnPtr     = __fun_proto
        return native_meth

    return wrapper

def __parse_signature(signature: str) -> tuple[tuple[CType, ...], CType | None]:

    if signature[0] != "(":
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

if TYPE_CHECKING:
    POINTER: TypeAlias = Pointer  # type: ignore[no-redef] # noqa: F811

del __as_CData
del itself_or_null
del byref_or_null
del tmap
del dlclose
