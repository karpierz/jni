# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import jni
from jni.java import registerClass


class ExampleBase:

    def initialize(self, jenv: jni.JNIEnv):
        from .pl.python.jni.test import ExampleBase
        registerClass(jenv, "pl.python.jni.test.ExampleBase", ExampleBase)
        jenv.PushLocalFrame(1)
        try:
            jcls = jenv.FindClass(b"pl/python/jni/test/ExampleBase")
            self.Class = jni.cast(jenv.NewGlobalRef(jcls), jni.jclass)
        finally:
            jenv.PopLocalFrame()

    def dispose(self, jenv: jni.JNIEnv):
        jenv.DeleteGlobalRef(self.Class)
