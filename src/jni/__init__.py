# flake8-in-file-ignores: noqa: E402,F401,F403,F821

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

import ctypes as ct

from .__about__ import * ; del __about__  # type: ignore[name-defined]
from .__about__ import __all__            # type: ignore[attr-defined]
from . import __config__ ; del __config__
from .__config__ import config, set_config  # type: ignore[attr-defined]

__all__ = (
    'JVM', 'JEnv', 'load', 'method', 'JNIException', 'Throwable',
    # Must be provided by the implementation.
    'DLL', 'CFUNC',
    'POINTER', 'pointer', 'byref', 'addressof', 'sizeof', 'py_object', 'memmove', 'cast',
    'obj', 'new', 'new_array', 'new_cstr', 'new_cwstr', 'as_cstr', 'as_cwstr', 'to_bytes',
    'to_unicode', 'from_buffer', 'isNULL', 'NULL',
    # JNI interface
    'JavaVM', 'JNIEnv',
    'jboolean', 'jbyte', 'jchar', 'jshort', 'jint', 'jlong', 'jfloat', 'jdouble', 'jsize',
    'jobject', 'jclass', 'jthrowable', 'jstring', 'jarray', 'jbooleanArray', 'jbyteArray',
    'jcharArray', 'jshortArray', 'jintArray', 'jlongArray', 'jfloatArray', 'jdoubleArray',
    'jobjectArray', 'jweak', 'jvalue', 'jfieldID', 'jmethodID', 'jobjectRefType',
    'JNIInvalidRefType', 'JNILocalRefType', 'JNIGlobalRefType', 'JNIWeakGlobalRefType',
    'JNINativeMethod', 'JavaVMOption', 'JavaVMInitArgs', 'JavaVMAttachArgs',
    'JNI_TRUE', 'JNI_FALSE',
    'JNI_COMMIT', 'JNI_ABORT',
    'JNI_OK', 'JNI_ERR', 'JNI_EDETACHED', 'JNI_EVERSION', 'JNI_ENOMEM', 'JNI_EEXIST', 'JNI_EINVAL',
    'JDK1_2', 'JDK1_4',
    'JNI_VERSION_1_1', 'JNI_VERSION_1_2', 'JNI_VERSION_1_4', 'JNI_VERSION_1_6', 'JNI_VERSION_1_8',
    'JNI_VERSION_9',   'JNI_VERSION_10',  'JNI_VERSION_19',  'JNI_VERSION_20',  'JNI_VERSION_21',
    'JNI_VERSION_24',
    'defined', 'from_oid', 'config',
) + tuple(__all__)

BACKEND = config.get("BACKEND", "ctypes")

try:
    exec(f"from .{BACKEND} import *", globals())
except ImportError:  # pragma: no cover
    raise ImportError(f"Unknown jni backend: {BACKEND}") from None

exec(f"del {BACKEND}", globals())
config = set_config

from utlx import defined
from utlx.platform import from_oid
