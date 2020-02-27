import pytest

import jni.capi   as jni_capi
import jni.ctypes as jni_ctypes
import jni.cffi   as jni_cffi
import jni.cython as jni_cython


def test_jobjectRefType():
    assert 0 == jni_capi.JNIInvalidRefType    == jni_ctypes.JNIInvalidRefType    == jni_cffi.JNIInvalidRefType
    assert 1 == jni_capi.JNILocalRefType      == jni_ctypes.JNILocalRefType      == jni_cffi.JNILocalRefType
    assert 2 == jni_capi.JNIGlobalRefType     == jni_ctypes.JNIGlobalRefType     == jni_cffi.JNIGlobalRefType
    assert 3 == jni_capi.JNIWeakGlobalRefType == jni_ctypes.JNIWeakGlobalRefType == jni_cffi.JNIWeakGlobalRefType
    assert int is type(jni_capi.JNIInvalidRefType)    is type(jni_ctypes.JNIInvalidRefType)    is type(jni_cffi.JNIInvalidRefType)
    assert int is type(jni_capi.JNILocalRefType)      is type(jni_ctypes.JNILocalRefType)      is type(jni_cffi.JNILocalRefType)
    assert int is type(jni_capi.JNIGlobalRefType)     is type(jni_ctypes.JNIGlobalRefType)     is type(jni_cffi.JNIGlobalRefType)
    assert int is type(jni_capi.JNIWeakGlobalRefType) is type(jni_ctypes.JNIWeakGlobalRefType) is type(jni_cffi.JNIWeakGlobalRefType)

def test_jboolean_constants():
    assert False == jni_capi.JNI_FALSE == jni_ctypes.JNI_FALSE == jni_cffi.JNI_FALSE
    assert True  == jni_capi.JNI_TRUE  == jni_ctypes.JNI_TRUE  == jni_cffi.JNI_TRUE 
    assert int is type(jni_capi.JNI_FALSE) is type(jni_ctypes.JNI_FALSE) is type(jni_cffi.JNI_FALSE)
    assert int is type(jni_capi.JNI_TRUE)  is type(jni_ctypes.JNI_TRUE)  is type(jni_cffi.JNI_TRUE)

def test_possible_return_values():
    assert  0 == jni_capi.JNI_OK        == jni_ctypes.JNI_OK        == jni_cffi.JNI_OK
    assert -1 == jni_capi.JNI_ERR       == jni_ctypes.JNI_ERR       == jni_cffi.JNI_ERR
    assert -2 == jni_capi.JNI_EDETACHED == jni_ctypes.JNI_EDETACHED == jni_cffi.JNI_EDETACHED
    assert -3 == jni_capi.JNI_EVERSION  == jni_ctypes.JNI_EVERSION  == jni_cffi.JNI_EVERSION
    assert -4 == jni_capi.JNI_ENOMEM    == jni_ctypes.JNI_ENOMEM    == jni_cffi.JNI_ENOMEM
    assert -5 == jni_capi.JNI_EEXIST    == jni_ctypes.JNI_EEXIST    == jni_cffi.JNI_EEXIST
    assert -6 == jni_capi.JNI_EINVAL    == jni_ctypes.JNI_EINVAL    == jni_cffi.JNI_EINVAL
    assert int is type(jni_capi.JNI_OK)        is type(jni_ctypes.JNI_OK)        is type(jni_cffi.JNI_OK)
    assert int is type(jni_capi.JNI_ERR)       is type(jni_ctypes.JNI_ERR)       is type(jni_cffi.JNI_ERR)
    assert int is type(jni_capi.JNI_EDETACHED) is type(jni_ctypes.JNI_EDETACHED) is type(jni_cffi.JNI_EDETACHED)
    assert int is type(jni_capi.JNI_EVERSION)  is type(jni_ctypes.JNI_EVERSION)  is type(jni_cffi.JNI_EVERSION)
    assert int is type(jni_capi.JNI_ENOMEM)    is type(jni_ctypes.JNI_ENOMEM)    is type(jni_cffi.JNI_ENOMEM)
    assert int is type(jni_capi.JNI_EEXIST)    is type(jni_ctypes.JNI_EEXIST)    is type(jni_cffi.JNI_EEXIST)
    assert int is type(jni_capi.JNI_EINVAL)    is type(jni_ctypes.JNI_EINVAL)    is type(jni_cffi.JNI_EINVAL)

