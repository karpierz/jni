# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
import platform
import ctypes as ct

if platform.win32_ver()[0]:
    from ctypes  import WinDLL      as DLL
    from _ctypes import FreeLibrary as dlclose
    from ctypes  import WINFUNCTYPE as CFUNC
else:
    from ctypes  import CDLL      as DLL
    from _ctypes import dlclose   as dlclose
    from ctypes  import CFUNCTYPE as CFUNC

from ctypes import POINTER
from ctypes import pointer
from ctypes import byref
from ctypes import addressof
from ctypes import cast
from ctypes import sizeof
from ctypes import py_object
from ctypes import memmove
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
jbooleanArray = jarray
jbyteArray    = jarray
jcharArray    = jarray
jshortArray   = jarray
jintArray     = jarray
jlongArray    = jarray
jfloatArray   = jarray
jdoubleArray  = jarray
jobjectArray  = jarray
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

jfieldID = ct.c_void_p

jmethodID = ct.c_void_p

# Return values from jobjectRefType

jobjectRefType = ct.c_int
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
isNULL = lambda jobj: not bool(jobj)

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
        fun = self.functions[0]
        jthr = fun.ExceptionOccurred(self)
        fun.ExceptionClear(self)
        jexc = fun.NewGlobalRef(self, jthr)
        fun.DeleteLocalRef(self, jthr)
        if Throwable.last:
            cause = Throwable.last.getCause()
            if cause: fun.DeleteGlobalRef(self, cause)
            Throwable.last = None
        fun.ExceptionClear(self)
        Throwable.last = thr = Throwable(jexc)#!!!, fname)
        raise thr

    # Java version

    def GetVersion(self):
        fun = self.functions[0]
        ret = fun.GetVersion(self)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Java class handling

    def DefineClass(self, name, loader, buf, blen):
        fun = self.functions[0]
        ret = fun.DefineClass(self, name, loader, buf, blen)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def FindClass(self, name):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.FindClass(self, name)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetSuperclass(self, sub):
        fun = self.functions[0]
        ret = fun.GetSuperclass(self, sub)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def IsAssignableFrom(self, sub, sup):
        fun = self.functions[0]
        return bool(fun.IsAssignableFrom(self, sub, sup))

    # Java exceptions handling

    def Throw(self, obj):
        fun = self.functions[0]
        ret = fun.Throw(self, obj)
        if ret != 0: self._handle_JNIException(ret)

    def ThrowNew(self, clazz, msg):
        fun = self.functions[0]
        ret = fun.ThrowNew(self, clazz, msg)
        if ret != 0: self._handle_JNIException(ret)

    def ExceptionOccurred(self):
        fun = self.functions[0]
        return fun.ExceptionOccurred(self)

    def ExceptionDescribe(self):
        fun = self.functions[0]
        fun.ExceptionDescribe(self)

    def ExceptionClear(self):
        fun = self.functions[0]
        if Throwable.last:
            cause = Throwable.last.getCause()
            if cause: fun.DeleteGlobalRef(self, cause)
            Throwable.last = None
        fun.ExceptionClear(self)

    def FatalError(self, msg):
        fun = self.functions[0]
        fun.FatalError(self, msg)

    def ExceptionCheck(self):
        fun = self.functions[0]
        return bool(fun.ExceptionCheck(self))

    # JVM Call frame

    def PushLocalFrame(self, capacity):
        fun = self.functions[0]
        ret = fun.PushLocalFrame(self, capacity)
        if ret != 0 and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def PopLocalFrame(self, result):
        fun = self.functions[0]
        return fun.PopLocalFrame(self, result)

    # Java references handling

    def NewGlobalRef(self, lobj):
        fun = self.functions[0]
        ret = fun.NewGlobalRef(self, lobj)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def DeleteGlobalRef(self, gref):
        fun = self.functions[0]
        if gref: fun.DeleteGlobalRef(self, gref)

    def NewLocalRef(self, ref):
        fun = self.functions[0]
        ret = fun.NewLocalRef(self, ref)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def DeleteLocalRef(self, obj):
        fun = self.functions[0]
        if obj: fun.DeleteLocalRef(self, obj)

    def NewWeakGlobalRef(self, obj):
        fun = self.functions[0]
        ret = fun.NewWeakGlobalRef(self, obj)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def DeleteWeakGlobalRef(self, ref):
        fun = self.functions[0]
        fun.DeleteWeakGlobalRef(self, ref)

    def EnsureLocalCapacity(self, capacity):
        fun = self.functions[0]
        ret = fun.EnsureLocalCapacity(self, capacity)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Java objects handling

    def AllocObject(self, clazz):
        fun = self.functions[0]
        ret = fun.AllocObject(self, clazz)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewObject(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.NewObjectA(self, clazz, methodID, args)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetObjectClass(self, obj):
        fun = self.functions[0]
        ret = fun.GetObjectClass(self, obj)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetObjectRefType(self, obj):
        # New in JNI 1.6
        fun = self.functions[0]
        ret = fun.GetObjectRefType(self, obj)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def IsInstanceOf(self, obj, clazz):
        fun = self.functions[0]
        return bool(fun.IsInstanceOf(self, obj, clazz))

    def IsSameObject(self, obj1, obj2):
        fun = self.functions[0]
        return bool(fun.IsSameObject(self, obj1, obj2))

    # Call Java instance method

    def GetMethodID(self, clazz, name, sig):
        fun = self.functions[0]
        ret = fun.GetMethodID(self, clazz, name, sig)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallObjectMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallObjectMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallBooleanMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallBooleanMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return bool(ret)

    def CallByteMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallByteMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallCharMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallCharMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallShortMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallShortMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallIntMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallIntMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallLongMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallLongMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallFloatMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallFloatMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallDoubleMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallDoubleMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallVoidMethod(self, obj, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        fun.CallVoidMethodA(self, obj, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # ... nonvirtually

    def CallNonvirtualObjectMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualObjectMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualBooleanMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualBooleanMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return bool(ret)

    def CallNonvirtualByteMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualByteMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualCharMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualCharMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualShortMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualShortMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualIntMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualIntMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualLongMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualLongMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualFloatMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualFloatMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualDoubleMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        ret = fun.CallNonvirtualDoubleMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallNonvirtualVoidMethod(self, obj, clazz, methodID, args=None):
        fun = self.functions[0]
        fun.CallNonvirtualVoidMethodA(self, obj, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # Getting Java instance fields

    def GetFieldID(self, clazz, name, sig):
        fun = self.functions[0]
        ret = fun.GetFieldID(self, clazz, name, sig)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetObjectField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetObjectField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetBooleanField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetBooleanField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return bool(ret)

    def GetByteField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetByteField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetCharField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetCharField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetShortField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetShortField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetIntField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetIntField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetLongField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetLongField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetFloatField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetFloatField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetDoubleField(self, obj, fieldID):
        fun = self.functions[0]
        ret = fun.GetDoubleField(self, obj, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Setting Java instance fields

    def SetObjectField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetObjectField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetBooleanField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetBooleanField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetByteField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetByteField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetCharField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetCharField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetShortField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetShortField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetIntField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetIntField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetLongField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetLongField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetFloatField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetFloatField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetDoubleField(self, obj, fieldID, value):
        fun = self.functions[0]
        fun.SetDoubleField(self, obj, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # Call Java static method

    def GetStaticMethodID(self, clazz, name, sig):
        fun = self.functions[0]
        ret = fun.GetStaticMethodID(self, clazz, name, sig)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticObjectMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticObjectMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticBooleanMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticBooleanMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return bool(ret)

    def CallStaticByteMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticByteMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticCharMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticCharMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticShortMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticShortMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticIntMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticIntMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticLongMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticLongMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticFloatMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticFloatMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticDoubleMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        ret = fun.CallStaticDoubleMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def CallStaticVoidMethod(self, clazz, methodID, args=None):  # (GIL ?)
        fun = self.functions[0]
        fun.CallStaticVoidMethodA(self, clazz, methodID, args)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # Getting Java static fields

    def GetStaticFieldID(self, clazz, name, sig):
        fun = self.functions[0]
        ret = fun.GetStaticFieldID(self, clazz, name, sig)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticObjectField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticObjectField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticBooleanField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticBooleanField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return bool(ret)

    def GetStaticByteField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticByteField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticCharField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticCharField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticShortField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticShortField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticIntField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticIntField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticLongField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticLongField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticFloatField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticFloatField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStaticDoubleField(self, clazz, fieldID):
        fun = self.functions[0]
        ret = fun.GetStaticDoubleField(self, clazz, fieldID)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Setting Java static fields

    def SetStaticObjectField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticObjectField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticBooleanField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticBooleanField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticByteField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticByteField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticCharField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticCharField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticShortField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticShortField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticIntField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticIntField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticLongField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticLongField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticFloatField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticFloatField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetStaticDoubleField(self, clazz, fieldID, value):
        fun = self.functions[0]
        fun.SetStaticDoubleField(self, clazz, fieldID, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # Java strings handling

    def NewString(self, unicode, slen):
        fun = self.functions[0]
        ret = fun.NewString(self, unicode, slen)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStringLength(self, str):
        fun = self.functions[0]
        ret = fun.GetStringLength(self, str)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStringChars(self, str, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetStringChars(self, str, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ReleaseStringChars(self, str, chars):
        fun = self.functions[0]
        fun.ReleaseStringChars(self, str, chars)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def NewStringUTF(self, utf):
        fun = self.functions[0]
        ret = fun.NewStringUTF(self, utf)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStringUTFLength(self, str):
        fun = self.functions[0]
        ret = fun.GetStringUTFLength(self, str)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetStringUTFChars(self, str, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetStringUTFChars(self, str, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ReleaseStringUTFChars(self, str, chars):
        fun = self.functions[0]
        fun.ReleaseStringUTFChars(self, str, chars)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetStringRegion(self, str, start, len, buf):
        fun = self.functions[0]
        fun.GetStringRegion(self, str, start, len, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetStringUTFRegion(self, str, start, len, buf):
        fun = self.functions[0]
        fun.GetStringUTFRegion(self, str, start, len, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # ... in a critical manner

    def GetStringCritical(self, string, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetStringCritical(self, string, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ReleaseStringCritical(self, string, cstring):
        fun = self.functions[0]
        fun.ReleaseStringCritical(self, string, cstring)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # Java arrays handling

    def GetArrayLength(self, array):
        fun = self.functions[0]
        ret = fun.GetArrayLength(self, array)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewObjectArray(self, size, clazz, init=None):
        fun = self.functions[0]
        ret = fun.NewObjectArray(self, size, clazz, init)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetObjectArrayElement(self, array, index):
        fun = self.functions[0]
        ret = fun.GetObjectArrayElement(self, array, index)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def SetObjectArrayElement(self, array, index, value):
        fun = self.functions[0]
        fun.SetObjectArrayElement(self, array, index, value)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def NewBooleanArray(self, size):
        fun = self.functions[0]
        ret = fun.NewBooleanArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewByteArray(self, size):
        fun = self.functions[0]
        ret = fun.NewByteArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewCharArray(self, size):
        fun = self.functions[0]
        ret = fun.NewCharArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewShortArray(self, size):
        fun = self.functions[0]
        ret = fun.NewShortArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewIntArray(self, size):
        fun = self.functions[0]
        ret = fun.NewIntArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewLongArray(self, size):
        fun = self.functions[0]
        ret = fun.NewLongArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewFloatArray(self, size):
        fun = self.functions[0]
        ret = fun.NewFloatArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def NewDoubleArray(self, size):
        fun = self.functions[0]
        ret = fun.NewDoubleArray(self, size)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetBooleanArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetBooleanArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetByteArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetByteArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetCharArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetCharArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetShortArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetShortArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetIntArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetIntArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetLongArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetLongArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetFloatArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetFloatArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetDoubleArrayElements(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetDoubleArrayElements(self, array, isCopy)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ReleaseBooleanArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseBooleanArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseByteArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseByteArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseCharArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseCharArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseShortArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseShortArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseIntArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseIntArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseLongArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseLongArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseFloatArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseFloatArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def ReleaseDoubleArrayElements(self, array, elems, mode=0):
        fun = self.functions[0]
        fun.ReleaseDoubleArrayElements(self, array, elems, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetBooleanArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetBooleanArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetByteArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetByteArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetCharArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetCharArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetShortArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetShortArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetIntArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetIntArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetLongArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetLongArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetFloatArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetFloatArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def GetDoubleArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.GetDoubleArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetBooleanArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetBooleanArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetByteArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetByteArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetCharArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetCharArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetShortArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetShortArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetIntArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetIntArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetLongArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetLongArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetFloatArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetFloatArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    def SetDoubleArrayRegion(self, array, start, size, buf):
        fun = self.functions[0]
        fun.SetDoubleArrayRegion(self, array, start, size, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # ... in a critical manner

    def GetPrimitiveArrayCritical(self, array, isCopy=None):
        fun = self.functions[0]
        ret = fun.GetPrimitiveArrayCritical(self, array, isCopy)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ReleasePrimitiveArrayCritical(self, array, carray, mode=0):
        fun = self.functions[0]
        fun.ReleasePrimitiveArrayCritical(self, array, carray, mode)
        if fun.ExceptionCheck(self): self._handle_JavaException()

    # Java native methods handling

    def RegisterNatives(self, clazz, methods, nMethods):
        fun = self.functions[0]
        # Required due to bug in jvm:
        # https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6493522
        fun.GetMethodID(self, clazz, b"notify", b"()V")
        ret = fun.RegisterNatives(self, clazz, methods, nMethods)
        if ret != 0 and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def UnregisterNatives(self, clazz):
        fun = self.functions[0]
        ret = fun.UnregisterNatives(self, clazz)
        if ret != 0 and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Java object monitoring

    def MonitorEnter(self, obj):
        fun = self.functions[0]
        ret = fun.MonitorEnter(self, obj)
        if ret != 0 and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def MonitorExit(self, obj):
        fun = self.functions[0]
        ret = fun.MonitorExit(self, obj)
        if ret != 0 and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Java direct buffer handling

    def NewDirectByteBuffer(self, address, capacity):
        fun = self.functions[0]
        ret = fun.NewDirectByteBuffer(self, address, capacity)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetDirectBufferAddress(self, buf):
        fun = self.functions[0]
        ret = fun.GetDirectBufferAddress(self, buf)
        if not ret and fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def GetDirectBufferCapacity(self, buf):
        fun = self.functions[0]
        ret = fun.GetDirectBufferCapacity(self, buf)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Java reflection support

    def FromReflectedMethod(self, method):
        fun = self.functions[0]
        ret = fun.FromReflectedMethod(self, method)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def FromReflectedField(self, field):
        fun = self.functions[0]
        ret = fun.FromReflectedField(self, field)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ToReflectedMethod(self, cls, methodID, isStatic):
        fun = self.functions[0]
        ret = fun.ToReflectedMethod(self, cls, methodID, isStatic)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    def ToReflectedField(self, cls, fieldID, isStatic):
        fun = self.functions[0]
        ret = fun.ToReflectedField(self, cls, fieldID, isStatic)
        if fun.ExceptionCheck(self): self._handle_JavaException()
        return ret

    # Java VM Interface

    def GetJavaVM(self, vm):
        fun = self.functions[0]
        ret = fun.GetJavaVM(self, vm)
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
        fun = self.functions[0]
        ret = fun.DestroyJavaVM(self)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThread(self, penv, args=None):
        fun = self.functions[0]
        ret = fun.AttachCurrentThread(self, penv, args)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThreadAsDaemon(self, penv, args=None):
        fun = self.functions[0]
        ret = fun.AttachCurrentThreadAsDaemon(self, penv, args)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def DetachCurrentThread(self):
        fun = self.functions[0]
        ret = fun.DetachCurrentThread(self)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def GetEnv(self, penv, version):
        fun = self.functions[0]
        ret = fun.GetEnv(self, penv, version)
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

# eof jni.h

class Throwable(Exception):

    last = None

    def __init__(self, cause=NULL, info=NULL):
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

    def __init__(self, error=JNI_ERR, info=None):
        self._error = error
        self._info  = info
        super().__init__(self.getMessage(), self.getError())

    def getMessage(self):
        prefix = self._info + ": " if self._info else ""
        return prefix + JNIException.reason.get(self._error,
                                                "unknown error code {0}".format(self._error))

    def getError(self):
        return self._error

def load(dll_path, handle=None, __dlclose=dlclose):

    try:
        dll = DLL(dll_path, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError("{}".format(exc)) from None

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
                               fnPtr=cast(FunProto(fun), jobject)) # ct.c_void_p
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
