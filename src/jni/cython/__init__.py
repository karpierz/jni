# flake8-in-file-ignores: noqa: E305,E402,E501,N813,N814,N816,W504,    F405

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import ParamSpec, TypeVar, TypeAlias, Final
from typing_extensions import sentinel
from types  import GenericAlias  # noqa: F401
from collections.abc import Callable
from os import PathLike
import ctypes as ct
import cython as cy  # type: ignore[import-not-found]

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
    CType: TypeAlias = type
    P = ParamSpec("P")
    R = TypeVar("R")

def CFUNC(*args, **kwargs):
    return object()

__none = sentinel("__none")

def POINTER(ctype):
    return cy.pointer(ctype)
def pointer(obj):
    return cy.address(obj)

def byref(obj, offset=0):
    return __ffi.new(POINTER(__ffi.typeof(obj)), obj)  # !!! zamplementowac offset !!!

def addressof(obj):
    return cy.address(obj)
def cast(obj, ctype):
    return cy.cast(ctype, obj)
def sizeof(obj_or_ctype):
    return cy.sizeof(obj_or_ctype)

def py_object(obj):
    return __ffi.new_handle(obj)
def memmove(dst, src, count):
    return __ffi.memmove(dst, src, count)

def obj(ctype, init=__none):
    return ctype() if init is __none else ctype(init)

def new(ctype, init=__none):
    return __ffi.new(__ffi.getctype(ctype) + "*",
                     None if init is __none else init)
def new_array(ctype, size):
    return __ffi.new(__ffi.getctype(ctype)+"[]", size)
def new_cstr(init):
    return __ffi.new("char[]", init)
def new_cwstr(init):
    return __ffi.new("wchar_t[]", init)
def as_cstr(obj):
    return __ffi.cast("char*", __ffi.from_buffer(obj))
def as_cwstr(obj):
    return __ffi.cast("wchar_t*", __ffi.from_buffer(obj))
def to_bytes(obj, size=-1):
    return __ffi.string(obj, size) if size >= 0 else __ffi.string(obj)
def to_unicode(obj, size=-1):
    return __ffi.string(obj, size) if size >= 0 else __ffi.string(obj)
def from_buffer(data):
    return __ffi.from_buffer(data)
def isNULL(jobj) -> bool:
    return jobj == cy.NULL
NULL = cy.NULL  # null constant

def itself_or_null(arg):
    return arg
def byref_or_null(arg):
    return arg

from .jni import * ; del jni  # type: ignore[import-not-found] # noqa: F403,F821

#
# JNI Types
#

# jni_md.h contains the machine-dependent typedefs for jbyte, jint
# and jlong

jboolean: TypeAlias = cy.uchar
jbyte:    TypeAlias = cy.schar  # javabridge: unsigned (chyba blad!!!)
def jchar(val, *args, **kwargs):
    return cy.ushort(ord(val), *args, **kwargs)
jshort:   TypeAlias = cy.short
jint:     TypeAlias = cy.long
jlong:    TypeAlias = cy.longlong  # int64_t, jni.h: __int64
jfloat:   TypeAlias = cy.float
jdouble:  TypeAlias = cy.double
jsize:    TypeAlias = jint
CSimpleType: TypeAlias = (
    type[jboolean] |
    type[jbyte] |
    # type[jchar] |
    type[jshort] |
    type[jint] |
    type[jlong] |
    type[jfloat] |
    type[jdouble]
)

_jobject: TypeAlias = cy.struct()
if TYPE_CHECKING:
    jobject: TypeAlias = Pointer[_jobject]
else:
    jobject = POINTER(_jobject)
jclass:        TypeAlias = jobject
jthrowable:    TypeAlias = jobject
jstring:       TypeAlias = jobject
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

jvalue = cy.union(
    z = jboolean,
    b = jbyte,
    c = jchar,
    s = jshort,
    i = jint,
    j = jlong,
    f = jfloat,
    d = jdouble,
    l = jobject,
)

_jfieldID = cy.struct()
if TYPE_CHECKING:
    jfieldID: TypeAlias = Pointer[_jfieldID]
else:
    jfieldID = POINTER(_jfieldID)

_jmethodID = cy.struct()
if TYPE_CHECKING:
    jmethodID: TypeAlias = Pointer[_jmethodID]