def test_release_mode():
    assert 1 == jni_capi.JNI_COMMIT == jni_ctypes.JNI_COMMIT == jni_cffi.JNI_COMMIT
    assert 2 == jni_capi.JNI_ABORT  == jni_ctypes.JNI_ABORT  == jni_cffi.JNI_ABORT 
    assert int is type(jni_capi.JNI_COMMIT) is type(jni_ctypes.JNI_COMMIT) is type(jni_cffi.JNI_COMMIT)
    assert int is type(jni_capi.JNI_ABORT)  is type(jni_ctypes.JNI_ABORT)  is type(jni_cffi.JNI_ABORT)

def test_VM_specific():
    assert 1 == jni_capi.JDK1_2 == jni_ctypes.JDK1_2 == jni_cffi.JDK1_2
    assert 1 == jni_capi.JDK1_4 == jni_ctypes.JDK1_4 == jni_cffi.JDK1_4 
    assert int is type(jni_capi.JDK1_2) is type(jni_ctypes.JDK1_2) is type(jni_cffi.JDK1_2)
    assert int is type(jni_capi.JDK1_4) is type(jni_ctypes.JDK1_4) is type(jni_cffi.JDK1_4)

def test_JNI_version_constants():
    assert 0x00010001 == jni_capi.JNI_VERSION_1_1 == jni_ctypes.JNI_VERSION_1_1 == jni_cffi.JNI_VERSION_1_1
    assert 0x00010002 == jni_capi.JNI_VERSION_1_2 == jni_ctypes.JNI_VERSION_1_2 == jni_cffi.JNI_VERSION_1_2
    assert 0x00010004 == jni_capi.JNI_VERSION_1_4 == jni_ctypes.JNI_VERSION_1_4 == jni_cffi.JNI_VERSION_1_4
    assert 0x00010006 == jni_capi.JNI_VERSION_1_6 == jni_ctypes.JNI_VERSION_1_6 == jni_cffi.JNI_VERSION_1_6
    assert 0x00010008 == jni_capi.JNI_VERSION_1_8 == jni_ctypes.JNI_VERSION_1_8 == jni_cffi.JNI_VERSION_1_8
    assert 0x00090000 == jni_capi.JNI_VERSION_9   == jni_ctypes.JNI_VERSION_9   == jni_cffi.JNI_VERSION_9
    assert 0x000a0000 == jni_capi.JNI_VERSION_10  == jni_ctypes.JNI_VERSION_10  == jni_cffi.JNI_VERSION_10
    assert int is type(jni_capi.JNI_VERSION_1_1) is type(jni_ctypes.JNI_VERSION_1_1) is type(jni_cffi.JNI_VERSION_1_1)
    assert int is type(jni_capi.JNI_VERSION_1_2) is type(jni_ctypes.JNI_VERSION_1_2) is type(jni_cffi.JNI_VERSION_1_2)
    assert int is type(jni_capi.JNI_VERSION_1_4) is type(jni_ctypes.JNI_VERSION_1_4) is type(jni_cffi.JNI_VERSION_1_4)
    assert int is type(jni_capi.JNI_VERSION_1_6) is type(jni_ctypes.JNI_VERSION_1_6) is type(jni_cffi.JNI_VERSION_1_6)
    assert int is type(jni_capi.JNI_VERSION_1_8) is type(jni_ctypes.JNI_VERSION_1_8) is type(jni_cffi.JNI_VERSION_1_8)
    assert int is type(jni_capi.JNI_VERSION_9)   is type(jni_ctypes.JNI_VERSION_9)   is type(jni_cffi.JNI_VERSION_9)
    assert int is type(jni_capi.JNI_VERSION_10)  is type(jni_ctypes.JNI_VERSION_10)  is type(jni_cffi.JNI_VERSION_10)

