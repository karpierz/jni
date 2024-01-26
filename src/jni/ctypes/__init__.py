# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
import os
import platform
import ctypes as ct

if platform.win32_ver()[0]:
    from ctypes  import WinDLL as DLL  # noqa: N814
    try:
        from _ctypes import FreeLibrary as dlclose  # noqa: N813
    except ImportError:  # pragma: no cover
        dlclose = lambda handle: 0
    from ctypes  import WINFUNCTYPE as CFUNC
else:
    from ctypes  import CDLL      as DLL      # noqa: N814
    from _ctypes import dlclose   as dlclose  # noqa: N813
    from ctypes  import CFUNCTYPE as CFUNC

from ctypes import POINTER
from ctypes import pointer
from ctypes import byref      # noqa: F401
from ctypes import addressof  # noqa: F401
from ctypes import sizeof     # noqa: F401
from ctypes import py_object  # noqa: F401
from ctypes import memmove    # noqa: F401
from ctypes import cast
__none = object()
obj         = lambda type, init=__none: type() if init is __none else type(init)
new         = lambda type, init=__none: pointer(type() if init is __none else type(init))
new_array   = lambda type, size: (type * size)()
new_cstr    = lambda init, __ct=ct: __ct.cast(__ct.create_string_buffer(init), __ct.c_char_p)
as_cstr     = lambda obj,  __ct=ct: __ct.c_char_p(obj)
to_bytes    = lambda obj, size=-1, __ct=ct: __ct.string_at(obj, size=size)
to_unicode  = lambda obj, size=-1, __ct=ct: __ct.wstring_at(obj, size=size)
from_buffer = lambda data, __ct=ct: __ct.cast((__ct.c_char * 0).from_buffer(data), __ct.POINTER(__ct.c_char))

def defined(varname, __getframe=sys._getframe):
    frame = __getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

def from_oid(oid, __cast=ct.cast, __py_object=ct.py_object):
    return __cast(oid, __py_object).value if oid else None


# Notes:
#   if (GIL ?) should be use: with JHost.ThreadState():

#
# JNI Types
#

jint     = ct.c_int32
jlong    = ct.c_int64
jbyte    = ct.c_int8

jboolean = ct.c_ubyte
jchar    = ct.c_wchar
jshort   = ct.c_int16
jfloat   = ct.c_float
jdouble  = ct.c_double
jsize    = jint

jobject       = ct.c_void_p
jclass        = jobject
jthrowable    = jobject
jstring       = jobject
jarray        = jobject
jbooleanArray = jarray  # noqa: N816
jbyteArray    = jarray  # noqa: N816
jcharArray    = jarray  # noqa: N816
jshortArray   = jarray  # noqa: N816
jintArray     = jarray  # noqa: N816
jlongArray    = jarray  # noqa: N816
jfloatArray   = jarray  # noqa: N816
jdoubleArray  = jarray  # noqa: N816
jobjectArray  = jarray  # noqa: N816
jweak         = jobject

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


if platform.system().lower() == "cli":
    _jvalue = jvalue

    class jvalue(ct.Structure):
        _anonymous_ = ("u",)
        _fields_    = [("u", _jvalue)]

    del _jvalue

jfieldID = ct.c_void_p  # noqa: N816

jmethodID = ct.c_void_p  # noqa: N816

# Return values from jobjectRefType

jobjectRefType = ct.c_int  # noqa: N816
(
    JNIInvalidRefType,
    JNILocalRefType,
    JNIGlobalRefType,
    JNIWeakGlobalRefType
) = (0, 1, 2, 3)

#
# jboolean constants
#

JNI_FALSE = 0
JNI_TRUE  = 1

#
# null constant
#

NULL   = obj(jobject, 0)
isNULL = lambda jobj: not bool(jobj)  # noqa: N816

#
# possible return values for JNI functions.
#

JNI_OK        =  0  # success
JNI_ERR       = -1  # unknown error
JNI_EDETACHED = -2  # thread detached from the VM
JNI_EVERSION  = -3  # JNI version error
JNI_ENOMEM    = -4  # not enough memory
JNI_EEXIST    = -5  # VM already created
JNI_EINVAL    = -6  # invalid arguments