else:
    jmethodID = POINTER(_jmethodID)

# Return values from jobjectRefType
# enum _jobjectType:
JNIInvalidRefType:    Final[int] = cy.const_int(0)
JNILocalRefType:      Final[int] = cy.const_int(1)
JNIGlobalRefType:     Final[int] = cy.const_int(2)
JNIWeakGlobalRefType: Final[int] = cy.const_int(3)
# jobjectRefType = _jobjectType
jobjectRefType = jint

#
# jboolean constants
#

JNI_FALSE: Final[int] = cy.const_int(0)
JNI_TRUE:  Final[int] = cy.const_int(1)

#
# possible return values for JNI functions.
#

JNI_OK:        Final[int] = cy.const_int(0)   # success
JNI_ERR:       Final[int] = cy.const_int(-1)  # unknown error
JNI_EDETACHED: Final[int] = cy.const_int(-2)  # thread detached from the VM
JNI_EVERSION:  Final[int] = cy.const_int(-3)  # JNI version error
JNI_ENOMEM:    Final[int] = cy.const_int(-4)  # not enough memory
JNI_EEXIST:    Final[int] = cy.const_int(-5)  # VM already created
JNI_EINVAL:    Final[int] = cy.const_int(-6)  # invalid arguments

#
# used in ReleaseScalarArrayElements
#

JNI_COMMIT: Final[int] = cy.const_int(1)
JNI_ABORT:  Final[int] = cy.const_int(2)

#
# JNI Native Method Interface.
#

# used in RegisterNatives to describe native method name, signature,
# and function pointer.

JNINativeMethod = cy.struct(
    name      = cy.p_char,  # Android and/or jnius: cy.p_const_char
    signature = cy.p_char,  # Android and/or jnius: cy.p_const_char
    fnPtr     = cy.p_void,
)

JNINativeInterface_ = cy.struct()

# We use inlined functions for C++ so that programmers can write:
#
#    env->FindClass("java/lang/String")
#
# in C++ rather than:
#
#    (*env)->FindClass(env, "java/lang/String")
#
# in C.

