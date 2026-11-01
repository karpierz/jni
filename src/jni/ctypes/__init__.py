# flake8-in-file-ignores: noqa: A005,E305,E402,E501,N813,N814,N816,W504

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ParamSpec, TypeVar, TypeAlias, Final
from typing_extensions import sentinel, Buffer
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
    from ctypes import _CData
    CData = TypeVar("CData", bound=_CData)
    P = ParamSpec("P")
    R = TypeVar("R")
    Pointer: TypeAlias = ct._Pointer
    Addr: TypeAlias = Pointer[CData] | ct.Array[CData] | int | bytes

DLL: type
if _platform.is_windows:
    from ctypes import WinDLL as DLL
    try:
        from _ctypes import FreeLibrary as dlclose
    except ImportError:  # pragma: no cover
        def dlclose(handle: int, /) -> None:
            return
    from ctypes import WINFUNCTYPE as CFUNC
else:  # pragma: no cover
    from ctypes  import CDLL      as DLL
    from _ctypes import dlclose   as dlclose  # type: ignore[attr-defined, no-redef]
    from ctypes  import CFUNCTYPE as CFUNC

__none = sentinel("__none")

from ctypes import POINTER
from ctypes import pointer
from ctypes import byref      # noqa: F401
from ctypes import addressof  # noqa: F401
from ctypes import sizeof     # noqa: F401
from ctypes import py_object  # noqa: F401
from ctypes import memmove    # noqa: F401
from ctypes import cast

def obj(ctype: type[CData], init: object = __none) -> CData:
    return ctype() if init is __none else ctype(init)  # type: ignore[call-arg]

def new(ctype: type[CData], init: object = __none) -> Pointer[CData]:
    return ct.pointer(ctype() if init is __none else ctype(init))  # type: ignore[call-arg]

def new_array(ctype: type[CData], size: int) -> ct.Array[CData]:
    arr: ct.Array[CData] = (ctype * size)()  # type: ignore[operator]
    return arr

def new_cstr(init: int | bytes) -> ct.c_char_p:
    return ct.cast(ct.create_string_buffer(init), ct.c_char_p)

def new_cwstr(init: int | str) -> ct.c_wchar_p:
    return ct.cast(ct.create_unicode_buffer(init), ct.c_wchar_p)

def as_cstr(obj: int | bytes | None) -> ct.c_char_p:
    return ct.c_char_p(obj)

def as_cwstr(obj: int | str | None) -> ct.c_wchar_p:
    return ct.c_wchar_p(obj)

def to_bytes(obj: Addr[CData], size: int = -1) -> bytes:
    return ct.string_at(obj, size=size)

def to_unicode(obj: Addr[CData], size: int = -1) -> str:
    return ct.wstring_at(obj, size=size)

def from_buffer(data: Buffer) -> Pointer[ct.c_char]:
    return ct.cast((ct.c_char * 0).from_buffer(data), ct.POINTER(ct.c_char))

def isNULL(jobj: object) -> bool:
    return not bool(jobj)

#
# JNI Types
#

# jni_md.h contains the machine-dependent typedefs for jbyte, jint
# and jlong

jboolean: TypeAlias = ct.c_ubyte
jbyte:    TypeAlias = ct.c_int8
jchar:    TypeAlias = ct.c_wchar
jshort:   TypeAlias = ct.c_int16
jint:     TypeAlias = ct.c_int32
jlong:    TypeAlias = ct.c_int64
jfloat:   TypeAlias = ct.c_float
jdouble:  TypeAlias = ct.c_double
jsize:    TypeAlias = jint
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

# class _jobject(ct.Structure): pass
# if TYPE_CHECKING:
#     jobject: TypeAlias = Pointer[_jobject]
# else:
#     jobject = POINTER(_jobject)
jobject:    TypeAlias = ct.c_void_p
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

CType: TypeAlias = CSimpleType | CObjectType | CArrayType

NULL: jobject = jobject()  # null constant # added
# NULL: ct.c_void_p = ct.c_void_p(0)  # null constant # added

class jvalue(ct.Union):
    _fields_ = [
    ("z", jboolean),
    ("b", jbyte),
    ("c", jchar),
    ("s", jshort),
    ("i", jint),
    ("j", jlong),
    ("f", jfloat),
    ("d", jdouble),
    ("l", jobject),
]

if _platform.is_ironpython:  # pragma: no cover
    _jvalue = jvalue

    class jvalue(ct.Structure):  # type: ignore[no-redef]
        _anonymous_ = ("u",)
        _fields_    = [("u", _jvalue)]

    del _jvalue

class _jfieldID(ct.Structure): pass
if TYPE_CHECKING:
    jfieldID: TypeAlias = Pointer[_jfieldID]
else:
    jfieldID = POINTER(_jfieldID)  # = ct.c_void_p

class _jmethodID(ct.Structure): pass
if TYPE_CHECKING:
    jmethodID: TypeAlias = Pointer[_jmethodID]
else:
    jmethodID = POINTER(_jmethodID)  # = ct.c_void_p

# Return values from jobjectRefType

jobjectRefType = ct.c_int
JNIInvalidRefType:    Final[int] = 0
JNILocalRefType:      Final[int] = 1
JNIGlobalRefType:     Final[int] = 2
JNIWeakGlobalRefType: Final[int] = 3

#
# jboolean constants
#

JNI_FALSE: Final[int] = 0
JNI_TRUE:  Final[int] = 1

#
# possible return values for JNI functions.
#

JNI_OK:        Final[int] =  0  # success
JNI_ERR:       Final[int] = -1  # unknown error
JNI_EDETACHED: Final[int] = -2  # thread detached from the VM
JNI_EVERSION:  Final[int] = -3  # JNI version error
JNI_ENOMEM:    Final[int] = -4  # not enough memory
JNI_EEXIST:    Final[int] = -5  # VM already created
JNI_EINVAL:    Final[int] = -6  # invalid arguments

#
# used in ReleaseScalarArrayElements
#

JNI_COMMIT: Final[int] = 1
JNI_ABORT:  Final[int] = 2

#
# JNI Native Method Interface.
#

# used in RegisterNatives to describe native method name, signature,
# and function pointer.

class JNINativeMethod(ct.Structure):
    _fields_ = [
    ("name",      ct.c_char_p),
    ("signature", ct.c_char_p),
    ("fnPtr",     ct.c_void_p)
]

class JNINativeInterface_(ct.Structure):
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

