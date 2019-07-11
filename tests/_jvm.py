# Copyright (c) 2004-2019 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from jt import jni


class JVM(object):

    """Java Virtual Machine"""

    JNI_VERSION = jni.JNI_VERSION_1_6

    def __init__(self, dll_path):

        self._jnijvm = None
        try:
            if not isinstance(dll_path, (str, type(u""))):
                raise JVMException(jni.JNI_EINVAL,
                                   "First paramter must be a string or unicode")
            try:
                self._JNI = jni.load(dll_path)
            except Exception as exc:
                raise JVMException(1001,
                                   "Unable to load DLL [{}], error = {}".format(dll_path, exc))
        except Exception as exc:
            self.handleException(exc)

    def __del__(self):

        if not self._jnijvm: return
        try: self._jnijvm.DestroyJavaVM()
        except: pass
        self._jnijvm = None
        try: self._JNI.dllclose()
        except: pass
        self._JNI = None

    def start(self, *jvmoptions, **jvmargs):

        ignoreUnrecognized = jvmargs.get("ignoreUnrecognized", True)

        try:
            pjvm = jni.obj(jni.POINTER(jni.JavaVM))
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            jvm_args = jni.obj(jni.JavaVMInitArgs)
            jvm_args.version  = JVM.JNI_VERSION
            jvm_args.nOptions = len(jvmoptions)
            jvm_args.options  = options = jni.new_array(jni.JavaVMOption, jvm_args.nOptions)
            _keep = []
            for i, option in enumerate(jvmoptions):
                optionString = jni.new_cstr(option if isinstance(option, bytes)
                                            else str(option).encode("utf-8"))
                _keep.append(optionString)
                jvm_args.options[i].optionString = optionString
                jvm_args.options[i].extraInfo    = jni.NULL
            jvm_args.ignoreUnrecognized = jni.JNI_TRUE if ignoreUnrecognized else jni.JNI_FALSE
            err = self._JNI.CreateJavaVM(pjvm, penv, jvm_args)
            del _keep, options, jvm_args
            if err != jni.JNI_OK or jni.isNULL(pjvm):
                raise jni.JNIException(err, info="JNI_CreateJavaVM")
            self._jnijvm = jni.JVM(pjvm)
            return self._jnijvm, jni.JEnv(penv)
        except Exception as exc:
            try:
                self.handleException(exc)
            finally:
                self._jnijvm = None

    def shutdown(self):

        if self._jnijvm is None: return
        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            self._jnijvm.AttachCurrentThread(penv)
            self._jnijvm.DestroyJavaVM()
        except Exception as exc:
            try:
                self.handleException(exc)
            finally:
                self._jnijvm = None

    def isStarted(self):

        # Check if the JVM environment has been initialized
        return self._jnijvm is not None

    def attachThread(self, daemon=False):

        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            if not daemon:
                self._jnijvm.AttachCurrentThread(penv)
            else:
                self._jnijvm.AttachCurrentThreadAsDaemon(penv)
            return self._jnijvm, jni.JEnv(penv)
        except Exception as exc:
            self.handleException(exc)

    def detachThread(self):

        try:
            self._jnijvm.DetachCurrentThread()
        except Exception as exc:
            self.handleException(exc)

    def isThreadAttached(self):

        try:
            penv = jni.obj(jni.POINTER(jni.JNIEnv))
            self._jnijvm.GetEnv(penv, JVM.JNI_VERSION)
        except jni.JNIException as exc:
            if exc.getError() == jni.JNI_EDETACHED:
                return False
            self.handleException(exc)
        except Exception as exc:
            self.handleException(exc)
        else:
            return not jni.isNULL(penv)

    def handleException(self, exc):

        try:
            raise exc
        except jni.Throwable as exc:
            self.JException.printDescribe()
            jexc = self.JException(exc)
            classname = jexc.getClass().getName()
            message   = jexc.getMessage()
            raise RuntimeError(u"Java exception {} occurred: {}".format(classname,
                               message if message is not None else classname))
        except jni.JNIException as exc:
            raise RuntimeError(exc.getMessage())
        except JVMException as exc:
            raise RuntimeError(exc.args[1])
        except:
            raise exc


class JVMException(Exception):

    def __init__(self, *args, **kwargs):
        super(JVMException, self).__init__(*args, **kwargs)