# JNIEnv = cy.const(cy.pointer(JNINativeInterface_))
class JNIEnv:

    __itself_or_null = itself_or_null
    __byref_or_null  = byref_or_null

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
        if Throwable.last:
            jthr = Throwable.last.getJThrowable()
            if jthr: fun.DeleteGlobalRef(env, jthr)
            Throwable.last = None
        fun.ExceptionClear(env)
        Throwable.last = thr = Throwable(jexc)  # !!!, fname)
        raise thr

    # Java version

    def GetVersion(self) -> int:
        env = self
        fun = self.functions[0]
        ret = fun.GetVersion(env)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java class handling

    def DefineClass(self, name, loader, buf, blen):
        env = self
        fun = self.functions[0]
        ret = fun.DefineClass(env, name, loader, buf, blen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FindClass(self, name: bytes) -> jclass:  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.FindClass(env, name)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetSuperclass(self, sub: jclass) -> jclass | None:
        env = self
        fun = self.functions[0]
        ret = fun.GetSuperclass(env, sub)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

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

    def ThrowNew(self, clazz, msg) -> None:
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

    def FatalError(self, msg) -> None:
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
        ret = fun.PushLocalFrame(env, capacity)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def PopLocalFrame(self, result: jobject | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.PopLocalFrame(env, result if result is not None else NULL)
        return ret

    # Java references handling

    def NewGlobalRef(self, lobj):
        env = self
        fun = self.functions[0]
        ret = fun.NewGlobalRef(env, lobj)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteGlobalRef(self, gref) -> None:
        env = self
        fun = self.functions[0]
        if gref: fun.DeleteGlobalRef(env, gref)

    def NewLocalRef(self, ref):
        env = self
        fun = self.functions[0]
        ret = fun.NewLocalRef(env, ref)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteLocalRef(self, obj) -> None:
        env = self
        fun = self.functions[0]
        if obj: fun.DeleteLocalRef(env, obj)

    def NewWeakGlobalRef(self, obj):
        env = self
        fun = self.functions[0]
        ret = fun.NewWeakGlobalRef(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteWeakGlobalRef(self, ref) -> None:
        env = self
        fun = self.functions[0]
        fun.DeleteWeakGlobalRef(env, ref)

    def EnsureLocalCapacity(self, capacity: jint | int):
        env = self
        fun = self.functions[0]
        ret = fun.EnsureLocalCapacity(env, capacity)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java objects handling

    def AllocObject(self, clazz: jclass) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.AllocObject(env, clazz)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObject(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.NewObjectA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectClass(self, obj: jobject) -> jclass:
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectClass(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectRefType(self, obj) -> int:
        # New in JNI 1.6
        env = self
        fun = self.functions[0]
        ret: int = fun.GetObjectRefType(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def IsInstanceOf(self, obj, clazz) -> bool:
        env = self
        fun = self.functions[0]
        return bool(fun.IsInstanceOf(env, obj, clazz))

    def IsSameObject(self, obj1, obj2) -> bool:
        env = self
        fun = self.functions[0]
        return bool(fun.IsSameObject(env, obj1, obj2))

    # Call Java instance method

    def GetMethodID(self, clazz, name, sig):
        env = self
        fun = self.functions[0]
        ret = fun.GetMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallObjectMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallObjectMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallBooleanMethod(self, obj, methodID, args=None) -> bool:  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallBooleanMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallByteMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallByteMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallCharMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallCharMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallShortMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallShortMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallIntMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallIntMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallLongMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallLongMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallFloatMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallFloatMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallDoubleMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallDoubleMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallVoidMethod(self, obj, methodID, args=None) -> None:  # (GIL ?)
        env = self
        fun = self.functions[0]
        fun.CallVoidMethodA(env, obj, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... nonvirtually

    def CallNonvirtualObjectMethod(self, obj, clazz, methodID, args=None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualObjectMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualBooleanMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualBooleanMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallNonvirtualByteMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualByteMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualCharMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualCharMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualShortMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualShortMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualIntMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualIntMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualLongMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualLongMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualFloatMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualFloatMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualDoubleMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualDoubleMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualVoidMethod(self, obj, clazz, methodID, args=None) -> None:
        env = self
        fun = self.functions[0]
        fun.CallNonvirtualVoidMethodA(env, obj, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java instance fields

    def GetFieldID(self, clazz, name, sig):
        env = self
        fun = self.functions[0]
        ret = fun.GetFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetBooleanField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetBooleanField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetByteField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetByteField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetCharField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetShortField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetIntField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetLongField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetFloatField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleField(self, obj, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetDoubleField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java instance fields

    def SetObjectField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetObjectField(env, obj, fieldID, JNIEnv.__itself_or_null(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetBooleanField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetByteField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetCharField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetShortField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetIntField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetLongField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetFloatField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleField(self, obj, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetDoubleField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Call Java static method

    def GetStaticMethodID(self, clazz, name, sig):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticObjectMethod(self, clazz: jclass, methodID: jmethodID, args: Pointer[jvalue] | None = None) -> jobject:
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticObjectMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticBooleanMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticBooleanMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallStaticByteMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticByteMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticCharMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticCharMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticShortMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticShortMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticIntMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticIntMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticLongMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticLongMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticFloatMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticFloatMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticDoubleMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticDoubleMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticVoidMethod(self, clazz, methodID, args=None) -> None:  # (GIL ?)
        env = self
        fun = self.functions[0]
        fun.CallStaticVoidMethodA(env, clazz, methodID, JNIEnv.__itself_or_null(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java static fields

    def GetStaticFieldID(self, clazz, name, sig):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticObjectField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticObjectField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticBooleanField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticBooleanField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetStaticByteField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticByteField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticCharField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticCharField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticShortField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticShortField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticIntField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticIntField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticLongField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticLongField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticFloatField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticFloatField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticDoubleField(self, clazz, fieldID):
        env = self
        fun = self.functions[0]
        ret = fun.GetStaticDoubleField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java static fields

    def SetStaticObjectField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticObjectField(env, clazz, fieldID, JNIEnv.__itself_or_null(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticBooleanField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticBooleanField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticByteField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticByteField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticCharField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticCharField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticShortField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticShortField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticIntField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticIntField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticLongField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticLongField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticFloatField(self, clazz, fieldID, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetStaticFloatField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticDoubleField(self, clazz, fieldID, value) -> None:
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
        return ret

    def GetStringLength(self, str: jstring) -> int:  # noqa: A002
        env = self
        fun = self.functions[0]
        ret: int = fun.GetStringLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringChars(self, str, isCopy=None):  # noqa: A002
        env = self
        fun = self.functions[0]
        ret: Pointer[jchar] = fun.GetStringChars(env, str, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringChars(self, str, chars):  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.ReleaseStringChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewStringUTF(self, utf: bytes) -> jstring:
        env = self
        fun = self.functions[0]
        ret = fun.NewStringUTF(env, utf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

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

    def GetStringUTFChars(self, str, isCopy=None):  # noqa: A002
        env = self
        fun = self.functions[0]
        ret = fun.GetStringUTFChars(env, str, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringUTFChars(self, str, chars) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.ReleaseStringUTFChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringRegion(self, str, start, len, buf) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.GetStringRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringUTFRegion(self, str, start, len, buf) -> None:  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.GetStringUTFRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetStringCritical(self, string, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetStringCritical(env, string, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringCritical(self, string, cstring) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseStringCritical(env, string, cstring)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java arrays handling

    def GetArrayLength(self, array: jarray) -> int:
        env = self
        fun = self.functions[0]
        ret = fun.GetArrayLength(env, array)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObjectArray(self, size, clazz, init=None):
        env = self
        fun = self.functions[0]
        ret = fun.NewObjectArray(env, size, clazz, JNIEnv.__itself_or_null(init))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectArrayElement(self, array: jobjectArray, index: jsize | int):
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectArrayElement(env, array, index)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def SetObjectArrayElement(self, array: jobjectArray, index: jsize | int, value) -> None:
        env = self
        fun = self.functions[0]
        fun.SetObjectArrayElement(env, array, index, JNIEnv.__itself_or_null(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewBooleanArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewBooleanArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewByteArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewByteArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewCharArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewCharArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewShortArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewShortArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewIntArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewIntArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewLongArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewLongArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewFloatArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewFloatArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewDoubleArray(self, size):
        env = self
        fun = self.functions[0]
        ret = fun.NewDoubleArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetBooleanArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetBooleanArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetByteArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetByteArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetCharArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetShortArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetIntArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetLongArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetFloatArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetDoubleArrayElements(env, array, JNIEnv.__byref_or_null(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseBooleanArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseBooleanArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseByteArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseByteArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseCharArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseCharArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseShortArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseShortArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseIntArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseIntArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseLongArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseLongArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseFloatArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseFloatArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseDoubleArrayElements(self, array, elems, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleaseDoubleArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetBooleanArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetByteArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetCharArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetShortArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetIntArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetLongArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetFloatArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetDoubleArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.GetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleArrayRegion(self, array, start, size, buf) -> None:
        env = self
        fun = self.functions[0]
        fun.SetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetPrimitiveArrayCritical(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetPrimitiveArrayCritical(env, array, JNIEnv.__byref_or_null(isCopy))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleasePrimitiveArrayCritical(self, array, carray, mode=0) -> None:
        env = self
        fun = self.functions[0]
        fun.ReleasePrimitiveArrayCritical(env, array, carray, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java native methods handling

    def RegisterNatives(self, clazz, methods, nMethods: jint | int):
        env = self
        fun = self.functions[0]
        # Required due to bug in jvm:
        # https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6493522
        fun.GetMethodID(env, clazz, b"notify", b"()V")
        ret = fun.RegisterNatives(env, clazz, methods, nMethods)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def UnregisterNatives(self, clazz):
        env = self
        fun = self.functions[0]
        ret = fun.UnregisterNatives(env, clazz)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java object monitoring

    def MonitorEnter(self, obj) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.MonitorEnter(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def MonitorExit(self, obj) -> int:
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
        return ret

    def GetDirectBufferAddress(self, buf: jobject) -> Pointer[ct.c_char]:
        env = self
        fun = self.functions[0]
        ret = fun.GetDirectBufferAddress(env, buf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferCapacity(self, buf: jobject) -> int:
        env = self
        fun = self.functions[0]
        ret: int = fun.GetDirectBufferCapacity(env, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java reflection support

    def FromReflectedMethod(self, method) -> jmethodID:
        env = self
        fun = self.functions[0]
        ret = fun.FromReflectedMethod(env, method)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FromReflectedField(self, field) -> jfieldID:
        env = self
        fun = self.functions[0]
        ret = fun.FromReflectedField(env, field)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedMethod(self, cls, methodID, isStatic: jboolean | bool):
        env = self
        fun = self.functions[0]
        ret = fun.ToReflectedMethod(env, cls, methodID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedField(self, cls, fieldID, isStatic: jboolean | bool):
        env = self
        fun = self.functions[0]
        ret = fun.ToReflectedField(env, cls, fieldID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

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
        return ret

    # Virtual threads

    def IsVirtualThread(self, obj: jobject) -> bool:
        # Since: JDK/JRE 19.0
        env = self
        fun = self.functions[0]
        ret = fun.IsVirtualThread(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

# tmap[JNIEnv] = ffi.typeof("JNIEnv")

def JEnv(penv: POINTER(JNIEnv)) -> JNIEnv:
    jenv = JNIEnv()
    jenv._JNIEnv__env = penv
    jenv.functions    = penv
    return jenv

#
# JNI Invocation Interface.
#

JNIInvokeInterface_ = cy.struct()

# JavaVM = cy.const(cy.pointer(JNIInvokeInterface_))
class JavaVM:

    __itself_or_null = itself_or_null

    def _handle_JNIException(self, err: int) -> None:
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def DestroyJavaVM(self) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.DestroyJavaVM(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThread(self, penv, args=None) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.AttachCurrentThread(jvm, penv, JavaVM.__itself_or_null(args))
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThreadAsDaemon(self, penv, args=None) -> None:
        jvm = self
        fun = self.functions[0]
        ret = fun.AttachCurrentThreadAsDaemon(jvm, penv, JavaVM.__itself_or_null(args))
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

# tmap[JavaVM] = ffi.typeof("JavaVM")

def JVM(pjvm: POINTER(JavaVM)) -> JavaVM:
    jvm = JavaVM()
    jvm._JavaVM__jvm = pjvm
    jvm.functions    = pjvm
    return jvm

# print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
from rich import print as print_  # noqa: E402
from . import jni as jni_  # noqa: E402
# print_(dir(jni_))
del print_, jni_
# print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")

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
JavaVMOption = cy.struct(
    optionString = cy.p_char,
    extraInfo    = cy.p_void,
)

JavaVMInitArgs = cy.struct(
    version            = jint,
    nOptions           = jint,
    options            = cy.pointer(JavaVMOption),
    ignoreUnrecognized = jboolean,
)

JavaVMAttachArgs = cy.struct(
    version =  jint,
    name    =  cy.p_char,
    group   =  jobject,
)

# These will be VM-specific.

JDK1_2: Final[int] = cy.const_int(1)
JDK1_4: Final[int] = cy.const_int(1)

# End VM-specific.

JNI_VERSION_1_1: Final[int] = cy.const_int(0x00010001)
JNI_VERSION_1_2: Final[int] = cy.const_int(0x00010002)
JNI_VERSION_1_4: Final[int] = cy.const_int(0x00010004)
JNI_VERSION_1_6: Final[int] = cy.const_int(0x00010006)
JNI_VERSION_1_8: Final[int] = cy.const_int(0x00010008)
JNI_VERSION_9:   Final[int] = cy.const_int(0x00090000)
JNI_VERSION_10:  Final[int] = cy.const_int(0x000a0000)
JNI_VERSION_19:  Final[int] = cy.const_int(0x00130000)
JNI_VERSION_20:  Final[int] = cy.const_int(0x00140000)
JNI_VERSION_21:  Final[int] = cy.const_int(0x00150000)
JNI_VERSION_24:  Final[int] = cy.const_int(0x00180000)

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

#
# Decorator for defining Java native method in Python
#

def method(signature: str, *,
           name: str | None = None) -> Callable[[Callable[P, R]], JNINativeMethod]:
    arg_types, res_type = __parse_signature(signature)
    fun_name = name.encode() if name is not None else None
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

del itself_or_null
del byref_or_null
del _jobject
del JNINativeInterface_
del JNIInvokeInterface_
