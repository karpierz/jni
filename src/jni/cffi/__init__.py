# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import sys
import os
import platform
import ctypes as ct

from .jni import ffi ; del jni

DLL     = lambda name, handle=None, __ffi=ffi: __ffi.dlopen(name)
dlclose = lambda handle,            __ffi=ffi: __ffi.dlclose(handle)

def CFUNC(restype, *argtypes, __ffi=ffi):
    callback_sign = ((restype.cname if restype is not None else "void") + " __stdcall" +
                     " (" + ", ".join(arg_type.cname for arg_type in argtypes) + ")")
    return __ffi.callback(callback_sign)

tmap = {}
__none = object()

POINTER   = lambda type, __tmap=tmap, __ffi=ffi: __ffi.typeof(__ffi.getctype(__tmap.get(type, type))+"*")
pointer   = lambda obj,               __ffi=ffi: __ffi.new(POINTER(__ffi.typeof(obj)), obj)
byref     = lambda obj, offset=0,     __ffi=ffi: __ffi.new(POINTER(__ffi.typeof(obj)), obj) # !!! zamplementowac offset !!!
addressof = lambda obj,               __ffi=ffi: __ffi.addressof(obj)
cast      = lambda obj, type,         __ffi=ffi: __ffi.cast(type, obj)
sizeof    = lambda obj_or_type,       __ffi=ffi: __ffi.sizeof(obj_or_type)
py_object = lambda obj,               __ffi=ffi: __ffi.new_handle(obj)
memmove   = lambda dst, src, count,   __ffi=ffi: __ffi.memmove(dst, src, count)
obj       = lambda type, init=__none, __ffi=ffi:(__ffi.new(__ffi.getctype(type)+"*", None if init is __none else init)[0]
                                                 if type.kind != "primitive" else
                                                 __ffi.cast(type, 0 if init is __none else init))
new         = lambda type, init=__none, __ffi=ffi: __ffi.new(__ffi.getctype(type)+"*", None if init is __none else init)
new_array   = lambda type, size,        __ffi=ffi: __ffi.new(__ffi.getctype(type)+"[]", size)
new_cstr    = lambda init,              __ffi=ffi: __ffi.new("char[]", init)
as_cstr     = lambda obj,               __ffi=ffi: __ffi.cast("char*", __ffi.from_buffer(obj))
to_bytes    = lambda obj, size=-1,      __ffi=ffi: __ffi.string(obj, size) if size >= 0 else __ffi.string(obj)
to_unicode  = to_bytes
from_buffer = lambda data,              __ffi=ffi: __ffi.from_buffer(data)

_itself_or_NULL = lambda arg, __NULL=ffi.NULL: __NULL if arg is None else arg
_byref_or_NULL  = lambda arg, __NULL=ffi.NULL: __NULL if arg is None else byref(arg)

class _CData(ct.Structure):
    _fields_ = ( # PyObject_HEAD
    ("ob_refcnt",     ct.c_ssize_t),
    ("ob_type",       ct.c_void_p),
    # _CData body
    ("c_type",        ct.py_object), # CTypeDescrObject*
    ("c_data",        ct.c_void_p),  # char*
    ("c_weakreflist", ct.py_object), # PyObject*
)

_as_CData = lambda obj, __ct=ct: __ct.cast(id(obj), __ct.POINTER(_CData))[0]

def defined(varname, __getframe=sys._getframe):
    frame = __getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

def from_oid(oid, __cast=ct.cast, __py_object=ct.py_object):
    return __cast(oid, __py_object).value if oid else None

#
# JNI Types
#

jint     = ffi.typeof("jint")
jlong    = ffi.typeof("jlong")
jbyte    = ffi.typeof("jbyte")

jboolean = ffi.typeof("jboolean")
jchar    = ffi.typeof("jchar")
jshort   = ffi.typeof("jshort")
jfloat   = ffi.typeof("jfloat")
jdouble  = ffi.typeof("jdouble")
jsize    = ffi.typeof("jsize")

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

jvalue = ffi.typeof("jvalue")

jfieldID = ffi.typeof("jfieldID")

jmethodID = ffi.typeof("jmethodID")

# Return values from jobjectRefType

jobjectRefType = ffi.typeof("jobjectRefType")
JNIInvalidRefType    = jobjectRefType.relements["JNIInvalidRefType"]
JNILocalRefType      = jobjectRefType.relements["JNILocalRefType"]
JNIGlobalRefType     = jobjectRefType.relements["JNIGlobalRefType"]
JNIWeakGlobalRefType = jobjectRefType.relements["JNIWeakGlobalRefType"]

