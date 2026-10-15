# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

from pathlib import Path
import os
import enum

import jni

class EStatusCode(enum.IntEnum):
    SUCCESS   = 1000
    UNKNOWN   = 1001
    EXCEPTION = 1002
    HOST      = 1003
    ERR       = jni.JNI_ERR        # unknown error
    EDETACHED = jni.JNI_EDETACHED  # thread detached from the VM
    EVERSION  = jni.JNI_EVERSION   # JNI version error
    ENOMEM    = jni.JNI_ENOMEM     # not enough memory
    EEXIST    = jni.JNI_EEXIST     # VM already created
    EINVAL    = jni.JNI_EINVAL     # invalid arguments


class JVM:
    """Java Virtual Machine"""

    JNI_VERSION = jni.JNI_VERSION_1_8

    def __init__(self, dll_path: object | None = None):
        """Initializer"""

        if_load = dll_path is not None

        self._jvm = None  # _JVM
        self.JavaException = None
        self.ExceptionsMap = {}
        try:
            # TODO: add the non-string parameters, for possible callbacks

            if if_load and not isinstance(dll_path, (str, os.PathLike)):
                raise JVMError(EStatusCode.EINVAL,
                               "First parameter must be a string or os.PathLike type")
            self._jvm = _JVM()
            try:
                self._jvm.JNI = jni.load(dll_path) if if_load else None
            except Exception as exc:
                raise JVMError(EStatusCode.UNKNOWN,
                               f"Unable to load DLL [{dll_path}], error = {exc}") from None
            self._jvm._create()
        except Exception as exc:
            self.handleException(exc)

    def __del__(self):
        """Finalizer"""
        if not self._jvm: return
        try: self._jvm.jnijvm.DestroyJavaVM()
        except Exception: pass
        self._jvm.jnijvm = None
        try: self._jvm.JNI.dllclose()
        except Exception: pass
        self._jvm.JNI = None

    def start(self, *jvmoptions, **jvmargs) -> tuple[_JVM, jni.JNIEnv]:
        ignoreUnrecognized = jvmargs.get("ignoreUnrecognized", True)
        try:
            pjvm = jni.obj(jni.POINTER(jni.JavaVM))
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            jvm_args = jni.obj(jni.JavaVMInitArgs)
            jvm_args.version  = JVM.JNI_VERSION
            jvm_args.nOptions = len(jvmoptions)
            jvm_args.options  = joptions = jni.new_array(jni.JavaVMOption, jvm_args.nOptions)
            _keep = []
            for i, option in enumerate(jvmoptions):
                optionString = jni.new_cstr(option if isinstance(option, bytes)
                                            else str(option).encode())
                _keep.append(optionString)
                jvm_args.options[i].optionString = optionString
                jvm_args.options[i].extraInfo    = jni.NULL
            jvm_args.ignoreUnrecognized = jni.JNI_TRUE if ignoreUnrecognized else jni.JNI_FALSE
            err = self._jvm.JNI.CreateJavaVM(pjvm, penv, jvm_args)
            del _keep, joptions, jvm_args
            if err != jni.JNI_OK or jni.isNULL(pjvm):  # pragma: no cover
                raise jni.JNIException(err if err != jni.JNI_OK else jni.JNI_ERR,
                                       info="JNI_CreateJavaVM")
            self._jvm.jnijvm = jni.JVM(pjvm)
            jenv = jni.JEnv(penv)
            try:
                self._jvm._initialize(jenv)
            except Exception as exc:  # pragma: no cover
                try: self._jvm.jnijvm.DestroyJavaVM()
                except Exception: pass
                raise exc
            return self._jvm, jenv
        except Exception as exc:  # pragma: no cover
            try:
                self.handleException(exc)
            finally:
                self._jvm.jnijvm = None

    def shutdown(self):
        if self._jvm.jnijvm is None:
            return  # pragma: no cover
        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            self._jvm.jnijvm.AttachCurrentThread(penv)
            jenv = jni.JEnv(penv)
            self._jvm._dispose(jenv)
            self._jvm.jnijvm.DestroyJavaVM()
        except Exception as exc:  # pragma: no cover
            try:
                self.handleException(exc)
            finally:
                self._jvm.jnijvm = None

    def isStarted(self) -> bool:
        # Check if the JVM environment has been initialized
        return self._jvm is not None and self._jvm.jnijvm is not None

    def handleException(self, exc):
        try:
            raise exc
        except jni.Throwable as exc:  # pragma: no cover
            self.JException.printDescribe()
            jexc = self.JException(exc)
            if self.JavaException and hasattr(self.JavaException, "__exception__"):
                raise self.JavaException.__exception__(jexc) from None
            else:
                classname = jexc.getClass().getName()
                message   = jexc.getMessage()
                if message is None: message = classname
                PyExc = self.JavaException or RuntimeError
                raise PyExc(f"Java exception {classname} occurred: {message}") from None
        except jni.JNIException as exc:  # pragma: no cover
            PyExc = self.ExceptionsMap.get(exc.getError(),
                                           self.ExceptionsMap.get(EStatusCode.ERR, RuntimeError))
            raise PyExc(exc.getMessage()) from None
        except JVMError as exc:
            PyExc = self.ExceptionsMap.get(exc.args[0],
                                           self.ExceptionsMap.get(EStatusCode.ERR, RuntimeError))
            raise PyExc(exc.args[1]) from None
        except Exception:  # pragma: no cover
            PyExc = self.ExceptionsMap.get(None)
            raise (PyExc(exc) if PyExc else exc) from None


class JVMError(Exception):

    def __init__(self, *args, **kwargs):
        """Initializer"""
        super().__init__(*args, **kwargs)


class _JVM:

    def __init__(self):
        """Initializer"""
        super().__init__()
        self.JNI:    jni.JNI    = None
        self.jnijvm: jni.JavaVM = None

    def _create(self):
        pass

    def _initialize(self, jenv: jni.JNIEnv):
        pass

    def _dispose(self, jenv: jni.JNIEnv):
        pass