#
# used in ReleaseScalarArrayElements
#

JNI_COMMIT = 1
JNI_ABORT  = 2

#
# JNI Native Method Interface.
#

# used in RegisterNatives to describe native method name,
# signature, and function pointer.

class JNINativeMethod(ct.Structure):
    _fields_ = [
    ("name",      ct.c_char_p),
    ("signature", ct.c_char_p),
    ("fnPtr",     ct.c_void_p)
]

class JNINativeInterface_(ct.Structure): pass

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

    def _handle_JNIException(self, err):
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def _handle_JavaException(self):
        env = self
        fun = self.functions[0]
        jthr = fun.ExceptionOccurred(env)
        fun.ExceptionClear(env)
        jexc = fun.NewGlobalRef(env, jthr)
        fun.DeleteLocalRef(env, jthr)
        if Throwable.last:
            cause = Throwable.last.getCause()
            if cause: fun.DeleteGlobalRef(env, cause)
            Throwable.last = None
        fun.ExceptionClear(env)
        Throwable.last = thr = Throwable(jexc)  # !!!, fname)
        raise thr

    # Java version

    def GetVersion(self):
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

    def FindClass(self, name):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.FindClass(env, name)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetSuperclass(self, sub):
        env = self
        fun = self.functions[0]
        ret = fun.GetSuperclass(env, sub)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def IsAssignableFrom(self, sub, sup):
        env = self
        fun = self.functions[0]
        return bool(fun.IsAssignableFrom(env, sub, sup))

    # Java exceptions handling

    def Throw(self, obj):
        env = self
        fun = self.functions[0]
        ret = fun.Throw(env, obj)
        if ret != 0: self._handle_JNIException(ret)

    def ThrowNew(self, clazz, msg):
        env = self
        fun = self.functions[0]
        ret = fun.ThrowNew(env, clazz, msg)
        if ret != 0: self._handle_JNIException(ret)

    def ExceptionOccurred(self):
        env = self
        fun = self.functions[0]
        return fun.ExceptionOccurred(env)

    def ExceptionDescribe(self):
        env = self
        fun = self.functions[0]
        fun.ExceptionDescribe(env)

    def ExceptionClear(self):
        env = self
        fun = self.functions[0]
        if Throwable.last:
            cause = Throwable.last.getCause()
            if cause: fun.DeleteGlobalRef(env, cause)
            Throwable.last = None
        fun.ExceptionClear(env)

    def FatalError(self, msg):
        env = self
        fun = self.functions[0]
        fun.FatalError(env, msg)

    def ExceptionCheck(self):
        env = self
        fun = self.functions[0]
        return bool(fun.ExceptionCheck(env))

    # JVM Call frame

    def PushLocalFrame(self, capacity):
        env = self
        fun = self.functions[0]
        ret = fun.PushLocalFrame(env, capacity)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def PopLocalFrame(self, result):
        env = self
        fun = self.functions[0]
        return fun.PopLocalFrame(env, result)

    # Java references handling

    def NewGlobalRef(self, lobj):
        env = self
        fun = self.functions[0]
        ret = fun.NewGlobalRef(env, lobj)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteGlobalRef(self, gref):
        env = self
        fun = self.functions[0]
        if gref: fun.DeleteGlobalRef(env, gref)

    def NewLocalRef(self, ref):
        env = self
        fun = self.functions[0]
        ret = fun.NewLocalRef(env, ref)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteLocalRef(self, obj):
        env = self
        fun = self.functions[0]
        if obj: fun.DeleteLocalRef(env, obj)

    def NewWeakGlobalRef(self, obj):
        env = self
        fun = self.functions[0]
        ret = fun.NewWeakGlobalRef(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteWeakGlobalRef(self, ref):
        env = self
        fun = self.functions[0]
        fun.DeleteWeakGlobalRef(env, ref)

    def EnsureLocalCapacity(self, capacity):
        env = self
        fun = self.functions[0]
        ret = fun.EnsureLocalCapacity(env, capacity)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java objects handling

    def AllocObject(self, clazz):
        env = self
        fun = self.functions[0]
        ret = fun.AllocObject(env, clazz)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObject(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.NewObjectA(env, clazz, methodID, args)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectClass(self, obj):
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectClass(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectRefType(self, obj):
        # New in JNI 1.6
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectRefType(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def IsInstanceOf(self, obj, clazz):
        env = self
        fun = self.functions[0]
        return bool(fun.IsInstanceOf(env, obj, clazz))

    def IsSameObject(self, obj1, obj2):
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
        ret = fun.CallObjectMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallBooleanMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallBooleanMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallByteMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallByteMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallCharMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallCharMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallShortMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallShortMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallIntMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallIntMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallLongMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallLongMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallFloatMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallFloatMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallDoubleMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallDoubleMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallVoidMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        fun.CallVoidMethodA(env, obj, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... nonvirtually

    def CallNonvirtualObjectMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualObjectMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualBooleanMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualBooleanMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallNonvirtualByteMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualByteMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualCharMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualCharMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualShortMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualShortMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualIntMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualIntMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualLongMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualLongMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualFloatMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualFloatMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualDoubleMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        ret = fun.CallNonvirtualDoubleMethodA(env, obj, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualVoidMethod(self, obj, clazz, methodID, args=None):
        env = self
        fun = self.functions[0]
        fun.CallNonvirtualVoidMethodA(env, obj, clazz, methodID, args)
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

    def SetObjectField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetObjectField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetBooleanField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetByteField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetCharField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetShortField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetIntField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetLongField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatField(self, obj, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetFloatField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleField(self, obj, fieldID, value):
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

    def CallStaticObjectMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticObjectMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticBooleanMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticBooleanMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallStaticByteMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticByteMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticCharMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticCharMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticShortMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticShortMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticIntMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticIntMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticLongMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticLongMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticFloatMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticFloatMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticDoubleMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        ret = fun.CallStaticDoubleMethodA(env, clazz, methodID, args)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticVoidMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self
        fun = self.functions[0]
        fun.CallStaticVoidMethodA(env, clazz, methodID, args)
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

    def SetStaticObjectField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticObjectField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticBooleanField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticBooleanField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticByteField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticByteField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticCharField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticCharField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticShortField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticShortField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticIntField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticIntField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticLongField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticLongField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticFloatField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticFloatField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticDoubleField(self, clazz, fieldID, value):
        env = self
        fun = self.functions[0]
        fun.SetStaticDoubleField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java strings handling

    def NewString(self, unicode, slen):
        env = self
        fun = self.functions[0]
        ret = fun.NewString(env, unicode, slen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringLength(self, str):  # noqa: A002
        env = self
        fun = self.functions[0]
        ret = fun.GetStringLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringChars(self, str, isCopy=None):  # noqa: A002
        env = self
        fun = self.functions[0]
        ret = fun.GetStringChars(env, str, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringChars(self, str, chars):  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.ReleaseStringChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewStringUTF(self, utf):
        env = self
        fun = self.functions[0]
        ret = fun.NewStringUTF(env, utf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFLength(self, str):  # noqa: A002
        env = self
        fun = self.functions[0]
        ret = fun.GetStringUTFLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFChars(self, str, isCopy=None):  # noqa: A002
        env = self
        fun = self.functions[0]
        ret = fun.GetStringUTFChars(env, str, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringUTFChars(self, str, chars):  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.ReleaseStringUTFChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringRegion(self, str, start, len, buf):  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.GetStringRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringUTFRegion(self, str, start, len, buf):  # noqa: A002
        env = self
        fun = self.functions[0]
        fun.GetStringUTFRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetStringCritical(self, string, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetStringCritical(env, string, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringCritical(self, string, cstring):
        env = self
        fun = self.functions[0]
        fun.ReleaseStringCritical(env, string, cstring)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java arrays handling

    def GetArrayLength(self, array):
        env = self
        fun = self.functions[0]
        ret = fun.GetArrayLength(env, array)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObjectArray(self, size, clazz, init=None):
        env = self
        fun = self.functions[0]
        ret = fun.NewObjectArray(env, size, clazz, init)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectArrayElement(self, array, index):
        env = self
        fun = self.functions[0]
        ret = fun.GetObjectArrayElement(env, array, index)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def SetObjectArrayElement(self, array, index, value):
        env = self
        fun = self.functions[0]
        fun.SetObjectArrayElement(env, array, index, value)
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
        ret = fun.GetBooleanArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetByteArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetByteArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetCharArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetShortArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetIntArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetLongArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetFloatArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleArrayElements(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetDoubleArrayElements(env, array, isCopy)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseBooleanArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseBooleanArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseByteArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseByteArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseCharArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseCharArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseShortArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseShortArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseIntArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseIntArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseLongArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseLongArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseFloatArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseFloatArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseDoubleArrayElements(self, array, elems, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleaseDoubleArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetBooleanArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetByteArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetCharArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetShortArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetIntArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetLongArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetFloatArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetDoubleArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.GetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleArrayRegion(self, array, start, size, buf):
        env = self
        fun = self.functions[0]
        fun.SetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetPrimitiveArrayCritical(self, array, isCopy=None):
        env = self
        fun = self.functions[0]
        ret = fun.GetPrimitiveArrayCritical(env, array, isCopy)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleasePrimitiveArrayCritical(self, array, carray, mode=0):
        env = self
        fun = self.functions[0]
        fun.ReleasePrimitiveArrayCritical(env, array, carray, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java native methods handling

    def RegisterNatives(self, clazz, methods, nMethods):
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

    def MonitorEnter(self, obj):
        env = self
        fun = self.functions[0]
        ret = fun.MonitorEnter(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def MonitorExit(self, obj):
        env = self
        fun = self.functions[0]
        ret = fun.MonitorExit(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java direct buffer handling

    def NewDirectByteBuffer(self, address, capacity):
        env = self
        fun = self.functions[0]
        ret = fun.NewDirectByteBuffer(env, address, capacity)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferAddress(self, buf):
        env = self
        fun = self.functions[0]
        ret = fun.GetDirectBufferAddress(env, buf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferCapacity(self, buf):
        env = self
        fun = self.functions[0]
        ret = fun.GetDirectBufferCapacity(env, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java reflection support

    def FromReflectedMethod(self, method):
        env = self
        fun = self.functions[0]
        ret = fun.FromReflectedMethod(env, method)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FromReflectedField(self, field):
        env = self
        fun = self.functions[0]
        ret = fun.FromReflectedField(env, field)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedMethod(self, cls, methodID, isStatic):
        env = self
        fun = self.functions[0]
        ret = fun.ToReflectedMethod(env, cls, methodID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedField(self, cls, fieldID, isStatic):
        env = self
        fun = self.functions[0]
        ret = fun.ToReflectedField(env, cls, fieldID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java VM Interface

    def GetJavaVM(self, vm):
        env = self
        fun = self.functions[0]
        ret = fun.GetJavaVM(env, vm)
        if ret != 0: self._handle_JNIException(ret)


JEnv = lambda penv: penv[0]

#
# JNI Invocation Interface.
#

class JNIInvokeInterface_(ct.Structure): pass

class JavaVM(ct.Structure):
    _fields_ = [("functions", POINTER(JNIInvokeInterface_))]

    def _handle_JNIException(self, err):
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def DestroyJavaVM(self):
        jvm = self
        fun = self.functions[0]
        ret = fun.DestroyJavaVM(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThread(self, penv, args=None):
        jvm = self
        fun = self.functions[0]
        ret = fun.AttachCurrentThread(jvm, penv, args)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThreadAsDaemon(self, penv, args=None):
        jvm = self
        fun = self.functions[0]
        ret = fun.AttachCurrentThreadAsDaemon(jvm, penv, args)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def DetachCurrentThread(self):
        jvm = self
        fun = self.functions[0]
        ret = fun.DetachCurrentThread(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def GetEnv(self, penv, version):
        jvm = self
        fun = self.functions[0]
        ret = fun.GetEnv(jvm, penv, version)
        if ret != JNI_OK: self._handle_JNIException(ret)


JVM = lambda pjvm: pjvm[0]

# JNI Native Method Interface.

# temporary
va_list = ct.c_void_p

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
]

del JNINativeInterface_
del va_list

# JNI Invocation Interface.

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

JDK1_2 = 1
JDK1_4 = 1

# End VM-specific.

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

JNI_VERSION_1_1 = 0x00010001
JNI_VERSION_1_2 = 0x00010002
JNI_VERSION_1_4 = 0x00010004
JNI_VERSION_1_6 = 0x00010006
JNI_VERSION_1_8 = 0x00010008
JNI_VERSION_9   = 0x00090000
JNI_VERSION_10  = 0x000a0000
JNI_VERSION_19  = 0x00130000
JNI_VERSION_20  = 0x00140000
JNI_VERSION_21  = 0x00150000

# eof jni.h

class Throwable(Exception):  # noqa: N818

    last = None

    def __init__(self, cause=NULL, info=NULL):  # noqa: D107
        self._cause = cast(cause, jthrowable)
        self._info  = cast(info,  jstring)
        super().__init__(self._cause, self._info)

    def getCause(self):
        return self._cause

    def getInfo(self):
        return self._info

class JNIException(SystemError):

    reason = {
        JNI_OK:        "success",
        JNI_ERR:       "unknown error",
        JNI_EDETACHED: "thread detached from the VM",
        JNI_EVERSION:  "JNI version error",
        JNI_ENOMEM:    "not enough memory",
        JNI_EEXIST:    "VM already created",
        JNI_EINVAL:    "invalid arguments",
    }

    def __init__(self, error=JNI_ERR, info=None):  # noqa: D107
        self._error = error
        self._info  = info
        super().__init__(self.getMessage(), self.getError())

    def getMessage(self):
        prefix = self._info + ": " if self._info else ""
        return prefix + JNIException.reason.get(self._error,
                                                f"unknown error code {self._error}")

    def getError(self):
        return self._error

def load(dll_path, handle=None, __dlclose=dlclose):

    try:
        if isinstance(dll_path, os.PathLike): dll_path = str(dll_path)
        dll = DLL(dll_path, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError(f"{exc}") from None

    def proto(restype, func, *argtypes):
        func.restype  = restype
        func.argtypes = argtypes
        return func

    JNI = type("JNI", (), dict(dll=dll, dllclose=classmethod(lambda cls, __dlclose=__dlclose: __dlclose(cls.dll._handle))))
    JNI.GetDefaultJavaVMInitArgs = proto(jint, dll.JNI_GetDefaultJavaVMInitArgs, POINTER(JavaVMInitArgs))
    JNI.CreateJavaVM             = proto(jint, dll.JNI_CreateJavaVM,             POINTER(POINTER(JavaVM)), POINTER(POINTER(JNIEnv)), POINTER(JavaVMInitArgs))
    JNI.GetCreatedJavaVMs        = proto(jint, dll.JNI_GetCreatedJavaVMs,        POINTER(POINTER(JavaVM)), jsize, POINTER(jsize))

    return JNI

#
# Decorator for defining Java native method in Python
#

def method(signature, **kwargs):
    ret_type, arg_types = __parse_signature(signature)
    fun_name = kwargs["name"].encode("utf-8") if "name" in kwargs else None
    fun_sign = signature.encode("utf-8")
    FunProto = CFUNC(ret_type, POINTER(JNIEnv), jobject, *arg_types)

    def wrapper(fun):
        return JNINativeMethod(name=fun_name or fun.__name__.encode("utf-8"),
                               signature=fun_sign,
                               fnPtr=cast(FunProto(fun), jobject))  # ct.c_void_p
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
del platform
del ct
del dlclose