#
# jboolean constants
#

JNI_FALSE = ffi.integer_const("JNI_FALSE")
JNI_TRUE  = ffi.integer_const("JNI_TRUE")

#
# null constant
#

NULL   = ffi.NULL
isNULL = lambda jobj, __NULL=NULL: jobj == __NULL

#
# possible return values for JNI functions.
#

JNI_OK        = ffi.integer_const("JNI_OK")         # success
JNI_ERR       = ffi.integer_const("JNI_ERR")        # unknown error
JNI_EDETACHED = ffi.integer_const("JNI_EDETACHED")  # thread detached from the VM
JNI_EVERSION  = ffi.integer_const("JNI_EVERSION")   # JNI version error
JNI_ENOMEM    = ffi.integer_const("JNI_ENOMEM")     # not enough memory
JNI_EEXIST    = ffi.integer_const("JNI_EEXIST")     # VM already created
JNI_EINVAL    = ffi.integer_const("JNI_EINVAL")     # invalid arguments

#
# used in ReleaseScalarArrayElements
#

JNI_COMMIT = ffi.integer_const("JNI_COMMIT")
JNI_ABORT  = ffi.integer_const("JNI_ABORT")

#
# JNI Native Method Interface.
#

# used in RegisterNatives to describe native method name,
# signature, and function pointer.