class JNIEnv(ct.Structure):
    _fields_ = [("functions", POINTER(JNINativeInterface_))]

    def _handle_JNIException(self, err: int) -> None:
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def _handle_JavaException(self) -> Throwable:
        env = self
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
        env = self
        fun = self.functions[0]
        ret: int = fun.GetVersion(env)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java class handling

    def DefineClass(self, name: bytes, loader: jobject, buf: Pointer[jbyte], blen: jsize | int) -> jclass:
        env = self
        fun = self.functions[0]
        ret = fun.DefineClass(env, name, loader, buf, blen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jclass(ret)

    def FindClass(self, name: bytes) -> jclass:
        env = self
        fun = self.functions[0]
        ret = fun.FindClass(env, name)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jclass(ret)

    def GetSuperclass(self, sub: jclass) -> jclass | None:
        env = self
        fun = self.functions[0]
        ret = fun.GetSuperclass(env, sub)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jclass(ret) if ret else None

    def IsAssignableFrom(self, sub: jclass, sup: jclass) -> bool:
        env = self
        fun = self.functions[0]
        return bool(fun.IsAssignableFrom(env, sub, sup))

    # Java exceptions handling

    def Throw(self, obj: jthrowable) -> None:
        env = self
        fun = self.functions[0]
        ret = fun.Throw(env, obj)
        if ret != 0: self._handle_JNIException(ret)

    def ThrowNew(self, clazz: jclass, msg: bytes) -> None:
        env = self
        fun = self.functions[0]
        ret = fun.ThrowNew(env, clazz, msg)
        if ret != 0: self._handle_JNIException(ret)

    def ExceptionOccurred(self) -> jthrowable | None:
        env = self
        fun = self.functions[0]
        ret = fun.ExceptionOccurred(env)
        return jthrowable(ret) if ret else None

    def ExceptionDescribe(self) -> None:
        env = self
        fun = self.functions[0]
        fun.ExceptionDescribe(env)

    def ExceptionClear(self) -> None:
        env = self
        fun = self.functions[0]
        if Throwable.last:
            jthr = Throwable.last.getJThrowable()
            if jthr: fun.DeleteGlobalRef(env, jthr)
            Throwable.last = None
        fun.ExceptionClear(env)

    def FatalError(self, msg: bytes) -> None:
        env = self
        fun = self.functions[0]
        fun.FatalError(env, msg)

    def ExceptionCheck(self) -> bool:
        env = self
        fun = self.functions[0]
        return bool(fun.ExceptionCheck(env))

    # JVM Call frame

    def PushLocalFrame(self, capacity: jint | int) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.PushLocalFrame(env, capacity)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def PopLocalFrame(self, result: jobject | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.PopLocalFrame(env, result if result is not None else jobject())
        return jobject(ret)

    # Java references handling

    def NewGlobalRef(self, lobj: jobject) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.NewGlobalRef(env, lobj)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def DeleteGlobalRef(self, gref: jobject) -> None:
        env = self
        fun = self.functions[0]
        if gref: fun.DeleteGlobalRef(env, gref)

    def NewLocalRef(self, ref: jobject) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.NewLocalRef(env, ref)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def DeleteLocalRef(self, obj: jobject) -> None:
        env = self
        fun = self.functions[0]
        if obj: fun.DeleteLocalRef(env, obj)

    def NewWeakGlobalRef(self, obj: jobject) -> jweak:
        env = self
        fun = self.functions[0]
        ret = fun.NewWeakGlobalRef(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jweak(ret)

    def DeleteWeakGlobalRef(self, ref: jweak) -> None:
        env = self
        fun = self.functions[0]
        fun.DeleteWeakGlobalRef(env, ref)

    def EnsureLocalCapacity(self, capacity: jint | int) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.EnsureLocalCapacity(env, capacity)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java objects handling

    def AllocObject(self, clazz: jclass) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.AllocObject(env, clazz)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def NewObject(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.NewObjectA(env, clazz, methodID, args)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def GetObjectClass(self, obj: jobject) -> jclass:
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectClass(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jclass(ret)

    def GetObjectRefType(self, obj: jobject) -> int:
        # New in JNI 1.6
        env = self
        fun = self.functions[0]
        ret: int = fun.GetObjectRefType(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def IsInstanceOf(self, obj: jobject, clazz: jclass) -> bool:
        env = self
        fun = self.functions[0]
        return bool(fun.IsInstanceOf(env, obj, clazz))

    def IsSameObject(self, obj1: jobject, obj2: jobject) -> bool:
        env = self
        fun = self.functions[0]
        return bool(fun.IsSameObject(env, obj1, obj2))

    # Call Java instance method

    def GetMethodID(self, clazz: jclass, name: bytes, sig: bytes) -> jmethodID:
        env = self
        fun = self.functions[0]
        ret: jmethodID = fun.GetMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallObjectMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.CallObjectMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def CallBooleanMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> bool:
        env = self
        fun = self.functions[0]
        ret = fun.CallBooleanMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallByteMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallByteMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallCharMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> str:
        env = self
        fun = self.functions[0]
        ret: str = fun.CallCharMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallShortMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallShortMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallIntMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallIntMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallLongMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallLongMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallFloatMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.CallFloatMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallDoubleMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.CallDoubleMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallVoidMethod(self, obj: jobject, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> None:
        env = self
        fun = self.functions[0]
        fun.CallVoidMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... nonvirtually

    def CallNonvirtualObjectMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualObjectMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def CallNonvirtualBooleanMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> bool:
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualBooleanMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallNonvirtualByteMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualByteMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualCharMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> str:
        env = self
        fun = self.functions[0]
        ret: str = fun.CallNonvirtualCharMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualShortMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualShortMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualIntMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualIntMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualLongMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallNonvirtualLongMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualFloatMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.CallNonvirtualFloatMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualDoubleMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.CallNonvirtualDoubleMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualVoidMethod(self, obj: jobject, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> None:
        env = self
        fun = self.functions[0]
        fun.CallNonvirtualVoidMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java instance fields

    def GetFieldID(self, clazz: jclass, name: bytes, sig: bytes) -> jfieldID:
        env = self
        fun = self.functions[0]
        ret: jfieldID = fun.GetFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectField(self, obj: jobject, fieldID: jfieldID) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def GetBooleanField(self, obj: jobject, fieldID: jfieldID) -> bool:
        env = self
        fun = self.functions[0]
        ret = fun.GetBooleanField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetByteField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetByteField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharField(self, obj: jobject, fieldID: jfieldID) -> str:
        env = self
        fun = self.functions[0]
        ret: str = fun.GetCharField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetShortField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetIntField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongField(self, obj: jobject, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetLongField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatField(self, obj: jobject, fieldID: jfieldID) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.GetFloatField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleField(self, obj: jobject, fieldID: jfieldID) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.GetDoubleField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java instance fields

    def SetObjectField(self, obj: jobject, fieldID: jfieldID, value: jobject) -> None:
        env = self
        fun = self.functions[0]
        fun.SetObjectField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanField(self, obj: jobject, fieldID: jfieldID, value: jboolean | bool) -> None:
        env = self
        fun = self.functions[0]
        fun.SetBooleanField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteField(self, obj: jobject, fieldID: jfieldID, value: jbyte | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetByteField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharField(self, obj: jobject, fieldID: jfieldID, value: jchar | str) -> None:
        env = self
        fun = self.functions[0]
        fun.SetCharField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortField(self, obj: jobject, fieldID: jfieldID, value: jshort | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetShortField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntField(self, obj: jobject, fieldID: jfieldID, value: jint | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetIntField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongField(self, obj: jobject, fieldID: jfieldID, value: jlong | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetLongField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatField(self, obj: jobject, fieldID: jfieldID, value: jfloat | float) -> None:
        env = self
        fun = self.functions[0]
        fun.SetFloatField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleField(self, obj: jobject, fieldID: jfieldID, value: jdouble | float) -> None:
        env = self
        fun = self.functions[0]
        fun.SetDoubleField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Call Java static method

    def GetStaticMethodID(self, clazz: jclass, name: bytes, sig: bytes) -> jmethodID:
        env = self
        fun = self.functions[0]
        ret: jmethodID = fun.GetStaticMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticObjectMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticObjectMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def CallStaticBooleanMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> bool:
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticBooleanMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallStaticByteMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallStaticByteMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticCharMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> str:
        env = self
        fun = self.functions[0]
        ret: str = fun.CallStaticCharMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticShortMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallStaticShortMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticIntMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallStaticIntMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticLongMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.CallStaticLongMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticFloatMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.CallStaticFloatMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticDoubleMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.CallStaticDoubleMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticVoidMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> None:
        env = self
        fun = self.functions[0]
        fun.CallStaticVoidMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java static fields

    def GetStaticFieldID(self, clazz: jclass, name: bytes, sig: bytes) -> jfieldID:
        env = self
        fun = self.functions[0]
        ret: jfieldID = fun.GetStaticFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticObjectField(self, clazz: jclass, fieldID: jfieldID) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticObjectField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def GetStaticBooleanField(self, clazz: jclass, fieldID: jfieldID) -> bool:
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticBooleanField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetStaticByteField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStaticByteField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticCharField(self, clazz: jclass, fieldID: jfieldID) -> str:
        env = self
        fun = self.functions[0]
        ret: str = fun.GetStaticCharField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticShortField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStaticShortField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticIntField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStaticIntField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticLongField(self, clazz: jclass, fieldID: jfieldID) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStaticLongField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticFloatField(self, clazz: jclass, fieldID: jfieldID) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.GetStaticFloatField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticDoubleField(self, clazz: jclass, fieldID: jfieldID) -> float:
        env = self
        fun = self.functions[0]
        ret: float = fun.GetStaticDoubleField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java static fields

    def SetStaticObjectField(self, clazz: jclass, fieldID: jfieldID, value: jobject) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticObjectField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticBooleanField(self, clazz: jclass, fieldID: jfieldID, value: jboolean | bool) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticBooleanField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticByteField(self, clazz: jclass, fieldID: jfieldID, value: jbyte | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticByteField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticCharField(self, clazz: jclass, fieldID: jfieldID, value: jchar | str) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticCharField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticShortField(self, clazz: jclass, fieldID: jfieldID, value: jshort | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticShortField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticIntField(self, clazz: jclass, fieldID: jfieldID, value: jint | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticIntField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticLongField(self, clazz: jclass, fieldID: jfieldID, value: jlong | int) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticLongField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticFloatField(self, clazz: jclass, fieldID: jfieldID, value: jfloat | float) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticFloatField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticDoubleField(self, clazz: jclass, fieldID: jfieldID, value: jdouble | float) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticDoubleField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java strings handling

    def NewString(self, unicode: str, slen: jsize | int) -> jstring:
        env = self
        fun = self.functions[0]
        ret = fun.NewString(env, unicode, slen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jstring(ret)

    def GetStringLength(self, str: jstring) -> int:  # noqa: A002
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStringLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringChars(self, str: jstring, isCopy: Pointer[jboolean] | None = None) -> Pointer[jchar]:  # noqa: A002
        env = self
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetStringChars(env, str, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringChars(self, str: jstring, chars: Pointer[jchar]) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.ReleaseStringChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewStringUTF(self, utf: bytes) -> jstring:
        env = self
        fun = self.functions[0]
        ret = fun.NewStringUTF(env, utf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jstring(ret)

    def GetStringUTFLength(self, str: jstring) -> int:  # noqa: A002
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStringUTFLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFLengthAsLong(self, str: jstring) -> int:  # noqa: A002
        # Since: JDK/JRE 24.0
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStringUTFLengthAsLong(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFChars(self, str: jstring, isCopy: Pointer[jboolean] | None = None) -> Pointer[ct.c_char]:  # noqa: A002
        env = self
        fun = self.functions[0]
        ret: Pointer[ct.c_char] = fun.GetStringUTFChars(env, str, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringUTFChars(self, str: jstring, chars: Pointer[ct.c_char]) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.ReleaseStringUTFChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringRegion(self, str: jstring, start: jsize | int, len: jsize | int, buf: Pointer[jchar]) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.GetStringRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringUTFRegion(self, str: jstring, start: jsize | int, len: jsize | int, buf: Pointer[ct.c_char]) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.GetStringUTFRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetStringCritical(self, string: jstring, isCopy: Pointer[jboolean] | None = None) -> Pointer[jchar]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetStringCritical(env, string, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringCritical(self, string: jstring, cstring: Pointer[jchar]) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseStringCritical(env, string, cstring)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java arrays handling

    def GetArrayLength(self, array: jarray) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetArrayLength(env, array)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObjectArray(self, size: jsize | int, clazz: jclass, init: jobject | None = None) -> jobjectArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewObjectArray(env, size, clazz, init)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jobjectArray(ret)

    def GetObjectArrayElement(self, array: jobjectArray, index: jsize | int) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectArrayElement(env, array, index)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def SetObjectArrayElement(self, array: jobjectArray, index: jsize | int, value: jobject) -> None:
        env = self
        fun = self.functions[0]
        fun.SetObjectArrayElement(env, array, index, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewBooleanArray(self, size: jsize | int) -> jbooleanArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewBooleanArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jbooleanArray(ret)

    def NewByteArray(self, size: jsize | int) -> jbyteArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewByteArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jbyteArray(ret)

    def NewCharArray(self, size: jsize | int) -> jcharArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewCharArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jcharArray(ret)

    def NewShortArray(self, size: jsize | int) -> jshortArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewShortArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jshortArray(ret)

    def NewIntArray(self, size: jsize | int) -> jintArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewIntArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jintArray(ret)

    def NewLongArray(self, size: jsize | int) -> jlongArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewLongArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jlongArray(ret)

    def NewFloatArray(self, size: jsize | int) -> jfloatArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewFloatArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jfloatArray(ret)

    def NewDoubleArray(self, size: jsize | int) -> jdoubleArray:
        env = self
        fun = self.functions[0]
        ret = fun.NewDoubleArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jdoubleArray(ret)

    def GetBooleanArrayElements(self, array: jbooleanArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jboolean]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jboolean] = fun.GetBooleanArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetByteArrayElements(self, array: jbyteArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jbyte]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jbyte] = fun.GetByteArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharArrayElements(self, array: jcharArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jchar]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetCharArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortArrayElements(self, array: jshortArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jshort]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jshort] = fun.GetShortArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntArrayElements(self, array: jintArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jint]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jint] = fun.GetIntArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongArrayElements(self, array: jlongArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jlong]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jlong] = fun.GetLongArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatArrayElements(self, array: jfloatArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jfloat]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jfloat] = fun.GetFloatArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleArrayElements(self, array: jdoubleArray, isCopy: Pointer[jboolean] | None = None) -> Pointer[jdouble]:
        env = self
        fun = self.functions[0]
        ret: Pointer[jdouble] = fun.GetDoubleArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseBooleanArrayElements(self, array: jbooleanArray, elems: Pointer[jboolean], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseBooleanArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseByteArrayElements(self, array: jbyteArray, elems: Pointer[jbyte], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseByteArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseCharArrayElements(self, array: jcharArray, elems: Pointer[jchar], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseCharArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseShortArrayElements(self, array: jshortArray, elems: Pointer[jshort], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseShortArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseIntArrayElements(self, array: jintArray, elems: Pointer[jint], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseIntArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseLongArrayElements(self, array: jlongArray, elems: Pointer[jlong], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseLongArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseFloatArrayElements(self, array: jfloatArray, elems: Pointer[jfloat], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseFloatArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseDoubleArrayElements(self, array: jdoubleArray, elems: Pointer[jdouble], mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseDoubleArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetBooleanArrayRegion(self, array: jbooleanArray, start: jint | int, size: jint | int, buf: Pointer[jboolean]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetByteArrayRegion(self, array: jbyteArray, start: jint | int, size: jint | int, buf: Pointer[jbyte]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetCharArrayRegion(self, array: jcharArray, start: jint | int, size: jint | int, buf: Pointer[jchar]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetShortArrayRegion(self, array: jshortArray, start: jint | int, size: jint | int, buf: Pointer[jshort]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetIntArrayRegion(self, array: jintArray, start: jint | int, size: jint | int, buf: Pointer[jint]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetLongArrayRegion(self, array: jlongArray, start: jint | int, size: jint | int, buf: Pointer[jlong]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetFloatArrayRegion(self, array: jfloatArray, start: jint | int, size: jint | int, buf: Pointer[jfloat]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetDoubleArrayRegion(self, array: jdoubleArray, start: jint | int, size: jint | int, buf: Pointer[jdouble]) -> None:
        env = self
        fun = self.functions[0]
        fun.GetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanArrayRegion(self, array: jbooleanArray, start: jint | int, size: jint | int, buf: Pointer[jboolean]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteArrayRegion(self, array: jbyteArray, start: jint | int, size: jint | int, buf: Pointer[jbyte]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharArrayRegion(self, array: jcharArray, start: jint | int, size: jint | int, buf: Pointer[jchar]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortArrayRegion(self, array: jshortArray, start: jint | int, size: jint | int, buf: Pointer[jshort]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntArrayRegion(self, array: jintArray, start: jint | int, size: jint | int, buf: Pointer[jint]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongArrayRegion(self, array: jlongArray, start: jint | int, size: jint | int, buf: Pointer[jlong]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatArrayRegion(self, array: jfloatArray, start: jint | int, size: jint | int, buf: Pointer[jfloat]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleArrayRegion(self, array: jdoubleArray, start: jint | int, size: jint | int, buf: Pointer[jdouble]) -> None:
        env = self
        fun = self.functions[0]
        fun.SetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetPrimitiveArrayCritical(self, array: jarray, isCopy: Pointer[jboolean] | None = None) -> ct.c_void_p:
        env = self
        fun = self.functions[0]
        ret = fun.GetPrimitiveArrayCritical(env, array, isCopy)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ct.c_void_p(ret)

    def ReleasePrimitiveArrayCritical(self, array: jarray, carray: ct.c_void_p, mode: jint | int = 0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleasePrimitiveArrayCritical(env, array, carray, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java native methods handling

    def RegisterNatives(self, clazz: jclass, methods: Pointer[JNINativeMethod], nMethods: jint | int) -> int:
        env = self
        fun = self.functions[0]
        # Required due to bug in jvm:
        # https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6493522
        fun.GetMethodID(env, clazz, b"notify", b"()V")
        ret: int = fun.RegisterNatives(env, clazz, methods, nMethods)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def UnregisterNatives(self, clazz: jclass) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.UnregisterNatives(env, clazz)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java object monitoring

    def MonitorEnter(self, obj: jobject) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.MonitorEnter(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def MonitorExit(self, obj: jobject) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.MonitorExit(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java direct buffer handling

    def NewDirectByteBuffer(self, address: Pointer[ct.c_char], capacity: jlong | int) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.NewDirectByteBuffer(env, address, capacity)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def GetDirectBufferAddress(self, buf: jobject) -> Pointer[ct.c_char]:
        env = self
        fun = self.functions[0]
        ret: Pointer[ct.c_char] = fun.GetDirectBufferAddress(env, buf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferCapacity(self, buf: jobject) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetDirectBufferCapacity(env, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java reflection support

    def FromReflectedMethod(self, method: jobject) -> jmethodID:
        env = self
        fun = self.functions[0]
        ret: jmethodID = fun.FromReflectedMethod(env, method)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FromReflectedField(self, field: jobject) -> jfieldID:
        env = self
        fun = self.functions[0]
        ret: jfieldID = fun.FromReflectedField(env, field)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedMethod(self, cls: jclass, methodID: jmethodID, isStatic: jboolean | bool) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.ToReflectedMethod(env, cls, methodID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    def ToReflectedField(self, cls: jclass, fieldID: jfieldID, isStatic: jboolean | bool) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.ToReflectedField(env, cls, fieldID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    # Java VM Interface

    def GetJavaVM(self, vm: Pointer[Pointer[JavaVM]]) -> None:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetJavaVM(env, vm)
        if ret != 0: self._handle_JNIException(ret)

    # Module Features

    def GetModule(self, clazz: jclass) -> jobject:
        # Since: JDK/JRE 9.0
        env = self
        fun = self.functions[0]
        ret = fun.GetModule(env, clazz)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return jobject(ret)

    # Virtual threads

    def IsVirtualThread(self, obj: jobject) -> bool:
        # Since: JDK/JRE 19.0
        env = self
        fun = self.functions[0]
        ret = fun.IsVirtualThread(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

def JEnv(penv: Pointer[JNIEnv]) -> JNIEnv:
    env: JNIEnv = penv[0]
    return env

#
# JNI Invocation Interface.
#

class JNIInvokeInterface_(ct.Structure):
    pass

class JavaVM(ct.Structure):
    _fields_ = [("functions", POINTER(JNIInvokeInterface_))]

    def _handle_JNIException(self, err: int) -> None:
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def DestroyJavaVM(self) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.DestroyJavaVM(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThread(self, penv: Pointer[Pointer[JNIEnv]], args: Pointer[JavaVMAttachArgs] | None = None) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.AttachCurrentThread(jvm, penv, args)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThreadAsDaemon(self, penv: Pointer[Pointer[JNIEnv]], args: Pointer[JavaVMAttachArgs] | None = None) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.AttachCurrentThreadAsDaemon(jvm, penv, args)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def DetachCurrentThread(self) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.DetachCurrentThread(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def GetEnv(self, penv: Pointer[Pointer[JNIEnv]], version: jint | int) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.GetEnv(jvm, penv, version)
        if ret != JNI_OK: self._handle_JNIException(ret)

def JVM(pjvm: Pointer[JavaVM]) -> JavaVM:
    jvm: JavaVM = pjvm[0]
    return jvm

# JNI Native Method Interface.

va_list = ct.c_void_p  # temporary

JNINativeInterface_._fields_ = [
    ("reserved0", ct.c_void_p),
    ("reserved1", ct.c_void_p),
    ("reserved2", ct.c_void_p),
    ("reserved3", ct.c_void_p),

    ("GetVersion",                    CFUNC(jint,               POINTER(JNIEnv))),

    ("DefineClass",                   CFUNC(jclass,             POINTER(JNIEnv), ct.c_char_p, jobject, POINTER(jbyte), jsize)),
    ("FindClass",                     CFUNC(jclass,             POINTER(JNIEnv), ct.c_char_p)),

    ("FromReflectedMethod",           CFUNC(jmethodID,          POINTER(JNIEnv), jobject)),
    ("FromReflectedField",            CFUNC(jfieldID,           POINTER(JNIEnv), jobject)),

    ("ToReflectedMethod",             CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID, jboolean)),

    ("GetSuperclass",                 CFUNC(jclass,             POINTER(JNIEnv), jclass)),
    ("IsAssignableFrom",              CFUNC(jboolean,           POINTER(JNIEnv), jclass, jclass)),

    ("ToReflectedField",              CFUNC(jobject,            POINTER(JNIEnv), jclass, jfieldID, jboolean)),

    ("Throw",                         CFUNC(jint,               POINTER(JNIEnv), jthrowable)),
    ("ThrowNew",                      CFUNC(jint,               POINTER(JNIEnv), jclass, ct.c_char_p)),
    ("ExceptionOccurred",             CFUNC(jthrowable,         POINTER(JNIEnv))),
    ("ExceptionDescribe",             CFUNC(None,               POINTER(JNIEnv))),
    ("ExceptionClear",                CFUNC(None,               POINTER(JNIEnv))),
    ("FatalError",                    CFUNC(None,               POINTER(JNIEnv), ct.c_char_p)),

    ("PushLocalFrame",                CFUNC(jint,               POINTER(JNIEnv), jint)),
    ("PopLocalFrame",                 CFUNC(jobject,            POINTER(JNIEnv), jobject)),

    ("NewGlobalRef",                  CFUNC(jobject,            POINTER(JNIEnv), jobject)),
    ("DeleteGlobalRef",               CFUNC(None,               POINTER(JNIEnv), jobject)),
    ("DeleteLocalRef",                CFUNC(None,               POINTER(JNIEnv), jobject)),
    ("IsSameObject",                  CFUNC(jboolean,           POINTER(JNIEnv), jobject, jobject)),
    ("NewLocalRef",                   CFUNC(jobject,            POINTER(JNIEnv), jobject)),
    ("EnsureLocalCapacity",           CFUNC(jint,               POINTER(JNIEnv), jint)),

    ("AllocObject",                   CFUNC(jobject,            POINTER(JNIEnv), jclass)),
    ("NewObject",                     CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("NewObjectV",                    CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("NewObjectA",                    CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("GetObjectClass",                CFUNC(jclass,             POINTER(JNIEnv), jobject)),
    ("IsInstanceOf",                  CFUNC(jboolean,           POINTER(JNIEnv), jobject, jclass)),

    ("GetMethodID",                   CFUNC(jmethodID,          POINTER(JNIEnv), jclass, ct.c_char_p, ct.c_char_p)),

    ("CallObjectMethod",              CFUNC(jobject,            POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallObjectMethodV",             CFUNC(jobject,            POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallObjectMethodA",             CFUNC(jobject,            POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallBooleanMethod",             CFUNC(jboolean,           POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallBooleanMethodV",            CFUNC(jboolean,           POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallBooleanMethodA",            CFUNC(jboolean,           POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallByteMethod",                CFUNC(jbyte,              POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallByteMethodV",               CFUNC(jbyte,              POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallByteMethodA",               CFUNC(jbyte,              POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallCharMethod",                CFUNC(jchar,              POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallCharMethodV",               CFUNC(jchar,              POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallCharMethodA",               CFUNC(jchar,              POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallShortMethod",               CFUNC(jshort,             POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallShortMethodV",              CFUNC(jshort,             POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallShortMethodA",              CFUNC(jshort,             POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallIntMethod",                 CFUNC(jint,               POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallIntMethodV",                CFUNC(jint,               POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallIntMethodA",                CFUNC(jint,               POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallLongMethod",                CFUNC(jlong,              POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallLongMethodV",               CFUNC(jlong,              POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallLongMethodA",               CFUNC(jlong,              POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallFloatMethod",               CFUNC(jfloat,             POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallFloatMethodV",              CFUNC(jfloat,             POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallFloatMethodA",              CFUNC(jfloat,             POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallDoubleMethod",              CFUNC(jdouble,            POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallDoubleMethodV",             CFUNC(jdouble,            POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallDoubleMethodA",             CFUNC(jdouble,            POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallVoidMethod",                CFUNC(None,               POINTER(JNIEnv), jobject, jmethodID)),  # ...),
    ("CallVoidMethodV",               CFUNC(None,               POINTER(JNIEnv), jobject, jmethodID, va_list)),
    ("CallVoidMethodA",               CFUNC(None,               POINTER(JNIEnv), jobject, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualObjectMethod",    CFUNC(jobject,            POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualObjectMethodV",   CFUNC(jobject,            POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualObjectMethodA",   CFUNC(jobject,            POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualBooleanMethod",   CFUNC(jboolean,           POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualBooleanMethodV",  CFUNC(jboolean,           POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualBooleanMethodA",  CFUNC(jboolean,           POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualByteMethod",      CFUNC(jbyte,              POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualByteMethodV",     CFUNC(jbyte,              POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualByteMethodA",     CFUNC(jbyte,              POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualCharMethod",      CFUNC(jchar,              POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualCharMethodV",     CFUNC(jchar,              POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualCharMethodA",     CFUNC(jchar,              POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualShortMethod",     CFUNC(jshort,             POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualShortMethodV",    CFUNC(jshort,             POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualShortMethodA",    CFUNC(jshort,             POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualIntMethod",       CFUNC(jint,               POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualIntMethodV",      CFUNC(jint,               POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualIntMethodA",      CFUNC(jint,               POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualLongMethod",      CFUNC(jlong,              POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualLongMethodV",     CFUNC(jlong,              POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualLongMethodA",     CFUNC(jlong,              POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualFloatMethod",     CFUNC(jfloat,             POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualFloatMethodV",    CFUNC(jfloat,             POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualFloatMethodA",    CFUNC(jfloat,             POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualDoubleMethod",    CFUNC(jdouble,            POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualDoubleMethodV",   CFUNC(jdouble,            POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualDoubleMethodA",   CFUNC(jdouble,            POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("CallNonvirtualVoidMethod",      CFUNC(None,               POINTER(JNIEnv), jobject, jclass, jmethodID)),  # ...),
    ("CallNonvirtualVoidMethodV",     CFUNC(None,               POINTER(JNIEnv), jobject, jclass, jmethodID, va_list)),
    ("CallNonvirtualVoidMethodA",     CFUNC(None,               POINTER(JNIEnv), jobject, jclass, jmethodID, POINTER(jvalue))),

    ("GetFieldID",                    CFUNC(jfieldID,           POINTER(JNIEnv), jclass, ct.c_char_p, ct.c_char_p)),

    ("GetObjectField",                CFUNC(jobject,            POINTER(JNIEnv), jobject, jfieldID)),
    ("GetBooleanField",               CFUNC(jboolean,           POINTER(JNIEnv), jobject, jfieldID)),
    ("GetByteField",                  CFUNC(jbyte,              POINTER(JNIEnv), jobject, jfieldID)),
    ("GetCharField",                  CFUNC(jchar,              POINTER(JNIEnv), jobject, jfieldID)),
    ("GetShortField",                 CFUNC(jshort,             POINTER(JNIEnv), jobject, jfieldID)),
    ("GetIntField",                   CFUNC(jint,               POINTER(JNIEnv), jobject, jfieldID)),
    ("GetLongField",                  CFUNC(jlong,              POINTER(JNIEnv), jobject, jfieldID)),
    ("GetFloatField",                 CFUNC(jfloat,             POINTER(JNIEnv), jobject, jfieldID)),
    ("GetDoubleField",                CFUNC(jdouble,            POINTER(JNIEnv), jobject, jfieldID)),

    ("SetObjectField",                CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jobject)),
    ("SetBooleanField",               CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jboolean)),
    ("SetByteField",                  CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jbyte)),
    ("SetCharField",                  CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jchar)),
    ("SetShortField",                 CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jshort)),
    ("SetIntField",                   CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jint)),
    ("SetLongField",                  CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jlong)),
    ("SetFloatField",                 CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jfloat)),
    ("SetDoubleField",                CFUNC(None,               POINTER(JNIEnv), jobject, jfieldID, jdouble)),

    ("GetStaticMethodID",             CFUNC(jmethodID,          POINTER(JNIEnv), jclass, ct.c_char_p, ct.c_char_p)),

    ("CallStaticObjectMethod",        CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticObjectMethodV",       CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticObjectMethodA",       CFUNC(jobject,            POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticBooleanMethod",       CFUNC(jboolean,           POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticBooleanMethodV",      CFUNC(jboolean,           POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticBooleanMethodA",      CFUNC(jboolean,           POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticByteMethod",          CFUNC(jbyte,              POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticByteMethodV",         CFUNC(jbyte,              POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticByteMethodA",         CFUNC(jbyte,              POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticCharMethod",          CFUNC(jchar,              POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticCharMethodV",         CFUNC(jchar,              POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticCharMethodA",         CFUNC(jchar,              POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticShortMethod",         CFUNC(jshort,             POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticShortMethodV",        CFUNC(jshort,             POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticShortMethodA",        CFUNC(jshort,             POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticIntMethod",           CFUNC(jint,               POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticIntMethodV",          CFUNC(jint,               POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticIntMethodA",          CFUNC(jint,               POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticLongMethod",          CFUNC(jlong,              POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticLongMethodV",         CFUNC(jlong,              POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticLongMethodA",         CFUNC(jlong,              POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticFloatMethod",         CFUNC(jfloat,             POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticFloatMethodV",        CFUNC(jfloat,             POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticFloatMethodA",        CFUNC(jfloat,             POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticDoubleMethod",        CFUNC(jdouble,            POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticDoubleMethodV",       CFUNC(jdouble,            POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticDoubleMethodA",       CFUNC(jdouble,            POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("CallStaticVoidMethod",          CFUNC(None,               POINTER(JNIEnv), jclass, jmethodID)),  # ...),
    ("CallStaticVoidMethodV",         CFUNC(None,               POINTER(JNIEnv), jclass, jmethodID, va_list)),
    ("CallStaticVoidMethodA",         CFUNC(None,               POINTER(JNIEnv), jclass, jmethodID, POINTER(jvalue))),

    ("GetStaticFieldID",              CFUNC(jfieldID,           POINTER(JNIEnv), jclass, ct.c_char_p, ct.c_char_p)),

    ("GetStaticObjectField",          CFUNC(jobject,            POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticBooleanField",         CFUNC(jboolean,           POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticByteField",            CFUNC(jbyte,              POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticCharField",            CFUNC(jchar,              POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticShortField",           CFUNC(jshort,             POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticIntField",             CFUNC(jint,               POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticLongField",            CFUNC(jlong,              POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticFloatField",           CFUNC(jfloat,             POINTER(JNIEnv), jclass, jfieldID)),
    ("GetStaticDoubleField",          CFUNC(jdouble,            POINTER(JNIEnv), jclass, jfieldID)),

    ("SetStaticObjectField",          CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jobject)),
    ("SetStaticBooleanField",         CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jboolean)),
    ("SetStaticByteField",            CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jbyte)),
    ("SetStaticCharField",            CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jchar)),
    ("SetStaticShortField",           CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jshort)),
    ("SetStaticIntField",             CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jint)),
    ("SetStaticLongField",            CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jlong)),
    ("SetStaticFloatField",           CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jfloat)),
    ("SetStaticDoubleField",          CFUNC(None,               POINTER(JNIEnv), jclass, jfieldID, jdouble)),

    ("NewString",                     CFUNC(jstring,            POINTER(JNIEnv), POINTER(jchar), jsize)),
    ("GetStringLength",               CFUNC(jsize,              POINTER(JNIEnv), jstring)),
    ("GetStringChars",                CFUNC(POINTER(jchar),     POINTER(JNIEnv), jstring, POINTER(jboolean))),
    ("ReleaseStringChars",            CFUNC(None,               POINTER(JNIEnv), jstring, POINTER(jchar))),

    ("NewStringUTF",                  CFUNC(jstring,            POINTER(JNIEnv), POINTER(ct.c_char))),
    ("GetStringUTFLength",            CFUNC(jsize,              POINTER(JNIEnv), jstring)),
    ("GetStringUTFChars",             CFUNC(POINTER(ct.c_char), POINTER(JNIEnv), jstring, POINTER(jboolean))),
    ("ReleaseStringUTFChars",         CFUNC(None,               POINTER(JNIEnv), jstring, POINTER(ct.c_char))),

    ("GetArrayLength",                CFUNC(jsize,              POINTER(JNIEnv), jarray)),

    ("NewObjectArray",                CFUNC(jobjectArray,       POINTER(JNIEnv), jsize, jclass, jobject)),
    ("GetObjectArrayElement",         CFUNC(jobject,            POINTER(JNIEnv), jobjectArray, jsize)),
    ("SetObjectArrayElement",         CFUNC(None,               POINTER(JNIEnv), jobjectArray, jsize, jobject)),

    ("NewBooleanArray",               CFUNC(jbooleanArray,      POINTER(JNIEnv), jsize)),
    ("NewByteArray",                  CFUNC(jbyteArray,         POINTER(JNIEnv), jsize)),
    ("NewCharArray",                  CFUNC(jcharArray,         POINTER(JNIEnv), jsize)),
    ("NewShortArray",                 CFUNC(jshortArray,        POINTER(JNIEnv), jsize)),
    ("NewIntArray",                   CFUNC(jintArray,          POINTER(JNIEnv), jsize)),
    ("NewLongArray",                  CFUNC(jlongArray,         POINTER(JNIEnv), jsize)),
    ("NewFloatArray",                 CFUNC(jfloatArray,        POINTER(JNIEnv), jsize)),
    ("NewDoubleArray",                CFUNC(jdoubleArray,       POINTER(JNIEnv), jsize)),

    ("GetBooleanArrayElements",       CFUNC(POINTER(jboolean),  POINTER(JNIEnv), jbooleanArray, POINTER(jboolean))),
    ("GetByteArrayElements",          CFUNC(POINTER(jbyte),     POINTER(JNIEnv), jbyteArray,    POINTER(jboolean))),
    ("GetCharArrayElements",          CFUNC(POINTER(jchar),     POINTER(JNIEnv), jcharArray,    POINTER(jboolean))),
    ("GetShortArrayElements",         CFUNC(POINTER(jshort),    POINTER(JNIEnv), jshortArray,   POINTER(jboolean))),
    ("GetIntArrayElements",           CFUNC(POINTER(jint),      POINTER(JNIEnv), jintArray,     POINTER(jboolean))),
    ("GetLongArrayElements",          CFUNC(POINTER(jlong),     POINTER(JNIEnv), jlongArray,    POINTER(jboolean))),
    ("GetFloatArrayElements",         CFUNC(POINTER(jfloat),    POINTER(JNIEnv), jfloatArray,   POINTER(jboolean))),
    ("GetDoubleArrayElements",        CFUNC(POINTER(jdouble),   POINTER(JNIEnv), jdoubleArray,  POINTER(jboolean))),

    ("ReleaseBooleanArrayElements",   CFUNC(None,               POINTER(JNIEnv), jbooleanArray, POINTER(jboolean), jint)),
    ("ReleaseByteArrayElements",      CFUNC(None,               POINTER(JNIEnv), jbyteArray,    POINTER(jbyte),    jint)),
    ("ReleaseCharArrayElements",      CFUNC(None,               POINTER(JNIEnv), jcharArray,    POINTER(jchar),    jint)),
    ("ReleaseShortArrayElements",     CFUNC(None,               POINTER(JNIEnv), jshortArray,   POINTER(jshort),   jint)),
    ("ReleaseIntArrayElements",       CFUNC(None,               POINTER(JNIEnv), jintArray,     POINTER(jint),     jint)),
    ("ReleaseLongArrayElements",      CFUNC(None,               POINTER(JNIEnv), jlongArray,    POINTER(jlong),    jint)),
    ("ReleaseFloatArrayElements",     CFUNC(None,               POINTER(JNIEnv), jfloatArray,   POINTER(jfloat),   jint)),
    ("ReleaseDoubleArrayElements",    CFUNC(None,               POINTER(JNIEnv), jdoubleArray,  POINTER(jdouble),  jint)),

    ("GetBooleanArrayRegion",         CFUNC(None,               POINTER(JNIEnv), jbooleanArray, jsize, jsize, POINTER(jboolean))),
    ("GetByteArrayRegion",            CFUNC(None,               POINTER(JNIEnv), jbyteArray,    jsize, jsize, POINTER(jbyte))),
    ("GetCharArrayRegion",            CFUNC(None,               POINTER(JNIEnv), jcharArray,    jsize, jsize, POINTER(jchar))),
    ("GetShortArrayRegion",           CFUNC(None,               POINTER(JNIEnv), jshortArray,   jsize, jsize, POINTER(jshort))),
    ("GetIntArrayRegion",             CFUNC(None,               POINTER(JNIEnv), jintArray,     jsize, jsize, POINTER(jint))),
    ("GetLongArrayRegion",            CFUNC(None,               POINTER(JNIEnv), jlongArray,    jsize, jsize, POINTER(jlong))),
    ("GetFloatArrayRegion",           CFUNC(None,               POINTER(JNIEnv), jfloatArray,   jsize, jsize, POINTER(jfloat))),
    ("GetDoubleArrayRegion",          CFUNC(None,               POINTER(JNIEnv), jdoubleArray,  jsize, jsize, POINTER(jdouble))),

    ("SetBooleanArrayRegion",         CFUNC(None,               POINTER(JNIEnv), jbooleanArray, jsize, jsize, POINTER(jboolean))),
    ("SetByteArrayRegion",            CFUNC(None,               POINTER(JNIEnv), jbyteArray,    jsize, jsize, POINTER(jbyte))),
    ("SetCharArrayRegion",            CFUNC(None,               POINTER(JNIEnv), jcharArray,    jsize, jsize, POINTER(jchar))),
    ("SetShortArrayRegion",           CFUNC(None,               POINTER(JNIEnv), jshortArray,   jsize, jsize, POINTER(jshort))),
    ("SetIntArrayRegion",             CFUNC(None,               POINTER(JNIEnv), jintArray,     jsize, jsize, POINTER(jint))),
    ("SetLongArrayRegion",            CFUNC(None,               POINTER(JNIEnv), jlongArray,    jsize, jsize, POINTER(jlong))),
    ("SetFloatArrayRegion",           CFUNC(None,               POINTER(JNIEnv), jfloatArray,   jsize, jsize, POINTER(jfloat))),
    ("SetDoubleArrayRegion",          CFUNC(None,               POINTER(JNIEnv), jdoubleArray,  jsize, jsize, POINTER(jdouble))),

    ("RegisterNatives",               CFUNC(jint,               POINTER(JNIEnv), jclass, POINTER(JNINativeMethod), jint)),
    ("UnregisterNatives",             CFUNC(jint,               POINTER(JNIEnv), jclass)),

    ("MonitorEnter",                  CFUNC(jint,               POINTER(JNIEnv), jobject)),
    ("MonitorExit",                   CFUNC(jint,               POINTER(JNIEnv), jobject)),

    ("GetJavaVM",                     CFUNC(jint,               POINTER(JNIEnv), POINTER(POINTER(JavaVM)))),

    ("GetStringRegion",               CFUNC(None,               POINTER(JNIEnv), jstring, jsize, jsize, POINTER(jchar))),
    ("GetStringUTFRegion",            CFUNC(None,               POINTER(JNIEnv), jstring, jsize, jsize, POINTER(ct.c_char))),

    ("GetPrimitiveArrayCritical",     CFUNC(ct.c_void_p,        POINTER(JNIEnv), jarray, POINTER(jboolean))),
    ("ReleasePrimitiveArrayCritical", CFUNC(None,               POINTER(JNIEnv), jarray, ct.c_void_p, jint)),

    ("GetStringCritical",             CFUNC(POINTER(jchar),     POINTER(JNIEnv), jstring, POINTER(jboolean))),
    ("ReleaseStringCritical",         CFUNC(None,               POINTER(JNIEnv), jstring, POINTER(jchar))),

    ("NewWeakGlobalRef",              CFUNC(jweak,              POINTER(JNIEnv), jobject)),
    ("DeleteWeakGlobalRef",           CFUNC(None,               POINTER(JNIEnv), jweak)),

    ("ExceptionCheck",                CFUNC(jboolean,           POINTER(JNIEnv))),

    ("NewDirectByteBuffer",           CFUNC(jobject,            POINTER(JNIEnv), POINTER(ct.c_char), jlong)),
    ("GetDirectBufferAddress",        CFUNC(POINTER(ct.c_char), POINTER(JNIEnv), jobject)),
    ("GetDirectBufferCapacity",       CFUNC(jlong,              POINTER(JNIEnv), jobject)),

    # New JNI 1.6 Features
    ("GetObjectRefType",              CFUNC(jobjectRefType,     POINTER(JNIEnv), jobject)),

    # New JNI 9.0 Features
    ("GetModule",                     CFUNC(jobject,            POINTER(JNIEnv), jclass)),

    # New JNI 19.0 Features
    ("IsVirtualThread",               CFUNC(jboolean,           POINTER(JNIEnv), jobject)),

    # New JNI 24.0 Features
    ("GetStringUTFLengthAsLong",      CFUNC(jlong,              POINTER(JNIEnv), jstring)),
]

del JNINativeInterface_
del va_list

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
class JavaVMOption(ct.Structure):
    _fields_ = [
    ("optionString", ct.c_char_p),
    ("extraInfo",    ct.c_void_p),
]

class JavaVMInitArgs(ct.Structure):
    _fields_ = [
    ("version",            jint),
    ("nOptions",           jint),
    ("options",            POINTER(JavaVMOption)),
    ("ignoreUnrecognized", jboolean),
]

class JavaVMAttachArgs(ct.Structure):
    _fields_ = [
    ("version", jint),
    ("name",    ct.c_char_p),
    ("group",   jobject),
]

# These will be VM-specific.

JDK1_2: Final[int] = 1
JDK1_4: Final[int] = 1

# End VM-specific.

# JNI Invocation Interface.

JNIInvokeInterface_._fields_ = [
    ("reserved0", ct.c_void_p),
    ("reserved1", ct.c_void_p),
    ("reserved2", ct.c_void_p),

    ("DestroyJavaVM",               CFUNC(jint, POINTER(JavaVM))),
    ("AttachCurrentThread",         CFUNC(jint, POINTER(JavaVM), POINTER(POINTER(JNIEnv)), POINTER(JavaVMAttachArgs))),
    ("DetachCurrentThread",         CFUNC(jint, POINTER(JavaVM))),
    ("GetEnv",                      CFUNC(jint, POINTER(JavaVM), POINTER(POINTER(JNIEnv)), jint)),
    ("AttachCurrentThreadAsDaemon", CFUNC(jint, POINTER(JavaVM), POINTER(POINTER(JNIEnv)), POINTER(JavaVMAttachArgs)))
]

del JNIInvokeInterface_

# JNI version constants

JNI_VERSION_1_1: Final[int] = 0x00010001
JNI_VERSION_1_2: Final[int] = 0x00010002
JNI_VERSION_1_4: Final[int] = 0x00010004
JNI_VERSION_1_6: Final[int] = 0x00010006
JNI_VERSION_1_8: Final[int] = 0x00010008
JNI_VERSION_9:   Final[int] = 0x00090000
JNI_VERSION_10:  Final[int] = 0x000a0000
JNI_VERSION_19:  Final[int] = 0x00130000
JNI_VERSION_20:  Final[int] = 0x00140000
JNI_VERSION_21:  Final[int] = 0x00150000
JNI_VERSION_24:  Final[int] = 0x00180000

# eof jni.h

class Throwable(Exception):  # noqa: N818

    last: Throwable | None = None

    def __init__(self, jthr: jthrowable | None = None, info: jstring | None = None) -> None:
        """Initializer"""
        self._jthr: jthrowable = cast(jthr, jthrowable) if jthr is not None else jthrowable()
        self._info: jstring    = cast(info, jstring)    if info is not None else jstring()
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
         __dlclose=dlclose) -> type:

    import os
    try:
        dll = DLL(os.fspath(dll_path) if dll_path is not None else None, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError(f"{exc}") from None

    dllclose = classmethod(lambda cls, __dlclose=__dlclose: __dlclose(cls.dll._handle))

    def proto(restype: type | None, func: Callable[P, R], *argtypes: type | None) -> Callable[P, R]:
        func.restype  = restype   # type: ignore[attr-defined]
        func.argtypes = argtypes  # type: ignore[attr-defined]
        return func

    JNI = type("JNI", (), dict(dll=dll, dllclose=dllclose,
               GetDefaultJavaVMInitArgs = proto(jint, dll.JNI_GetDefaultJavaVMInitArgs, POINTER(JavaVMInitArgs)),
               CreateJavaVM = proto(jint, dll.JNI_CreateJavaVM, POINTER(POINTER(JavaVM)), POINTER(POINTER(JNIEnv)), POINTER(JavaVMInitArgs)),
               GetCreatedJavaVMs = proto(jint, dll.JNI_GetCreatedJavaVMs, POINTER(POINTER(JavaVM)), jsize, POINTER(jsize)),))

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

    def wrapper(fun: Callable[P, R]) -> JNINativeMethod:
        return JNINativeMethod(name=fun_name or fun.__name__.encode(),
                               signature=fun_sign,
                               fnPtr=cast(FunProto(fun), jobject))  # ct.c_void_p
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
    POINTER: TypeAlias = Pointer  # type: ignore[no-redef]
    del P, R

del dlclose
del _platform
