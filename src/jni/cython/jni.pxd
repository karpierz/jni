# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

# distutils: language=c

cdef extern from "<stdarg.h>":

    ctypedef struct va_list:
        pass

#cdef extern from *:
#cdef public:
#cdef public api: # from "jni.h":
cdef api: # from "jni.h":

    #
    # JNI Types
    #

    ctypedef long           c_jint
    ctypedef long long      c_jlong  # int64_t, jni.h: __int64
    ctypedef signed char    c_jbyte  # javabridge: unsigned (chyba blad!!!)

    ctypedef unsigned char  c_jboolean
    ctypedef unsigned short c_jchar
    ctypedef short          c_jshort
    ctypedef float          c_jfloat
    ctypedef double         c_jdouble
    ctypedef c_jint         c_jsize

    struct _jobject
    ctypedef _jobject* c_jobject
    ctypedef c_jobject c_jclass
    ctypedef c_jobject c_jthrowable
    ctypedef c_jobject c_jstring
    ctypedef c_jobject c_jarray
    ctypedef c_jarray  c_jbooleanArray
    ctypedef c_jarray  c_jbyteArray
    ctypedef c_jarray  c_jcharArray
    ctypedef c_jarray  c_jshortArray
    ctypedef c_jarray  c_jintArray
    ctypedef c_jarray  c_jlongArray
    ctypedef c_jarray  c_jfloatArray
    ctypedef c_jarray  c_jdoubleArray
    ctypedef c_jarray  c_jobjectArray
    ctypedef c_jobject c_jweak

    ctypedef union c_jvalue:
        c_jboolean z
        c_jbyte    b
        c_jchar    c
        c_jshort   s
        c_jint     i
        c_jlong    j
        c_jfloat   f
        c_jdouble  d
        c_jobject  l

    struct _jfieldID
    ctypedef _jfieldID* c_jfieldID

    struct _jmethodID
    ctypedef _jmethodID* c_jmethodID

    # Return values from jobjectRefType

    cdef enum:
        JNIInvalidRefType    = 0
        JNILocalRefType      = 1
        JNIGlobalRefType     = 2
        JNIWeakGlobalRefType = 3
    ctypedef int c_jobjectRefType

    #
    # jboolean constants
    #

    cdef enum:
        JNI_FALSE = 0
        JNI_TRUE  = 1

    #
    # possible return values for JNI functions.
    #

    cdef enum:
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

    cdef enum:
        JNI_COMMIT = 1
        JNI_ABORT  = 2

    #
    # used in RegisterNatives to describe native method name,
    # signature, and function pointer.
    #

    ctypedef struct c_JNINativeMethod:
        char* name       # Android and/or jnius: const char*
        char* signature  # Android and/or jnius: const char*
        void* fnPtr

    #
    # JNI Native Method Interface.
    #

    struct JNINativeInterface_
    ctypedef const JNINativeInterface_* c_JNIEnv

    #
    # JNI Invocation Interface.
    #

    struct JNIInvokeInterface_
    ctypedef const JNIInvokeInterface_* c_JavaVM

    # JNI Native Method Interface.

    struct JNINativeInterface_:

        void* reserved0
        void* reserved1
        void* reserved2
        void* reserved3

        c_jint        (*GetVersion)                   (c_JNIEnv* env)

        c_jclass      (*DefineClass)                  (c_JNIEnv* env, const char* name, c_jobject loader, const c_jbyte* buf, c_jsize len)
        c_jclass      (*FindClass)                    (c_JNIEnv* env, const char* name)

        c_jmethodID   (*FromReflectedMethod)          (c_JNIEnv* env, c_jobject method)
        c_jfieldID    (*FromReflectedField)           (c_JNIEnv* env, c_jobject field)

        c_jobject     (*ToReflectedMethod)            (c_JNIEnv* env, c_jclass cls, c_jmethodID methodID, c_jboolean isStatic)

        c_jclass      (*GetSuperclass)                (c_JNIEnv* env, c_jclass sub)
        c_jboolean    (*IsAssignableFrom)             (c_JNIEnv* env, c_jclass sub, c_jclass sup)

        c_jobject     (*ToReflectedField)             (c_JNIEnv* env, c_jclass cls, c_jfieldID fieldID, c_jboolean isStatic)

        c_jint        (*Throw)                        (c_JNIEnv* env, c_jthrowable obj)
        c_jint        (*ThrowNew)                     (c_JNIEnv* env, c_jclass clazz, const char* msg)
        c_jthrowable  (*ExceptionOccurred)            (c_JNIEnv* env)
        void          (*ExceptionDescribe)            (c_JNIEnv* env)
        void          (*ExceptionClear)               (c_JNIEnv* env)
        void          (*FatalError)                   (c_JNIEnv* env, const char* msg)

        c_jint        (*PushLocalFrame)               (c_JNIEnv* env, c_jint capacity)
        c_jobject     (*PopLocalFrame)                (c_JNIEnv* env, c_jobject result)

        c_jobject     (*NewGlobalRef)                 (c_JNIEnv* env, c_jobject lobj)
        void          (*DeleteGlobalRef)              (c_JNIEnv* env, c_jobject gref)
        void          (*DeleteLocalRef)               (c_JNIEnv* env, c_jobject obj)
        c_jboolean    (*IsSameObject)                 (c_JNIEnv* env, c_jobject obj1, c_jobject obj2)
        c_jobject     (*NewLocalRef)                  (c_JNIEnv* env, c_jobject ref)
        c_jint        (*EnsureLocalCapacity)          (c_JNIEnv* env, c_jint capacity)

        c_jobject     (*AllocObject)                  (c_JNIEnv* env, c_jclass clazz)
        c_jobject     (*NewObject)                    (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...)
        c_jobject     (*NewObjectV)                   (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args)
        c_jobject     (*NewObjectA)                   (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args)

        c_jclass      (*GetObjectClass)               (c_JNIEnv* env, c_jobject obj)
        c_jboolean    (*IsInstanceOf)                 (c_JNIEnv* env, c_jobject obj, c_jclass clazz)

        c_jmethodID   (*GetMethodID)                  (c_JNIEnv* env, c_jclass clazz, const char* name, const char* sig)

        c_jobject     (*CallObjectMethod)             (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jobject     (*CallObjectMethodV)            (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jobject     (*CallObjectMethodA)            (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jboolean    (*CallBooleanMethod)            (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jboolean    (*CallBooleanMethodV)           (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jboolean    (*CallBooleanMethodA)           (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jbyte       (*CallByteMethod)               (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jbyte       (*CallByteMethodV)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jbyte       (*CallByteMethodA)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jchar       (*CallCharMethod)               (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jchar       (*CallCharMethodV)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jchar       (*CallCharMethodA)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jshort      (*CallShortMethod)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jshort      (*CallShortMethodV)             (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jshort      (*CallShortMethodA)             (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jint        (*CallIntMethod)                (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jint        (*CallIntMethodV)               (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jint        (*CallIntMethodA)               (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jlong       (*CallLongMethod)               (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jlong       (*CallLongMethodV)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jlong       (*CallLongMethodA)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jfloat      (*CallFloatMethod)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jfloat      (*CallFloatMethodV)             (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jfloat      (*CallFloatMethodA)             (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jdouble     (*CallDoubleMethod)             (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        c_jdouble     (*CallDoubleMethodV)            (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        c_jdouble     (*CallDoubleMethodA)            (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        void          (*CallVoidMethod)               (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, ...) # nogil
        void          (*CallVoidMethodV)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, va_list args) # nogil
        void          (*CallVoidMethodA)              (c_JNIEnv* env, c_jobject obj, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jobject     (*CallNonvirtualObjectMethod)   (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jobject     (*CallNonvirtualObjectMethodV)  (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jobject     (*CallNonvirtualObjectMethodA)  (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jboolean    (*CallNonvirtualBooleanMethod)  (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jboolean    (*CallNonvirtualBooleanMethodV) (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jboolean    (*CallNonvirtualBooleanMethodA) (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jbyte       (*CallNonvirtualByteMethod)     (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jbyte       (*CallNonvirtualByteMethodV)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jbyte       (*CallNonvirtualByteMethodA)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jchar       (*CallNonvirtualCharMethod)     (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jchar       (*CallNonvirtualCharMethodV)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jchar       (*CallNonvirtualCharMethodA)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jshort      (*CallNonvirtualShortMethod)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jshort      (*CallNonvirtualShortMethodV)   (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jshort      (*CallNonvirtualShortMethodA)   (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jint        (*CallNonvirtualIntMethod)      (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jint        (*CallNonvirtualIntMethodV)     (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jint        (*CallNonvirtualIntMethodA)     (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jlong       (*CallNonvirtualLongMethod)     (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jlong       (*CallNonvirtualLongMethodV)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jlong       (*CallNonvirtualLongMethodA)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jfloat      (*CallNonvirtualFloatMethod)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jfloat      (*CallNonvirtualFloatMethodV)   (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jfloat      (*CallNonvirtualFloatMethodA)   (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jdouble     (*CallNonvirtualDoubleMethod)   (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jdouble     (*CallNonvirtualDoubleMethodV)  (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jdouble     (*CallNonvirtualDoubleMethodA)  (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        void          (*CallNonvirtualVoidMethod)     (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        void          (*CallNonvirtualVoidMethodV)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        void          (*CallNonvirtualVoidMethodA)    (c_JNIEnv* env, c_jobject obj, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jfieldID    (*GetFieldID)                   (c_JNIEnv* env, c_jclass clazz, const char* name, const char* sig)

        c_jobject     (*GetObjectField)               (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jboolean    (*GetBooleanField)              (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jbyte       (*GetByteField)                 (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jchar       (*GetCharField)                 (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jshort      (*GetShortField)                (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jint        (*GetIntField)                  (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jlong       (*GetLongField)                 (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jfloat      (*GetFloatField)                (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)
        c_jdouble     (*GetDoubleField)               (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID)

        void          (*SetObjectField)               (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jobject  value)
        void          (*SetBooleanField)              (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jboolean value)
        void          (*SetByteField)                 (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jbyte    value)
        void          (*SetCharField)                 (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jchar    value)
        void          (*SetShortField)                (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jshort   value)
        void          (*SetIntField)                  (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jint     value)
        void          (*SetLongField)                 (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jlong    value)
        void          (*SetFloatField)                (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jfloat   value)
        void          (*SetDoubleField)               (c_JNIEnv* env, c_jobject obj, c_jfieldID fieldID, c_jdouble  value)

        c_jmethodID   (*GetStaticMethodID)            (c_JNIEnv* env, c_jclass clazz, const char* name, const char* sig)

        c_jobject     (*CallStaticObjectMethod)       (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jobject     (*CallStaticObjectMethodV)      (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jobject     (*CallStaticObjectMethodA)      (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jboolean    (*CallStaticBooleanMethod)      (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jboolean    (*CallStaticBooleanMethodV)     (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jboolean    (*CallStaticBooleanMethodA)     (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jbyte       (*CallStaticByteMethod)         (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jbyte       (*CallStaticByteMethodV)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jbyte       (*CallStaticByteMethodA)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jchar       (*CallStaticCharMethod)         (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jchar       (*CallStaticCharMethodV)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jchar       (*CallStaticCharMethodA)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jshort      (*CallStaticShortMethod)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jshort      (*CallStaticShortMethodV)       (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jshort      (*CallStaticShortMethodA)       (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jint        (*CallStaticIntMethod)          (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jint        (*CallStaticIntMethodV)         (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jint        (*CallStaticIntMethodA)         (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jlong       (*CallStaticLongMethod)         (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jlong       (*CallStaticLongMethodV)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jlong       (*CallStaticLongMethodA)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jfloat      (*CallStaticFloatMethod)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jfloat      (*CallStaticFloatMethodV)       (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jfloat      (*CallStaticFloatMethodA)       (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jdouble     (*CallStaticDoubleMethod)       (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        c_jdouble     (*CallStaticDoubleMethodV)      (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        c_jdouble     (*CallStaticDoubleMethodA)      (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        void          (*CallStaticVoidMethod)         (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, ...) # nogil
        void          (*CallStaticVoidMethodV)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, va_list args) # nogil
        void          (*CallStaticVoidMethodA)        (c_JNIEnv* env, c_jclass clazz, c_jmethodID methodID, const c_jvalue* args) # nogil

        c_jfieldID    (*GetStaticFieldID)             (c_JNIEnv* env, c_jclass clazz, const char* name, const char* sig)

        c_jobject     (*GetStaticObjectField)         (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jboolean    (*GetStaticBooleanField)        (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jbyte       (*GetStaticByteField)           (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jchar       (*GetStaticCharField)           (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jshort      (*GetStaticShortField)          (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jint        (*GetStaticIntField)            (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jlong       (*GetStaticLongField)           (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jfloat      (*GetStaticFloatField)          (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)
        c_jdouble     (*GetStaticDoubleField)         (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID)

        void          (*SetStaticObjectField)         (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jobject  value)
        void          (*SetStaticBooleanField)        (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jboolean value)
        void          (*SetStaticByteField)           (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jbyte    value)
        void          (*SetStaticCharField)           (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jchar    value)
        void          (*SetStaticShortField)          (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jshort   value)
        void          (*SetStaticIntField)            (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jint     value)
        void          (*SetStaticLongField)           (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jlong    value)
        void          (*SetStaticFloatField)          (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jfloat   value)
        void          (*SetStaticDoubleField)         (c_JNIEnv* env, c_jclass clazz, c_jfieldID fieldID, c_jdouble  value)

        c_jstring     (*NewString)                    (c_JNIEnv* env, const c_jchar* ustr, c_jsize len)
        c_jsize       (*GetStringLength)              (c_JNIEnv* env, c_jstring str)
        const c_jchar*(*GetStringChars)               (c_JNIEnv* env, c_jstring str, c_jboolean* isCopy)
        void          (*ReleaseStringChars)           (c_JNIEnv* env, c_jstring str, const c_jchar* chars)

        c_jstring     (*NewStringUTF)                 (c_JNIEnv* env, const char* utf)
        c_jsize       (*GetStringUTFLength)           (c_JNIEnv* env, c_jstring str)
        const char*   (*GetStringUTFChars)            (c_JNIEnv* env, c_jstring str, c_jboolean* isCopy)
        void          (*ReleaseStringUTFChars)        (c_JNIEnv* env, c_jstring str, const char* chars)

        c_jsize       (*GetArrayLength)               (c_JNIEnv* env, c_jarray array)

        c_jobjectArray (*NewObjectArray)              (c_JNIEnv* env, c_jsize len, c_jclass clazz, c_jobject init)
        c_jobject     (*GetObjectArrayElement)        (c_JNIEnv* env, c_jobjectArray array, c_jsize index)
        void          (*SetObjectArrayElement)        (c_JNIEnv* env, c_jobjectArray array, c_jsize index, c_jobject value)

        c_jbooleanArray (*NewBooleanArray)            (c_JNIEnv* env, c_jsize len)
        c_jbyteArray  (*NewByteArray)                 (c_JNIEnv* env, c_jsize len)
        c_jcharArray  (*NewCharArray)                 (c_JNIEnv* env, c_jsize len)
        c_jshortArray (*NewShortArray)                (c_JNIEnv* env, c_jsize len)
        c_jintArray   (*NewIntArray)                  (c_JNIEnv* env, c_jsize len)
        c_jlongArray  (*NewLongArray)                 (c_JNIEnv* env, c_jsize len)
        c_jfloatArray (*NewFloatArray)                (c_JNIEnv* env, c_jsize len)
        c_jdoubleArray(*NewDoubleArray)               (c_JNIEnv* env, c_jsize len)

        c_jboolean*   (*GetBooleanArrayElements)      (c_JNIEnv* env, c_jbooleanArray array, c_jboolean* isCopy)
        c_jbyte*      (*GetByteArrayElements)         (c_JNIEnv* env, c_jbyteArray    array, c_jboolean* isCopy)
        c_jchar*      (*GetCharArrayElements)         (c_JNIEnv* env, c_jcharArray    array, c_jboolean* isCopy)
        c_jshort*     (*GetShortArrayElements)        (c_JNIEnv* env, c_jshortArray   array, c_jboolean* isCopy)
        c_jint*       (*GetIntArrayElements)          (c_JNIEnv* env, c_jintArray     array, c_jboolean* isCopy)
        c_jlong*      (*GetLongArrayElements)         (c_JNIEnv* env, c_jlongArray    array, c_jboolean* isCopy)
        c_jfloat*     (*GetFloatArrayElements)        (c_JNIEnv* env, c_jfloatArray   array, c_jboolean* isCopy)
        c_jdouble*    (*GetDoubleArrayElements)       (c_JNIEnv* env, c_jdoubleArray  array, c_jboolean* isCopy)

        void          (*ReleaseBooleanArrayElements)  (c_JNIEnv* env, c_jbooleanArray array, c_jboolean* elems, c_jint mode)
        void          (*ReleaseByteArrayElements)     (c_JNIEnv* env, c_jbyteArray    array, c_jbyte*    elems, c_jint mode)
        void          (*ReleaseCharArrayElements)     (c_JNIEnv* env, c_jcharArray    array, c_jchar*    elems, c_jint mode)
        void          (*ReleaseShortArrayElements)    (c_JNIEnv* env, c_jshortArray   array, c_jshort*   elems, c_jint mode)
        void          (*ReleaseIntArrayElements)      (c_JNIEnv* env, c_jintArray     array, c_jint*     elems, c_jint mode)
        void          (*ReleaseLongArrayElements)     (c_JNIEnv* env, c_jlongArray    array, c_jlong*    elems, c_jint mode)
        void          (*ReleaseFloatArrayElements)    (c_JNIEnv* env, c_jfloatArray   array, c_jfloat*   elems, c_jint mode)
        void          (*ReleaseDoubleArrayElements)   (c_JNIEnv* env, c_jdoubleArray  array, c_jdouble*  elems, c_jint mode)

        void          (*GetBooleanArrayRegion)        (c_JNIEnv* env, c_jbooleanArray array, c_jsize start, c_jsize len, c_jboolean* buf)
        void          (*GetByteArrayRegion)           (c_JNIEnv* env, c_jbyteArray    array, c_jsize start, c_jsize len, c_jbyte*    buf)
        void          (*GetCharArrayRegion)           (c_JNIEnv* env, c_jcharArray    array, c_jsize start, c_jsize len, c_jchar*    buf)
        void          (*GetShortArrayRegion)          (c_JNIEnv* env, c_jshortArray   array, c_jsize start, c_jsize len, c_jshort*   buf)
        void          (*GetIntArrayRegion)            (c_JNIEnv* env, c_jintArray     array, c_jsize start, c_jsize len, c_jint*     buf)
        void          (*GetLongArrayRegion)           (c_JNIEnv* env, c_jlongArray    array, c_jsize start, c_jsize len, c_jlong*    buf)
        void          (*GetFloatArrayRegion)          (c_JNIEnv* env, c_jfloatArray   array, c_jsize start, c_jsize len, c_jfloat*   buf)
        void          (*GetDoubleArrayRegion)         (c_JNIEnv* env, c_jdoubleArray  array, c_jsize start, c_jsize len, c_jdouble*  buf)

        void          (*SetBooleanArrayRegion)        (c_JNIEnv* env, c_jbooleanArray array, c_jsize start, c_jsize len, const c_jboolean* buf)
        void          (*SetByteArrayRegion)           (c_JNIEnv* env, c_jbyteArray    array, c_jsize start, c_jsize len, const c_jbyte*    buf)
        void          (*SetCharArrayRegion)           (c_JNIEnv* env, c_jcharArray    array, c_jsize start, c_jsize len, const c_jchar*    buf)
        void          (*SetShortArrayRegion)          (c_JNIEnv* env, c_jshortArray   array, c_jsize start, c_jsize len, const c_jshort*   buf)
        void          (*SetIntArrayRegion)            (c_JNIEnv* env, c_jintArray     array, c_jsize start, c_jsize len, const c_jint*     buf)
        void          (*SetLongArrayRegion)           (c_JNIEnv* env, c_jlongArray    array, c_jsize start, c_jsize len, const c_jlong*    buf)
        void          (*SetFloatArrayRegion)          (c_JNIEnv* env, c_jfloatArray   array, c_jsize start, c_jsize len, const c_jfloat*   buf)
        void          (*SetDoubleArrayRegion)         (c_JNIEnv* env, c_jdoubleArray  array, c_jsize start, c_jsize len, const c_jdouble*  buf)

        c_jint        (*RegisterNatives)              (c_JNIEnv* env, c_jclass clazz, const c_JNINativeMethod* methods, c_jint nMethods)
        c_jint        (*UnregisterNatives)            (c_JNIEnv* env, c_jclass clazz)

        c_jint        (*MonitorEnter)                 (c_JNIEnv* env, c_jobject obj)
        c_jint        (*MonitorExit)                  (c_JNIEnv* env, c_jobject obj)

        c_jint        (*GetJavaVM)                    (c_JNIEnv* env, c_JavaVM** vm)

        void          (*GetStringRegion)              (c_JNIEnv* env, c_jstring str, c_jsize start, c_jsize len, c_jchar* buf)
        void          (*GetStringUTFRegion)           (c_JNIEnv* env, c_jstring str, c_jsize start, c_jsize len, char*    buf)

        void*         (*GetPrimitiveArrayCritical)    (c_JNIEnv* env, c_jarray array, c_jboolean* isCopy)
        void          (*ReleasePrimitiveArrayCritical)(c_JNIEnv* env, c_jarray array, void* carray, c_jint mode)

        const c_jchar*(*GetStringCritical)            (c_JNIEnv* env, c_jstring string, c_jboolean* isCopy)
        void          (*ReleaseStringCritical)        (c_JNIEnv* env, c_jstring string, const c_jchar* cstring)

        c_jweak       (*NewWeakGlobalRef)             (c_JNIEnv* env, c_jobject obj)
        void          (*DeleteWeakGlobalRef)          (c_JNIEnv* env, c_jweak   ref)

        c_jboolean    (*ExceptionCheck)               (c_JNIEnv* env)

        c_jobject     (*NewDirectByteBuffer)          (c_JNIEnv* env, void* address, c_jlong capacity)
        void*         (*GetDirectBufferAddress)       (c_JNIEnv* env, c_jobject buf)
        c_jlong       (*GetDirectBufferCapacity)      (c_JNIEnv* env, c_jobject buf)

        # New JNI 1.6 Features

        c_jobjectRefType (*GetObjectRefType)          (c_JNIEnv* env, c_jobject obj)

    # JNI Invocation Interface.

    ctypedef struct c_JavaVMOption:
        char* optionString
        void* extraInfo

    ctypedef struct c_JavaVMInitArgs:
        c_jint          version
        c_jint          nOptions
        c_JavaVMOption* options
        c_jboolean      ignoreUnrecognized

    ctypedef struct c_JavaVMAttachArgs:
        c_jint    version
        char*     name
        c_jobject group

    # These will be VM-specific.

    cdef enum:
        JDK1_2 = 1
        JDK1_4 = 1

    # End VM-specific.

    struct JNIInvokeInterface_:

        void* reserved0
        void* reserved1
        void* reserved2

        c_jint (*DestroyJavaVM)              (c_JavaVM* vm) # nogil
        c_jint (*AttachCurrentThread)        (c_JavaVM* vm, void** penv, void* args) # nogil
        c_jint (*DetachCurrentThread)        (c_JavaVM* vm) # nogil
        c_jint (*GetEnv)                     (c_JavaVM* vm, void** penv, c_jint version) # nogil
        c_jint (*AttachCurrentThreadAsDaemon)(c_JavaVM* vm, void** penv, void* args) # nogil

    cdef enum:
        JNI_VERSION_1_1 = 0x00010001
        JNI_VERSION_1_2 = 0x00010002
        JNI_VERSION_1_4 = 0x00010004
        JNI_VERSION_1_6 = 0x00010006
        JNI_VERSION_1_8 = 0x00010008
        JNI_VERSION_9   = 0x00090000
        JNI_VERSION_10  = 0x000a0000

# eof jni.h

cdef extern: # from "jni.h":
    c_jint __stdcall JNI_GetDefaultJavaVMInitArgs(void* args) # nogil
    c_jint __stdcall JNI_CreateJavaVM     (c_JavaVM** pvm, void** penv, void* args) # nogil
    c_jint __stdcall JNI_GetCreatedJavaVMs(c_JavaVM** pvm, c_jsize size, c_jsize* nvms) # nogil
