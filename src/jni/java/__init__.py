# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

__all__ = ("registerClass", "registerNatives", "unregisterNatives", "throwJavaException")

from typing import Any
from typing_extensions import Buffer
from collections.abc import Sequence
import types
import inspect

from .. import JNIEnv, JNINativeMethod, jclass, jobject


def registerClass(jenv: JNIEnv, class_name: str | bytes,
                  class_code: types.ModuleType | type | Buffer,
                  native_methods: Sequence[JNINativeMethod] | None = None,
                  class_loader: jobject | None = None) -> None:

    from .. import POINTER, cast, new_array, jbyte, from_buffer

    if isinstance(class_name, str):
        class_name = class_name.encode()

    if inspect.ismodule(class_code) or inspect.isclass(class_code):
        if native_methods is None:
            native_methods = getattr(class_code, "__jnimethods__", ())
        java_class_code = getattr(class_code, "__javacode__")
        if not isinstance(java_class_code, Buffer):
            raise TypeError("class_code.__javacode__ must be a buffer-compatible object")
    else:
        java_class_code = class_code
    if native_methods is None: native_methods = ()

    jenv.PushLocalFrame(3)
    try:
        if class_loader is None:
            jcls = jenv.FindClass(b"java/lang/ClassLoader")
            jmid = jenv.GetStaticMethodID(jcls, b"getSystemClassLoader",
                                                b"()Ljava/lang/ClassLoader;")
            class_loader = jenv.CallStaticObjectMethod(jcls, jmid)

        try:
            jcls = jenv.FindClass(class_name.replace(b".", b"/"))
        except Exception:
            size = len(java_class_code)
            jcls = jenv.DefineClass(class_name.replace(b".", b"/"),
                                    class_loader,
                                    cast(from_buffer(java_class_code), POINTER(jbyte)),
                                    size)
        methods = new_array(JNINativeMethod, len(native_methods))
        for idx, method in enumerate(native_methods):
            methods[idx] = method
        jenv.RegisterNatives(jcls, cast(methods, POINTER(JNINativeMethod)), len(methods))
    finally:
        jenv.PopLocalFrame()


def registerNatives(jenv: JNIEnv, class_name: str | bytes,
                    native_methods: Sequence[JNINativeMethod]) -> None:

    from .. import POINTER, cast, new_array

    if isinstance(class_name, str):
        class_name = class_name.encode()

    if inspect.ismodule(native_methods) or inspect.isclass(native_methods):
        native_methods = getattr(native_methods, "__jnimethods__", ())
    if native_methods is None: native_methods = ()

    jenv.PushLocalFrame(1)
    try:
        jcls = jenv.FindClass(class_name.replace(b".", b"/"))
        methods = new_array(JNINativeMethod, len(native_methods))
        for idx, method in enumerate(native_methods):
            methods[idx] = method
        jenv.RegisterNatives(jcls, cast(methods, POINTER(JNINativeMethod)), len(methods))
    finally:
        jenv.PopLocalFrame()


def unregisterNatives(jenv: JNIEnv, class_name: str | bytes) -> None:

    if isinstance(class_name, str):
        class_name = class_name.encode()

    jenv.PushLocalFrame(1)
    try:
        jcls = jenv.FindClass(class_name.replace(b".", b"/"))
        jenv.UnregisterNatives(jcls)
    finally:
        jenv.PopLocalFrame()


def throwJavaException(jenv: JNIEnv,
                       jecls: str | bytes | jclass | jobject, message: Any) -> None:

    if not isinstance(message, bytes):
        message = str(message).encode()

    if isinstance(jecls, (str, bytes)):
        class_name = jecls if isinstance(jecls, bytes) else jecls.encode()
        jenv.PushLocalFrame(1)
        try:
            jecls = jenv.FindClass(class_name.replace(b".", b"/"))
            jenv.ThrowNew(jecls, message)
        finally:
            jenv.PopLocalFrame()
    else:
        jenv.ThrowNew(jecls, message)