JNINativeMethod = ffi.typeof("JNINativeMethod")

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

    def _handle_JNIException(self, err):
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def _handle_JavaException(self):
        env = self.__env
        fun = env[0]
        jthr = fun.ExceptionOccurred(env)
        fun.ExceptionClear(env)
        jexc = fun.NewGlobalRef(env, jthr)
        fun.DeleteLocalRef(env, jthr)
        if Throwable.last:
            cause = Throwable.last.getCause()
            if cause: fun.DeleteGlobalRef(env, cause)
            Throwable.last = None
        fun.ExceptionClear(env)
        Throwable.last = thr = Throwable(jexc)#!!!, fname)
        raise thr

    # Java version

    def GetVersion(self):
        env = self.__env
        fun = env[0]
        ret = fun.GetVersion(env)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java class handling

    def DefineClass(self, name, loader, buf, blen):
        env = self.__env
        fun = env[0]
        ret = fun.DefineClass(env, name, loader, cast(buf, "const jbyte*"), blen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FindClass(self, name):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.FindClass(env, name)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetSuperclass(self, sub):
        env = self.__env
        fun = env[0]
        ret = fun.GetSuperclass(env, sub)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret if not isNULL(ret) else None

    def IsAssignableFrom(self, sub, sup):
        env = self.__env
        fun = env[0]
        return bool(fun.IsAssignableFrom(env, sub, sup))

    # Java exceptions handling

    def Throw(self, obj):
        env = self.__env
        fun = env[0]
        ret = fun.Throw(env, obj)
        if ret != 0: self._handle_JNIException(ret)

    def ThrowNew(self, clazz, msg):
        env = self.__env
        fun = env[0]
        ret = fun.ThrowNew(env, clazz, msg)
        if ret != 0: self._handle_JNIException(ret)

    def ExceptionOccurred(self):
        env = self.__env
        fun = env[0]
        return fun.ExceptionOccurred(env)

    def ExceptionDescribe(self):
        env = self.__env
        fun = env[0]
        fun.ExceptionDescribe(env)

    def ExceptionClear(self):
        env = self.__env
        fun = env[0]
        if Throwable.last:
            cause = Throwable.last.getCause()
            if cause: fun.DeleteGlobalRef(env, cause)
            Throwable.last = None
        fun.ExceptionClear(env)

    def FatalError(self, msg):
        env = self.__env
        fun = env[0]
        fun.FatalError(env, msg)

    def ExceptionCheck(self):
        env = self.__env
        fun = env[0]
        return bool(fun.ExceptionCheck(env))

    # JVM Call frame

    def PushLocalFrame(self, capacity):
        env = self.__env
        fun = env[0]
        ret = fun.PushLocalFrame(env, capacity)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def PopLocalFrame(self, result):
        env = self.__env
        fun = env[0]
        return fun.PopLocalFrame(env, result)

    # Java references handling

    def NewGlobalRef(self, lobj):
        env = self.__env
        fun = env[0]
        ret = fun.NewGlobalRef(env, lobj)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteGlobalRef(self, gref):
        env = self.__env
        fun = env[0]
        if gref: fun.DeleteGlobalRef(env, gref)

    def NewLocalRef(self, ref):
        env = self.__env
        fun = env[0]
        ret = fun.NewLocalRef(env, ref)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteLocalRef(self, obj):
        env = self.__env
        fun = env[0]
        if obj: fun.DeleteLocalRef(env, obj)

    def NewWeakGlobalRef(self, obj):
        env = self.__env
        fun = env[0]
        ret = fun.NewWeakGlobalRef(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def DeleteWeakGlobalRef(self, ref):
        env = self.__env
        fun = env[0]
        fun.DeleteWeakGlobalRef(env, ref)

    def EnsureLocalCapacity(self, capacity):
        env = self.__env
        fun = env[0]
        ret = fun.EnsureLocalCapacity(env, capacity)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java objects handling

    def AllocObject(self, clazz):
        env = self.__env
        fun = env[0]
        ret = fun.AllocObject(env, clazz)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObject(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.NewObjectA(env, clazz, methodID, _itself_or_NULL(args))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectClass(self, obj):
        env = self.__env
        fun = env[0]
        ret = fun.GetObjectClass(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectRefType(self, obj):
        # New in JNI 1.6
        env = self.__env
        fun = env[0]
        ret = fun.GetObjectRefType(env, obj)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def IsInstanceOf(self, obj, clazz):
        env = self.__env
        fun = env[0]
        return bool(fun.IsInstanceOf(env, obj, clazz))

    def IsSameObject(self, obj1, obj2):
        env = self.__env
        fun = env[0]
        return bool(fun.IsSameObject(env, obj1, obj2))

    # Call Java instance method

    def GetMethodID(self, clazz, name, sig):
        env = self.__env
        fun = env[0]
        ret = fun.GetMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallObjectMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallObjectMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallBooleanMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallBooleanMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallByteMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallByteMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallCharMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallCharMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallShortMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallShortMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallIntMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallIntMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallLongMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallLongMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallFloatMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallFloatMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallDoubleMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallDoubleMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallVoidMethod(self, obj, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        fun.CallVoidMethodA(env, obj, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... nonvirtually

    def CallNonvirtualObjectMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualObjectMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualBooleanMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualBooleanMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallNonvirtualByteMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualByteMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualCharMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualCharMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualShortMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualShortMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualIntMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualIntMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualLongMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualLongMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualFloatMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualFloatMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualDoubleMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        ret = fun.CallNonvirtualDoubleMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallNonvirtualVoidMethod(self, obj, clazz, methodID, args=None):
        env = self.__env
        fun = env[0]
        fun.CallNonvirtualVoidMethodA(env, obj, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java instance fields

    def GetFieldID(self, clazz, name, sig):
        env = self.__env
        fun = env[0]
        ret = fun.GetFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetObjectField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetBooleanField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetBooleanField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetByteField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetByteField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetCharField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetShortField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetIntField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetLongField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetFloatField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleField(self, obj, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetDoubleField(env, obj, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java instance fields

    def SetObjectField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetObjectField(env, obj, fieldID, _itself_or_NULL(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetBooleanField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetByteField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetCharField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetShortField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetIntField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetLongField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetFloatField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleField(self, obj, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetDoubleField(env, obj, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Call Java static method

    def GetStaticMethodID(self, clazz, name, sig):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticMethodID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticObjectMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticObjectMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticBooleanMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticBooleanMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def CallStaticByteMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticByteMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticCharMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticCharMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticShortMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticShortMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticIntMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticIntMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticLongMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticLongMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticFloatMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticFloatMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticDoubleMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        ret = fun.CallStaticDoubleMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def CallStaticVoidMethod(self, clazz, methodID, args=None):  # (GIL ?)
        env = self.__env
        fun = env[0]
        fun.CallStaticVoidMethodA(env, clazz, methodID, _itself_or_NULL(args))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Getting Java static fields

    def GetStaticFieldID(self, clazz, name, sig):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticFieldID(env, clazz, name, sig)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticObjectField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticObjectField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticBooleanField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticBooleanField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return bool(ret)

    def GetStaticByteField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticByteField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticCharField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticCharField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticShortField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticShortField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticIntField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticIntField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticLongField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticLongField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticFloatField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticFloatField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStaticDoubleField(self, clazz, fieldID):
        env = self.__env
        fun = env[0]
        ret = fun.GetStaticDoubleField(env, clazz, fieldID)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Setting Java static fields

    def SetStaticObjectField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticObjectField(env, clazz, fieldID, _itself_or_NULL(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticBooleanField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticBooleanField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticByteField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticByteField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticCharField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticCharField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticShortField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticShortField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticIntField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticIntField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticLongField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticLongField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticFloatField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticFloatField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetStaticDoubleField(self, clazz, fieldID, value):
        env = self.__env
        fun = env[0]
        fun.SetStaticDoubleField(env, clazz, fieldID, value)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java strings handling

    def NewString(self, unicode, slen):
        env = self.__env
        fun = env[0]
        ret = fun.NewString(env, unicode, slen)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringLength(self, str):
        env = self.__env
        fun = env[0]
        ret = fun.GetStringLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringChars(self, str, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetStringChars(env, str, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringChars(self, str, chars):
        env = self.__env
        fun = env[0]
        fun.ReleaseStringChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewStringUTF(self, utf):
        env = self.__env
        fun = env[0]
        ret = fun.NewStringUTF(env, utf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFLength(self, str):
        env = self.__env
        fun = env[0]
        ret = fun.GetStringUTFLength(env, str)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetStringUTFChars(self, str, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetStringUTFChars(env, str, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringUTFChars(self, str, chars):
        env = self.__env
        fun = env[0]
        fun.ReleaseStringUTFChars(env, str, chars)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringRegion(self, str, start, len, buf):
        env = self.__env
        fun = env[0]
        fun.GetStringRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetStringUTFRegion(self, str, start, len, buf):
        env = self.__env
        fun = env[0]
        fun.GetStringUTFRegion(env, str, start, len, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetStringCritical(self, string, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetStringCritical(env, string, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseStringCritical(self, string, cstring):
        env = self.__env
        fun = env[0]
        fun.ReleaseStringCritical(env, string, cstring)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java arrays handling

    def GetArrayLength(self, array):
        env = self.__env
        fun = env[0]
        ret = fun.GetArrayLength(env, array)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewObjectArray(self, size, clazz, init=None):
        env = self.__env
        fun = env[0]
        ret = fun.NewObjectArray(env, size, clazz, _itself_or_NULL(init))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetObjectArrayElement(self, array, index):
        env = self.__env
        fun = env[0]
        ret = fun.GetObjectArrayElement(env, array, index)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def SetObjectArrayElement(self, array, index, value):
        env = self.__env
        fun = env[0]
        fun.SetObjectArrayElement(env, array, index, _itself_or_NULL(value))
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def NewBooleanArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewBooleanArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewByteArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewByteArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewCharArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewCharArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewShortArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewShortArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewIntArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewIntArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewLongArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewLongArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewFloatArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewFloatArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def NewDoubleArray(self, size):
        env = self.__env
        fun = env[0]
        ret = fun.NewDoubleArray(env, size)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetBooleanArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetBooleanArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetByteArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetByteArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetCharArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetCharArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetShortArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetShortArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetIntArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetIntArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetLongArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetLongArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetFloatArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetFloatArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDoubleArrayElements(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetDoubleArrayElements(env, array, _byref_or_NULL(isCopy))
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleaseBooleanArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseBooleanArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseByteArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseByteArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseCharArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseCharArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseShortArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseShortArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseIntArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseIntArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseLongArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseLongArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseFloatArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseFloatArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def ReleaseDoubleArrayElements(self, array, elems, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleaseDoubleArrayElements(env, array, elems, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetBooleanArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetByteArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetCharArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetShortArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetIntArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetLongArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetFloatArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def GetDoubleArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.GetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetBooleanArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetBooleanArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetByteArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetByteArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetCharArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetCharArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetShortArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetShortArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetIntArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetIntArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetLongArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetLongArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetFloatArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetFloatArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    def SetDoubleArrayRegion(self, array, start, size, buf):
        env = self.__env
        fun = env[0]
        fun.SetDoubleArrayRegion(env, array, start, size, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # ... in a critical manner

    def GetPrimitiveArrayCritical(self, array, isCopy=None):
        env = self.__env
        fun = env[0]
        ret = fun.GetPrimitiveArrayCritical(env, array, _byref_or_NULL(isCopy))
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ReleasePrimitiveArrayCritical(self, array, carray, mode=0):
        env = self.__env
        fun = env[0]
        fun.ReleasePrimitiveArrayCritical(env, array, carray, mode)
        if fun.ExceptionCheck(env): self._handle_JavaException()

    # Java native methods handling

    def RegisterNatives(self, clazz, methods, nMethods):
        env = self.__env
        fun = env[0]
        # Required due to bug in jvm:
        # https://bugs.java.com/bugdatabase/view_bug.do?bug_id=6493522
        fun.GetMethodID(env, clazz, b"notify", b"()V")
        ret = 0 # fun.RegisterNatives(env, clazz, methods, nMethods)
        # print("RegisterNatives:ret:", ret)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def UnregisterNatives(self, clazz):
        env = self.__env
        fun = env[0]
        ret = fun.UnregisterNatives(env, clazz)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java object monitoring

    def MonitorEnter(self, obj):
        env = self.__env
        fun = env[0]
        ret = fun.MonitorEnter(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def MonitorExit(self, obj):
        env = self.__env
        fun = env[0]
        ret = fun.MonitorExit(env, obj)
        if ret != 0 and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java direct buffer handling

    def NewDirectByteBuffer(self, address, capacity):
        env = self.__env
        fun = env[0]
        ret = fun.NewDirectByteBuffer(env, from_buffer(address), capacity)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferAddress(self, buf):
        env = self.__env
        fun = env[0]
        ret = fun.GetDirectBufferAddress(env, buf)
        if not ret and fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def GetDirectBufferCapacity(self, buf):
        env = self.__env
        fun = env[0]
        ret = fun.GetDirectBufferCapacity(env, buf)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java reflection support

    def FromReflectedMethod(self, method):
        env = self.__env
        fun = env[0]
        ret = fun.FromReflectedMethod(env, method)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def FromReflectedField(self, field):
        env = self.__env
        fun = env[0]
        ret = fun.FromReflectedField(env, field)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedMethod(self, cls, methodID, isStatic):
        env = self.__env
        fun = env[0]
        ret = fun.ToReflectedMethod(env, cls, methodID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    def ToReflectedField(self, cls, fieldID, isStatic):
        env = self.__env
        fun = env[0]
        ret = fun.ToReflectedField(env, cls, fieldID, isStatic)
        if fun.ExceptionCheck(env): self._handle_JavaException()
        return ret

    # Java VM Interface

    def GetJavaVM(self, vm):
        env = self.__env
        fun = env[0]
        ret = fun.GetJavaVM(env, vm)
        if ret != 0: self._handle_JNIException(ret)

tmap[JNIEnv] = ffi.typeof("JNIEnv")

def JEnv(penv):
    jenv = JNIEnv()
    jenv._JNIEnv__env = penv
    jenv._JNIEnv__fun = penv[0]
    return jenv

#
# JNI Invocation Interface.
#

class JavaVM:

    def _handle_JNIException(self, err):
        import sys
        fun_name = sys._getframe(1).f_code.co_name
        raise JNIException(err, info=fun_name)

    def DestroyJavaVM(self):
        jvm = self.__jvm
        fun = jvm[0]
        ret = fun.DestroyJavaVM(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def AttachCurrentThread(self, penv, args=None):
        jvm = self.__jvm
        fun = jvm[0]
        p_penv = pointer(penv)
        ret = fun.AttachCurrentThread(jvm, cast(p_penv, "void**"), _itself_or_NULL(args))
        if ret != JNI_OK: self._handle_JNIException(ret)
        _as_CData(penv).c_data = _as_CData(p_penv[0]).c_data

    def AttachCurrentThreadAsDaemon(self, penv, args=None):
        jvm = self.__jvm
        fun = jvm[0]
        p_penv = pointer(penv)
        ret = fun.AttachCurrentThreadAsDaemon(jvm, cast(p_penv, "void**"), _itself_or_NULL(args))
        if ret != JNI_OK: self._handle_JNIException(ret)
        _as_CData(penv).c_data = _as_CData(p_penv[0]).c_data

    def DetachCurrentThread(self):
        jvm = self.__jvm
        fun = jvm[0]
        ret = fun.DetachCurrentThread(jvm)
        if ret != JNI_OK: self._handle_JNIException(ret)

    def GetEnv(self, penv, version):
        jvm = self.__jvm
        fun = jvm[0]
        p_penv = pointer(penv)
        ret = fun.GetEnv(jvm, cast(p_penv, "void**"), version)
        if ret != JNI_OK: self._handle_JNIException(ret)
        _as_CData(penv).c_data = _as_CData(p_penv[0]).c_data

tmap[JavaVM] = ffi.typeof("JavaVM")

def JVM(pjvm):
    jvm = JavaVM()
    jvm._JavaVM__jvm = pjvm
    jvm._JavaVM__fun = pjvm[0]
    return jvm

JavaVMOption = ffi.typeof("JavaVMOption")

JavaVMInitArgs = ffi.typeof("JavaVMInitArgs")

JavaVMAttachArgs = ffi.typeof("JavaVMAttachArgs")

# These will be VM-specific.

JDK1_2 = ffi.integer_const("JDK1_2")
JDK1_4 = ffi.integer_const("JDK1_4")

# End VM-specific.

# JNI version constants

JNI_VERSION_1_1 = ffi.integer_const("JNI_VERSION_1_1")
JNI_VERSION_1_2 = ffi.integer_const("JNI_VERSION_1_2")
JNI_VERSION_1_4 = ffi.integer_const("JNI_VERSION_1_4")
JNI_VERSION_1_6 = ffi.integer_const("JNI_VERSION_1_6")
JNI_VERSION_1_8 = ffi.integer_const("JNI_VERSION_1_8")
JNI_VERSION_9   = ffi.integer_const("JNI_VERSION_9")
JNI_VERSION_10  = ffi.integer_const("JNI_VERSION_10")

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
                                                f"unknown error code {self._error}")

    def getError(self):
        return self._error

def load(dll_path, handle=None, __dlclose=dlclose, __ffi=ffi):

    try:
        if isinstance(dll_path, os.PathLike): dll_path = str(dll_path)
        dll = DLL(dll_path, handle=handle)
    except OSError as exc:
        raise exc
    except Exception as exc:
        raise OSError(f"{exc}") from None

    def JNI_GetDefaultJavaVMInitArgs(args, __dll=dll):
        return __dll.JNI_GetDefaultJavaVMInitArgs(cast(args, "void*"))

    def JNI_CreateJavaVM(pvm, penv, args, __dll=dll):
        p_pvm  = pointer(pvm)
        p_penv = pointer(penv)
        p_args = pointer(args)
        result = __dll.JNI_CreateJavaVM(p_pvm, cast(p_penv, "void**"), cast(p_args, "void*"))
        _as_CData(pvm).c_data  = _as_CData(p_pvm[0]).c_data
        _as_CData(penv).c_data = _as_CData(p_penv[0]).c_data
        return result

    def JNI_GetCreatedJavaVMs(pvm, size, nvms, __dll=dll):
        return __dll.JNI_GetCreatedJavaVMs(_itself_or_NULL(pvm), size, nvms)

    JNI = type("JNI", (), dict(dll=dll, dllclose=classmethod(lambda cls, __dlclose=__dlclose: __dlclose(cls.dll))))
    JNI.GetDefaultJavaVMInitArgs = JNI_GetDefaultJavaVMInitArgs
    JNI.CreateJavaVM             = JNI_CreateJavaVM
    JNI.GetCreatedJavaVMs        = JNI_GetCreatedJavaVMs

    return JNI

#
# Decorator for defining Java native method in Python
#

def method(signature, **kwargs):
    ret_type, arg_types = __parse_signature(signature)
    fun_name = new_cstr(kwargs["name"].encode("utf-8")) if "name" in kwargs else None
    fun_sign = new_cstr(signature.encode("utf-8"))
    FunProto = CFUNC(ret_type, POINTER(JNIEnv), jobject, *arg_types)
    Fun_Proto = None
    _fun_name = None
    def wrapper(fun, fun_name=fun_name, fun_sign=fun_sign):
        nonlocal Fun_Proto, _fun_name
        Fun_Proto = FunProto(fun)
        _fun_name = new_cstr(fun.__name__.encode("utf-8"))
        native_meth = new(JNINativeMethod)[0]
        native_meth.name      = fun_name or _fun_name
        native_meth.signature = fun_sign
        native_meth.fnPtr     = cast(Fun_Proto, "void*")
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
del platform
del ct
del ffi
del tmap
del dlclose
