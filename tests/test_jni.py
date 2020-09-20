# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional
import unittest
import sys
import os
import math


class JNITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from . import jvm
        cls.jvm    = jvm
        cls.JNI    = jvm._JNI
        cls.jnijvm = jvm._jnijvm

    def setUp(self):
        import jni
        penv = jni.obj(jni.POINTER(jni.JNIEnv))
        self.jnijvm.GetEnv(penv, self.jvm.JNI_VERSION)
        self.jenv = jni.JEnv(penv)

    def test_JNI_constants(self):

        import jni

        # jobjectRefType constants
        self.assertIs(type(jni.JNIInvalidRefType),    int)
        self.assertIs(type(jni.JNILocalRefType),      int)
        self.assertIs(type(jni.JNIGlobalRefType),     int)
        self.assertIs(type(jni.JNIWeakGlobalRefType), int)
        self.assertEqual(jni.JNIInvalidRefType,    0) 
        self.assertEqual(jni.JNILocalRefType,      1) 
        self.assertEqual(jni.JNIGlobalRefType,     2) 
        self.assertEqual(jni.JNIWeakGlobalRefType, 3) 

        # jboolean constants
        self.assertIs(type(jni.JNI_FALSE), int)
        self.assertIs(type(jni.JNI_TRUE),  int)
        self.assertEqual(jni.JNI_FALSE, False)
        self.assertEqual(jni.JNI_TRUE,  True)

        # possible return values constants
        self.assertIs(type(jni.JNI_OK),        int)
        self.assertIs(type(jni.JNI_ERR),       int)
        self.assertIs(type(jni.JNI_EDETACHED), int)
        self.assertIs(type(jni.JNI_EVERSION),  int)
        self.assertIs(type(jni.JNI_ENOMEM),    int)
        self.assertIs(type(jni.JNI_EEXIST),    int)
        self.assertIs(type(jni.JNI_EINVAL),    int)
        self.assertEqual(jni.JNI_OK,         0)
        self.assertEqual(jni.JNI_ERR,       -1)
        self.assertEqual(jni.JNI_EDETACHED, -2)
        self.assertEqual(jni.JNI_EVERSION,  -3)
        self.assertEqual(jni.JNI_ENOMEM,    -4)
        self.assertEqual(jni.JNI_EEXIST,    -5)
        self.assertEqual(jni.JNI_EINVAL,    -6)

        # release mode constants
        self.assertIs(type(jni.JNI_COMMIT), int)
        self.assertIs(type(jni.JNI_ABORT),  int)
        self.assertEqual(jni.JNI_COMMIT, 1)
        self.assertEqual(jni.JNI_ABORT,  2)

        # VM specific constants
        self.assertIs(type(jni.JDK1_2), int)
        self.assertIs(type(jni.JDK1_4), int)
        self.assertEqual(jni.JDK1_2, 1)
        self.assertEqual(jni.JDK1_4, 1)

        # JNI version constants
        self.assertIs(type(jni.JNI_VERSION_1_1), int)
        self.assertIs(type(jni.JNI_VERSION_1_2), int)
        self.assertIs(type(jni.JNI_VERSION_1_4), int)
        self.assertIs(type(jni.JNI_VERSION_1_6), int)
        self.assertIs(type(jni.JNI_VERSION_1_8), int)
        self.assertIs(type(jni.JNI_VERSION_9),   int)
        self.assertIs(type(jni.JNI_VERSION_10),  int)
        self.assertEqual(jni.JNI_VERSION_1_1, 0x00010001)
        self.assertEqual(jni.JNI_VERSION_1_2, 0x00010002)
        self.assertEqual(jni.JNI_VERSION_1_4, 0x00010004)
        self.assertEqual(jni.JNI_VERSION_1_6, 0x00010006)
        self.assertEqual(jni.JNI_VERSION_1_8, 0x00010008)
        self.assertEqual(jni.JNI_VERSION_9,   0x00090000)
        self.assertEqual(jni.JNI_VERSION_10,  0x000a0000)

    def test_jvm(self):

        import jni

        with self.assertRaises(OSError):
            JNI = jni.load(None)
        with self.assertRaises(OSError):
            JNI = jni.load("")
        with self.assertRaises(OSError):
            here = os.path.dirname(os.path.abspath(__file__))
            JNI = jni.load(os.path.join(here, "non-existent"))
        with self.assertRaises(OSError):
            JNI = jni.load(os.path.abspath(__file__))

        self.assertTrue(hasattr(self.JNI, "GetDefaultJavaVMInitArgs"))
        self.assertTrue(hasattr(self.JNI, "CreateJavaVM"))
        self.assertTrue(hasattr(self.JNI, "GetCreatedJavaVMs"))

        jni_version = self.jenv.GetVersion()
        self.assertIs(type(jni_version), int)
        self.assertNotEqual(jni_version, 0)
        self.assertIn(jni_version, (jni.JNI_VERSION_1_1,
                                    jni.JNI_VERSION_1_2,
                                    jni.JNI_VERSION_1_4,
                                    jni.JNI_VERSION_1_6,
                                    jni.JNI_VERSION_1_8,
                                    jni.JNI_VERSION_9,
                                    jni.JNI_VERSION_10))

    def test_classes(self):

        import jni

        String = self.jenv.FindClass(b"java/lang/String")
        self.assertTrue(String)
        String_super = self.jenv.GetSuperclass(String)
        self.assertTrue(String_super)

        Object = self.jenv.FindClass(b"java/lang/Object")
        self.assertTrue(Object)
        Object_super = self.jenv.GetSuperclass(Object)
        self.assertIs(Object_super, None)

        self.assertFalse(self.jenv.IsSameObject(String, Object))
        self.assertTrue(self.jenv.IsSameObject(String_super, Object))

        self.assertTrue(self.jenv.IsAssignableFrom(String, Object))
        self.assertFalse(self.jenv.IsAssignableFrom(Object, String))

        Field       = self.jenv.FindClass(b"java/lang/reflect/Field")
        Constructor = self.jenv.FindClass(b"java/lang/reflect/Constructor")
        Method      = self.jenv.FindClass(b"java/lang/reflect/Method")
        self.assertTrue(Field)
        self.assertTrue(Constructor)
        self.assertTrue(Method)

    def test_non_existent(self):
        """Non-existent classes/methods/fields return None from Find/Get APIs"""

        import jni

        # A class that doesn't exist
        with self.assertRaises(jni.Throwable):
            UnknownClass = self.jenv.FindClass(b"java/XXX")

        # A class that does exist, that we can then search for
        # non-existent Fields and Methods
        Example = self.jenv.FindClass(b"org/jt/jni/test/Example")
        self.assertTrue(Example)

        # Non existent Fields and Methods (static and non-static)
        with self.assertRaises(jni.Throwable):
            self.jenv.GetFieldID(Example, b"xxx", b"I")
        with self.assertRaises(jni.Throwable):
            self.jenv.GetStaticFieldID(Example, b"xxx", b"I")
        with self.assertRaises(jni.Throwable):
            self.jenv.GetMethodID(Example, b"xxx", b"()V")
        with self.assertRaises(jni.Throwable):
            self.jenv.GetStaticMethodID(Example, b"xxx", b"()V")

        # Bad signatures for existing Fields/Methods also fail.
        with self.assertRaises(jni.Throwable):
            self.jenv.GetFieldID(Example, b"int_field", b"D")
        with self.assertRaises(jni.Throwable):
            self.jenv.GetStaticFieldID(Example, b"static_int_field", b"D")
        with self.assertRaises(jni.Throwable):
            self.jenv.GetMethodID(Example, b"get_int_field", b"()D")
        with self.assertRaises(jni.Throwable):
            self.jenv.GetStaticMethodID(Example, b"get_static_int_field", b"()D")

    def test_object_lifecycle(self):
        """The basic lifecycle operations of an object can be performed"""

        import jni

        # Get a reference to the org.jt.jni.test.Example class
        Example = self.jenv.FindClass(b"org/jt/jni/test/Example")
        self.assertTrue(Example)

        # Find the default constructor
        Example__init = self.jenv.GetMethodID(Example, b"<init>", b"()V")
        # Find the 'one int' constructor
        Example__init_i = self.jenv.GetMethodID(Example, b"<init>", b"(I)V")
        # Find the 'two int' constructor
        Example__init_ii = self.jenv.GetMethodID(Example, b"<init>", b"(II)V")
        self.assertTrue(Example__init)
        self.assertTrue(Example__init_i)
        self.assertTrue(Example__init_ii)

        # Find Example.base_<type>_field
        Example__base_boolean_field = self.jenv.GetFieldID(Example, b"base_boolean_field", b"Z")
        Example__base_char_field    = self.jenv.GetFieldID(Example, b"base_char_field",    b"C")
        Example__base_byte_field    = self.jenv.GetFieldID(Example, b"base_byte_field",    b"B")
        Example__base_short_field   = self.jenv.GetFieldID(Example, b"base_short_field",   b"S")
        Example__base_int_field     = self.jenv.GetFieldID(Example, b"base_int_field",     b"I")
        Example__base_long_field    = self.jenv.GetFieldID(Example, b"base_long_field",    b"J")
        Example__base_float_field   = self.jenv.GetFieldID(Example, b"base_float_field",   b"F")
        Example__base_double_field  = self.jenv.GetFieldID(Example, b"base_double_field",  b"D")
        Example__base_String_field  = self.jenv.GetFieldID(Example, b"base_String_field",  b"Ljava/lang/String;")
        self.assertTrue(Example__base_boolean_field)
        self.assertTrue(Example__base_char_field)
        self.assertTrue(Example__base_byte_field)
        self.assertTrue(Example__base_short_field)
        self.assertTrue(Example__base_int_field)
        self.assertTrue(Example__base_long_field)
        self.assertTrue(Example__base_float_field)
        self.assertTrue(Example__base_double_field)
        self.assertTrue(Example__base_String_field)

        # Find Example.<type>_field
        Example__boolean_field = self.jenv.GetFieldID(Example, b"boolean_field", b"Z")
        Example__char_field    = self.jenv.GetFieldID(Example, b"char_field",    b"C")
        Example__byte_field    = self.jenv.GetFieldID(Example, b"byte_field",    b"B")
        Example__short_field   = self.jenv.GetFieldID(Example, b"short_field",   b"S")
        Example__int_field     = self.jenv.GetFieldID(Example, b"int_field",     b"I")
        Example__long_field    = self.jenv.GetFieldID(Example, b"long_field",    b"J")
        Example__float_field   = self.jenv.GetFieldID(Example, b"float_field",   b"F")
        Example__double_field  = self.jenv.GetFieldID(Example, b"double_field",  b"D")
        Example__String_field  = self.jenv.GetFieldID(Example, b"String_field",  b"Ljava/lang/String;")
        self.assertTrue(Example__boolean_field)
        self.assertTrue(Example__char_field)
        self.assertTrue(Example__byte_field)
        self.assertTrue(Example__short_field)
        self.assertTrue(Example__int_field)
        self.assertTrue(Example__long_field)
        self.assertTrue(Example__float_field)
        self.assertTrue(Example__double_field)
        self.assertTrue(Example__String_field)

        # Find the BaseExample.get_base_<type>_field() and BaseExample.set_base_<type>_field() methods on Example
        Example__get_base_boolean_field = self.jenv.GetMethodID(Example, b"get_base_boolean_field", b"()Z")
        Example__set_base_boolean_field = self.jenv.GetMethodID(Example, b"set_base_boolean_field", b"(Z)V")
        Example__get_base_char_field    = self.jenv.GetMethodID(Example, b"get_base_char_field",    b"()C")
        Example__set_base_char_field    = self.jenv.GetMethodID(Example, b"set_base_char_field",    b"(C)V")
        Example__get_base_byte_field    = self.jenv.GetMethodID(Example, b"get_base_byte_field",    b"()B")
        Example__set_base_byte_field    = self.jenv.GetMethodID(Example, b"set_base_byte_field",    b"(B)V")
        Example__get_base_short_field   = self.jenv.GetMethodID(Example, b"get_base_short_field",   b"()S")
        Example__set_base_short_field   = self.jenv.GetMethodID(Example, b"set_base_short_field",   b"(S)V")
        Example__get_base_int_field     = self.jenv.GetMethodID(Example, b"get_base_int_field",     b"()I")
        Example__set_base_int_field     = self.jenv.GetMethodID(Example, b"set_base_int_field",     b"(I)V")
        Example__get_base_long_field    = self.jenv.GetMethodID(Example, b"get_base_long_field",    b"()J")
        Example__set_base_long_field    = self.jenv.GetMethodID(Example, b"set_base_long_field",    b"(J)V")
        Example__get_base_float_field   = self.jenv.GetMethodID(Example, b"get_base_float_field",   b"()F")
        Example__set_base_float_field   = self.jenv.GetMethodID(Example, b"set_base_float_field",   b"(F)V")
        Example__get_base_double_field  = self.jenv.GetMethodID(Example, b"get_base_double_field",  b"()D")
        Example__set_base_double_field  = self.jenv.GetMethodID(Example, b"set_base_double_field",  b"(D)V")
        Example__get_base_String_field  = self.jenv.GetMethodID(Example, b"get_base_String_field",  b"()Ljava/lang/String;")
        Example__set_base_String_field  = self.jenv.GetMethodID(Example, b"set_base_String_field",  b"(Ljava/lang/String;)V")
        self.assertTrue(Example__get_base_boolean_field)
        self.assertTrue(Example__set_base_boolean_field)
        self.assertTrue(Example__get_base_char_field)
        self.assertTrue(Example__set_base_char_field)
        self.assertTrue(Example__get_base_byte_field)
        self.assertTrue(Example__set_base_byte_field)
        self.assertTrue(Example__get_base_short_field)
        self.assertTrue(Example__set_base_short_field)
        self.assertTrue(Example__get_base_int_field)
        self.assertTrue(Example__set_base_int_field)
        self.assertTrue(Example__get_base_long_field)
        self.assertTrue(Example__set_base_long_field)
        self.assertTrue(Example__get_base_float_field)
        self.assertTrue(Example__set_base_float_field)
        self.assertTrue(Example__get_base_double_field)
        self.assertTrue(Example__set_base_double_field)
        self.assertTrue(Example__get_base_String_field)
        self.assertTrue(Example__set_base_String_field)

        # Find the Example.get_<type>_field() and Example.set_<type>_field() methods
        Example__get_boolean_field = self.jenv.GetMethodID(Example, b"get_boolean_field", b"()Z")
        Example__set_boolean_field = self.jenv.GetMethodID(Example, b"set_boolean_field", b"(Z)V")
        Example__get_char_field    = self.jenv.GetMethodID(Example, b"get_char_field",    b"()C")
        Example__set_char_field    = self.jenv.GetMethodID(Example, b"set_char_field",    b"(C)V")
        Example__get_byte_field    = self.jenv.GetMethodID(Example, b"get_byte_field",    b"()B")
        Example__set_byte_field    = self.jenv.GetMethodID(Example, b"set_byte_field",    b"(B)V")
        Example__get_short_field   = self.jenv.GetMethodID(Example, b"get_short_field",   b"()S")
        Example__set_short_field   = self.jenv.GetMethodID(Example, b"set_short_field",   b"(S)V")
        Example__get_int_field     = self.jenv.GetMethodID(Example, b"get_int_field",     b"()I")
        Example__set_int_field     = self.jenv.GetMethodID(Example, b"set_int_field",     b"(I)V")
        Example__get_long_field    = self.jenv.GetMethodID(Example, b"get_long_field",    b"()J")
        Example__set_long_field    = self.jenv.GetMethodID(Example, b"set_long_field",    b"(J)V")
        Example__get_float_field   = self.jenv.GetMethodID(Example, b"get_float_field",   b"()F")
        Example__set_float_field   = self.jenv.GetMethodID(Example, b"set_float_field",   b"(F)V")
        Example__get_double_field  = self.jenv.GetMethodID(Example, b"get_double_field",  b"()D")
        Example__set_double_field  = self.jenv.GetMethodID(Example, b"set_double_field",  b"(D)V")
        Example__get_String_field  = self.jenv.GetMethodID(Example, b"get_String_field",  b"()Ljava/lang/String;")
        Example__set_String_field  = self.jenv.GetMethodID(Example, b"set_String_field",  b"(Ljava/lang/String;)V")
        self.assertTrue(Example__get_boolean_field)
        self.assertTrue(Example__set_boolean_field)
        self.assertTrue(Example__get_char_field)
        self.assertTrue(Example__set_char_field)
        self.assertTrue(Example__get_byte_field)
        self.assertTrue(Example__set_byte_field)
        self.assertTrue(Example__get_short_field)
        self.assertTrue(Example__set_short_field)
        self.assertTrue(Example__get_int_field)
        self.assertTrue(Example__set_int_field)
        self.assertTrue(Example__get_long_field)
        self.assertTrue(Example__set_long_field)
        self.assertTrue(Example__get_float_field)
        self.assertTrue(Example__set_float_field)
        self.assertTrue(Example__get_double_field)
        self.assertTrue(Example__set_double_field)
        self.assertTrue(Example__get_String_field)
        self.assertTrue(Example__set_String_field)

        # Create an instance of org.jt.jni.test.Example using the default constructor
        obj1 = self.jenv.NewObject(Example, Example__init)
        self.assertTrue(obj1)

        # Use the get_base_<type>_field and get_<type>_field methods

        self.assertEqual(self.jenv.CallBooleanMethod(obj1, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj1, Example__get_base_char_field), u'\u0016')
        self.assertEqual(self.jenv.CallByteMethod(obj1, Example__get_base_byte_field), 22)
        self.assertEqual(self.jenv.CallShortMethod(obj1, Example__get_base_short_field), 22)
        self.assertEqual(self.jenv.CallIntMethod(obj1, Example__get_base_int_field), 22)
        self.assertEqual(self.jenv.CallLongMethod(obj1, Example__get_base_long_field), 22)
        self.assertEqual(self.jenv.CallFloatMethod(obj1, Example__get_base_float_field), 22.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj1, Example__get_base_double_field), 22.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj1, Example__get_base_String_field)), "22")

        self.assertEqual(self.jenv.CallBooleanMethod(obj1, Example__get_boolean_field), False)
        self.assertEqual(self.jenv.CallCharMethod(obj1, Example__get_char_field), u'\u0021')
        self.assertEqual(self.jenv.CallByteMethod(obj1, Example__get_byte_field), 33)
        self.assertEqual(self.jenv.CallShortMethod(obj1, Example__get_short_field), 33)
        self.assertEqual(self.jenv.CallIntMethod(obj1, Example__get_int_field), 33)
        self.assertEqual(self.jenv.CallLongMethod(obj1, Example__get_long_field), 33)
        self.assertEqual(self.jenv.CallFloatMethod(obj1, Example__get_float_field), 33.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj1, Example__get_double_field), 33.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj1, Example__get_String_field)), "33")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj1, Example, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj1, Example, Example__get_base_char_field), u'\u0016')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj1, Example, Example__get_base_byte_field), 22)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj1, Example, Example__get_base_short_field), 22)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj1, Example, Example__get_base_int_field), 22)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj1, Example, Example__get_base_long_field), 22)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj1, Example, Example__get_base_float_field), 22.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj1, Example, Example__get_base_double_field), 22.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj1, Example, Example__get_base_String_field)), "22")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj1, Example, Example__get_boolean_field), False)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj1, Example, Example__get_char_field), u'\u0021')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj1, Example, Example__get_byte_field), 33)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj1, Example, Example__get_short_field), 33)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj1, Example, Example__get_int_field), 33)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj1, Example, Example__get_long_field), 33)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj1, Example, Example__get_float_field), 33.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj1, Example, Example__get_double_field), 33.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj1, Example, Example__get_String_field)), "33")

        self.assertEqual(self.jenv.GetBooleanField(obj1, Example__base_boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj1, Example__base_char_field), u'\u0016')
        self.assertEqual(self.jenv.GetByteField(obj1, Example__base_byte_field), 22)
        self.assertEqual(self.jenv.GetShortField(obj1, Example__base_short_field), 22)
        self.assertEqual(self.jenv.GetIntField(obj1, Example__base_int_field), 22)
        self.assertEqual(self.jenv.GetLongField(obj1, Example__base_long_field), 22)
        self.assertEqual(self.jenv.GetFloatField(obj1, Example__base_float_field), 22.0)
        self.assertEqual(self.jenv.GetDoubleField(obj1, Example__base_double_field), 22.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj1, Example__base_String_field)), "22")

        self.assertEqual(self.jenv.GetBooleanField(obj1, Example__boolean_field), False)
        self.assertEqual(self.jenv.GetCharField(obj1, Example__char_field), u'\u0021')
        self.assertEqual(self.jenv.GetByteField(obj1, Example__byte_field), 33)
        self.assertEqual(self.jenv.GetShortField(obj1, Example__short_field), 33)
        self.assertEqual(self.jenv.GetIntField(obj1, Example__int_field), 33)
        self.assertEqual(self.jenv.GetLongField(obj1, Example__long_field), 33)
        self.assertEqual(self.jenv.GetFloatField(obj1, Example__float_field), 33.0)
        self.assertEqual(self.jenv.GetDoubleField(obj1, Example__double_field), 33.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj1, Example__String_field)), "33")

        # Use the set_base_<type>_field and set_<type>_field methods

        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].z = False
        self.jenv.CallVoidMethod(obj1, Example__set_base_boolean_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].c = u'\u0471'
        self.jenv.CallVoidMethod(obj1, Example__set_base_char_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].b = 37
        self.jenv.CallVoidMethod(obj1, Example__set_base_byte_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].s = 1137
        self.jenv.CallVoidMethod(obj1, Example__set_base_short_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].i = 1137
        self.jenv.CallVoidMethod(obj1, Example__set_base_int_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].j = 1137
        self.jenv.CallVoidMethod(obj1, Example__set_base_long_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].f = 1137
        self.jenv.CallVoidMethod(obj1, Example__set_base_float_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].d = 1137
        self.jenv.CallVoidMethod(obj1, Example__set_base_double_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].l = self.jenv.NewStringUTF("1137".encode("utf-8"))
        self.jenv.CallVoidMethod(obj1, Example__set_base_String_field, jargs)

        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].z = True
        self.jenv.CallVoidMethod(obj1, Example__set_boolean_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].c = u'\u0476'
        self.jenv.CallVoidMethod(obj1, Example__set_char_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].b = 42
        self.jenv.CallVoidMethod(obj1, Example__set_byte_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].s = 1142
        self.jenv.CallVoidMethod(obj1, Example__set_short_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].i = 1142
        self.jenv.CallVoidMethod(obj1, Example__set_int_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].j = 1142
        self.jenv.CallVoidMethod(obj1, Example__set_long_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].f = 1142
        self.jenv.CallVoidMethod(obj1, Example__set_float_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].d = 1142
        self.jenv.CallVoidMethod(obj1, Example__set_double_field, jargs)
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].l = self.jenv.NewStringUTF("1142".encode("utf-8"))
        self.jenv.CallVoidMethod(obj1, Example__set_String_field, jargs)

        # Confirm that the values have changed

        self.assertEqual(self.jenv.CallBooleanMethod(obj1, Example__get_base_boolean_field), False)
        self.assertEqual(self.jenv.CallCharMethod(obj1, Example__get_base_char_field), u'\u0471')
        self.assertEqual(self.jenv.CallByteMethod(obj1, Example__get_base_byte_field), 37)
        self.assertEqual(self.jenv.CallShortMethod(obj1, Example__get_base_short_field), 1137)
        self.assertEqual(self.jenv.CallIntMethod(obj1, Example__get_base_int_field), 1137)
        self.assertEqual(self.jenv.CallLongMethod(obj1, Example__get_base_long_field), 1137)
        self.assertEqual(self.jenv.CallFloatMethod(obj1, Example__get_base_float_field), 1137.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj1, Example__get_base_double_field), 1137.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj1, Example__get_base_String_field)), "1137")

        self.assertEqual(self.jenv.CallBooleanMethod(obj1, Example__get_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj1, Example__get_char_field), u'\u0476')
        self.assertEqual(self.jenv.CallByteMethod(obj1, Example__get_byte_field), 42)
        self.assertEqual(self.jenv.CallShortMethod(obj1, Example__get_short_field), 1142)
        self.assertEqual(self.jenv.CallIntMethod(obj1, Example__get_int_field), 1142)
        self.assertEqual(self.jenv.CallLongMethod(obj1, Example__get_long_field), 1142)
        self.assertEqual(self.jenv.CallFloatMethod(obj1, Example__get_float_field), 1142.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj1, Example__get_double_field), 1142.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj1, Example__get_String_field)), "1142")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj1, Example, Example__get_base_boolean_field), False)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj1, Example, Example__get_base_char_field), u'\u0471')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj1, Example, Example__get_base_byte_field), 37)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj1, Example, Example__get_base_short_field), 1137)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj1, Example, Example__get_base_int_field), 1137)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj1, Example, Example__get_base_long_field), 1137)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj1, Example, Example__get_base_float_field), 1137.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj1, Example, Example__get_base_double_field), 1137.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj1, Example, Example__get_base_String_field)), "1137")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj1, Example, Example__get_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj1, Example, Example__get_char_field), u'\u0476')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj1, Example, Example__get_byte_field), 42)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj1, Example, Example__get_short_field), 1142)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj1, Example, Example__get_int_field), 1142)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj1, Example, Example__get_long_field), 1142)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj1, Example, Example__get_float_field), 1142.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj1, Example, Example__get_double_field), 1142.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj1, Example, Example__get_String_field)), "1142")

        self.assertEqual(self.jenv.GetBooleanField(obj1, Example__base_boolean_field), False)
        self.assertEqual(self.jenv.GetCharField(obj1, Example__base_char_field), u'\u0471')
        self.assertEqual(self.jenv.GetByteField(obj1, Example__base_byte_field), 37)
        self.assertEqual(self.jenv.GetShortField(obj1, Example__base_short_field), 1137)
        self.assertEqual(self.jenv.GetIntField(obj1, Example__base_int_field), 1137)
        self.assertEqual(self.jenv.GetLongField(obj1, Example__base_long_field), 1137)
        self.assertEqual(self.jenv.GetFloatField(obj1, Example__base_float_field), 1137.0)
        self.assertEqual(self.jenv.GetDoubleField(obj1, Example__base_double_field), 1137.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj1, Example__base_String_field)), "1137")

        self.assertEqual(self.jenv.GetBooleanField(obj1, Example__boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj1, Example__char_field), u'\u0476')
        self.assertEqual(self.jenv.GetByteField(obj1, Example__byte_field), 42)
        self.assertEqual(self.jenv.GetShortField(obj1, Example__short_field), 1142)
        self.assertEqual(self.jenv.GetIntField(obj1, Example__int_field), 1142)
        self.assertEqual(self.jenv.GetLongField(obj1, Example__long_field), 1142)
        self.assertEqual(self.jenv.GetFloatField(obj1, Example__float_field), 1142.0)
        self.assertEqual(self.jenv.GetDoubleField(obj1, Example__double_field), 1142.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj1, Example__String_field)), "1142")

        # Use the Set<Type>Field JNI functions

        self.jenv.SetBooleanField(obj1, Example__base_boolean_field, True)
        self.jenv.SetCharField(obj1, Example__base_char_field, u'\u0485')
        self.jenv.SetByteField(obj1, Example__base_byte_field, 57)
        self.jenv.SetShortField(obj1, Example__base_short_field, 1157)
        self.jenv.SetIntField(obj1, Example__base_int_field, 1157)
        self.jenv.SetLongField(obj1, Example__base_long_field, 1157)
        self.jenv.SetFloatField(obj1, Example__base_float_field, 1157)
        self.jenv.SetDoubleField(obj1, Example__base_double_field, 1157)
        self.jenv.SetObjectField(obj1, Example__base_String_field,
                                 self.jenv.NewStringUTF("1157".encode("utf-8")))

        self.jenv.SetBooleanField(obj1, Example__boolean_field, False)
        self.jenv.SetCharField(obj1, Example__char_field, u'\u048A')
        self.jenv.SetByteField(obj1, Example__byte_field, 62)
        self.jenv.SetShortField(obj1, Example__short_field, 1162)
        self.jenv.SetIntField(obj1, Example__int_field, 1162)
        self.jenv.SetLongField(obj1, Example__long_field, 1162)
        self.jenv.SetFloatField(obj1, Example__float_field, 1162)
        self.jenv.SetDoubleField(obj1, Example__double_field, 1162)
        self.jenv.SetObjectField(obj1, Example__String_field,
                                 self.jenv.NewStringUTF("1162".encode("utf-8")))

        # Confirm that the values have changed

        self.assertEqual(self.jenv.CallBooleanMethod(obj1, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj1, Example__get_base_char_field), u'\u0485')
        self.assertEqual(self.jenv.CallByteMethod(obj1, Example__get_base_byte_field), 57)
        self.assertEqual(self.jenv.CallShortMethod(obj1, Example__get_base_short_field), 1157)
        self.assertEqual(self.jenv.CallIntMethod(obj1, Example__get_base_int_field), 1157)
        self.assertEqual(self.jenv.CallLongMethod(obj1, Example__get_base_long_field), 1157)
        self.assertEqual(self.jenv.CallFloatMethod(obj1, Example__get_base_float_field), 1157.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj1, Example__get_base_double_field), 1157.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj1, Example__get_base_String_field)), "1157")

        self.assertEqual(self.jenv.CallBooleanMethod(obj1, Example__get_boolean_field), False)
        self.assertEqual(self.jenv.CallCharMethod(obj1, Example__get_char_field), u'\u048A')
        self.assertEqual(self.jenv.CallByteMethod(obj1, Example__get_byte_field), 62)
        self.assertEqual(self.jenv.CallShortMethod(obj1, Example__get_short_field), 1162)
        self.assertEqual(self.jenv.CallIntMethod(obj1, Example__get_int_field), 1162)
        self.assertEqual(self.jenv.CallLongMethod(obj1, Example__get_long_field), 1162)
        self.assertEqual(self.jenv.CallFloatMethod(obj1, Example__get_float_field), 1162.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj1, Example__get_double_field), 1162.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj1, Example__get_String_field)), "1162")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj1, Example, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj1, Example, Example__get_base_char_field), u'\u0485')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj1, Example, Example__get_base_byte_field), 57)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj1, Example, Example__get_base_short_field), 1157)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj1, Example, Example__get_base_int_field), 1157)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj1, Example, Example__get_base_long_field), 1157)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj1, Example, Example__get_base_float_field), 1157.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj1, Example, Example__get_base_double_field), 1157.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj1, Example, Example__get_base_String_field)), "1157")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj1, Example, Example__get_boolean_field), False)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj1, Example, Example__get_char_field), u'\u048A')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj1, Example, Example__get_byte_field), 62)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj1, Example, Example__get_short_field), 1162)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj1, Example, Example__get_int_field), 1162)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj1, Example, Example__get_long_field), 1162)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj1, Example, Example__get_float_field), 1162.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj1, Example, Example__get_double_field), 1162.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj1, Example, Example__get_String_field)), "1162")

        self.assertEqual(self.jenv.GetBooleanField(obj1, Example__base_boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj1, Example__base_char_field), u'\u0485')
        self.assertEqual(self.jenv.GetByteField(obj1, Example__base_byte_field), 57)
        self.assertEqual(self.jenv.GetShortField(obj1, Example__base_short_field), 1157)
        self.assertEqual(self.jenv.GetIntField(obj1, Example__base_int_field), 1157)
        self.assertEqual(self.jenv.GetLongField(obj1, Example__base_long_field), 1157)
        self.assertEqual(self.jenv.GetFloatField(obj1, Example__base_float_field), 1157.0)
        self.assertEqual(self.jenv.GetDoubleField(obj1, Example__base_double_field), 1157.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj1, Example__base_String_field)), "1157")

        self.assertEqual(self.jenv.GetBooleanField(obj1, Example__boolean_field), False)
        self.assertEqual(self.jenv.GetCharField(obj1, Example__char_field), u'\u048A')
        self.assertEqual(self.jenv.GetByteField(obj1, Example__byte_field), 62)
        self.assertEqual(self.jenv.GetShortField(obj1, Example__short_field), 1162)
        self.assertEqual(self.jenv.GetIntField(obj1, Example__int_field), 1162)
        self.assertEqual(self.jenv.GetLongField(obj1, Example__long_field), 1162)
        self.assertEqual(self.jenv.GetFloatField(obj1, Example__float_field), 1162.0)
        self.assertEqual(self.jenv.GetDoubleField(obj1, Example__double_field), 1162.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj1, Example__String_field)), "1162")

        # Create an instance of org.jt.jni.test.Example using the "one int" constructor

        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].i = 2242
        obj2 = self.jenv.NewObject(Example, Example__init_i, jargs)
        self.assertTrue(obj2)

        # Check that instance values are as expected

        self.assertEqual(self.jenv.CallBooleanMethod(obj2, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj2, Example__get_base_char_field), u'\u002C')
        self.assertEqual(self.jenv.CallByteMethod(obj2, Example__get_base_byte_field), 44)
        self.assertEqual(self.jenv.CallShortMethod(obj2, Example__get_base_short_field), 44)
        self.assertEqual(self.jenv.CallIntMethod(obj2, Example__get_base_int_field), 44)
        self.assertEqual(self.jenv.CallLongMethod(obj2, Example__get_base_long_field), 44)
        self.assertEqual(self.jenv.CallFloatMethod(obj2, Example__get_base_float_field), 44.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj2, Example__get_base_double_field), 44.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj2, Example__get_base_String_field)), "44")

        self.assertEqual(self.jenv.CallBooleanMethod(obj2, Example__get_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj2, Example__get_char_field), u'\u08C2')
        self.assertEqual(self.jenv.CallByteMethod(obj2, Example__get_byte_field), 42)
        self.assertEqual(self.jenv.CallShortMethod(obj2, Example__get_short_field), 2242)
        self.assertEqual(self.jenv.CallIntMethod(obj2, Example__get_int_field), 2242)
        self.assertEqual(self.jenv.CallLongMethod(obj2, Example__get_long_field), 2242)
        self.assertEqual(self.jenv.CallFloatMethod(obj2, Example__get_float_field), 2242.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj2, Example__get_double_field), 2242.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj2, Example__get_String_field)), "2242")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj2, Example, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj2, Example, Example__get_base_char_field), u'\u002C')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj2, Example, Example__get_base_byte_field), 44)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj2, Example, Example__get_base_short_field), 44)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj2, Example, Example__get_base_int_field), 44)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj2, Example, Example__get_base_long_field), 44)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj2, Example, Example__get_base_float_field), 44.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj2, Example, Example__get_base_double_field), 44.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj2, Example, Example__get_base_String_field)), "44")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj2, Example, Example__get_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj2, Example, Example__get_char_field), u'\u08C2')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj2, Example, Example__get_byte_field), 42)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj2, Example, Example__get_short_field), 2242)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj2, Example, Example__get_int_field), 2242)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj2, Example, Example__get_long_field), 2242)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj2, Example, Example__get_float_field), 2242.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj2, Example, Example__get_double_field), 2242.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj2, Example, Example__get_String_field)), "2242")

        self.assertEqual(self.jenv.GetBooleanField(obj2, Example__base_boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj2, Example__base_char_field), u'\u002C')
        self.assertEqual(self.jenv.GetByteField(obj2, Example__base_byte_field), 44)
        self.assertEqual(self.jenv.GetShortField(obj2, Example__base_short_field), 44)
        self.assertEqual(self.jenv.GetIntField(obj2, Example__base_int_field), 44)
        self.assertEqual(self.jenv.GetLongField(obj2, Example__base_long_field), 44)
        self.assertEqual(self.jenv.GetFloatField(obj2, Example__base_float_field), 44.0)
        self.assertEqual(self.jenv.GetDoubleField(obj2, Example__base_double_field), 44.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj2, Example__base_String_field)), "44")

        self.assertEqual(self.jenv.GetBooleanField(obj2, Example__boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj2, Example__char_field), u'\u08C2')
        self.assertEqual(self.jenv.GetByteField(obj2, Example__byte_field), 42)
        self.assertEqual(self.jenv.GetShortField(obj2, Example__short_field), 2242)
        self.assertEqual(self.jenv.GetIntField(obj2, Example__int_field), 2242)
        self.assertEqual(self.jenv.GetLongField(obj2, Example__long_field), 2242)
        self.assertEqual(self.jenv.GetFloatField(obj2, Example__float_field), 2242.0)
        self.assertEqual(self.jenv.GetDoubleField(obj2, Example__double_field), 2242.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj2, Example__String_field)), "2242")

        # Create an instance of org.jt.jni.test.Example using the "two int" constructor

        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].i = 3342
        jargs[1].i = 3337
        obj3 = self.jenv.NewObject(Example, Example__init_ii, jargs)
        self.assertTrue(obj3)

        # Check that instance values are as expected

        self.assertEqual(self.jenv.CallBooleanMethod(obj3, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj3, Example__get_base_char_field), u'\u0D0E')
        self.assertEqual(self.jenv.CallByteMethod(obj3, Example__get_base_byte_field), 42)
        self.assertEqual(self.jenv.CallShortMethod(obj3, Example__get_base_short_field), 3342)
        self.assertEqual(self.jenv.CallIntMethod(obj3, Example__get_base_int_field), 3342)
        self.assertEqual(self.jenv.CallLongMethod(obj3, Example__get_base_long_field), 3342)
        self.assertEqual(self.jenv.CallFloatMethod(obj3, Example__get_base_float_field), 3342.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj3, Example__get_base_double_field), 3342.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj3, Example__get_base_String_field)), "3342")

        self.assertEqual(self.jenv.CallBooleanMethod(obj3, Example__get_boolean_field), True)
        self.assertEqual(self.jenv.CallCharMethod(obj3, Example__get_char_field), u'\u0D09')
        self.assertEqual(self.jenv.CallByteMethod(obj3, Example__get_byte_field), 37)
        self.assertEqual(self.jenv.CallShortMethod(obj3, Example__get_short_field), 3337)
        self.assertEqual(self.jenv.CallIntMethod(obj3, Example__get_int_field), 3337)
        self.assertEqual(self.jenv.CallLongMethod(obj3, Example__get_long_field), 3337)
        self.assertEqual(self.jenv.CallFloatMethod(obj3, Example__get_float_field), 3337.0)
        self.assertEqual(self.jenv.CallDoubleMethod(obj3, Example__get_double_field), 3337.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallObjectMethod(obj3, Example__get_String_field)), "3337")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj3, Example, Example__get_base_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj3, Example, Example__get_base_char_field), u'\u0D0E')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj3, Example, Example__get_base_byte_field), 42)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj3, Example, Example__get_base_short_field), 3342)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj3, Example, Example__get_base_int_field), 3342)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj3, Example, Example__get_base_long_field), 3342)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj3, Example, Example__get_base_float_field), 3342.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj3, Example, Example__get_base_double_field), 3342.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj3, Example, Example__get_base_String_field)), "3342")

        self.assertEqual(self.jenv.CallNonvirtualBooleanMethod(obj3, Example, Example__get_boolean_field), True)
        self.assertEqual(self.jenv.CallNonvirtualCharMethod(obj3, Example, Example__get_char_field), u'\u0D09')
        self.assertEqual(self.jenv.CallNonvirtualByteMethod(obj3, Example, Example__get_byte_field), 37)
        self.assertEqual(self.jenv.CallNonvirtualShortMethod(obj3, Example, Example__get_short_field), 3337)
        self.assertEqual(self.jenv.CallNonvirtualIntMethod(obj3, Example, Example__get_int_field), 3337)
        self.assertEqual(self.jenv.CallNonvirtualLongMethod(obj3, Example, Example__get_long_field), 3337)
        self.assertEqual(self.jenv.CallNonvirtualFloatMethod(obj3, Example, Example__get_float_field), 3337.0)
        self.assertEqual(self.jenv.CallNonvirtualDoubleMethod(obj3, Example, Example__get_double_field), 3337.0)
        self.assertEqual(self.jstring2unicode(self.jenv.CallNonvirtualObjectMethod(obj3, Example, Example__get_String_field)), "3337")

        self.assertEqual(self.jenv.GetBooleanField(obj3, Example__base_boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj3, Example__base_char_field), u'\u0D0E')
        self.assertEqual(self.jenv.GetByteField(obj3, Example__base_byte_field), 42)
        self.assertEqual(self.jenv.GetShortField(obj3, Example__base_short_field), 3342)
        self.assertEqual(self.jenv.GetIntField(obj3, Example__base_int_field), 3342)
        self.assertEqual(self.jenv.GetLongField(obj3, Example__base_long_field), 3342)
        self.assertEqual(self.jenv.GetFloatField(obj3, Example__base_float_field), 3342.0)
        self.assertEqual(self.jenv.GetDoubleField(obj3, Example__base_double_field), 3342.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj3, Example__base_String_field)), "3342")

        self.assertEqual(self.jenv.GetBooleanField(obj3, Example__boolean_field), True)
        self.assertEqual(self.jenv.GetCharField(obj3, Example__char_field), u'\u0D09')
        self.assertEqual(self.jenv.GetByteField(obj3, Example__byte_field), 37)
        self.assertEqual(self.jenv.GetShortField(obj3, Example__short_field), 3337)
        self.assertEqual(self.jenv.GetIntField(obj3, Example__int_field), 3337)
        self.assertEqual(self.jenv.GetLongField(obj3, Example__long_field), 3337)
        self.assertEqual(self.jenv.GetFloatField(obj3, Example__float_field), 3337.0)
        self.assertEqual(self.jenv.GetDoubleField(obj3, Example__double_field), 3337.0)
        self.assertEqual(self.jstring2unicode(self.jenv.GetObjectField(obj3, Example__String_field)), "3337")

    def test_static(self):
        """Static fields and methods can be invoked"""

        import jni

        # Get a reference to the org.jt.jni.test.Example class
        Example = self.jenv.FindClass(b"org/jt/jni/test/Example")
        self.assertTrue(Example)

        # Find Example.static_base_<type>_field
        Example__static_base_boolean_field = self.jenv.GetStaticFieldID(Example, b"static_base_boolean_field", b"Z")
        Example__static_base_char_field    = self.jenv.GetStaticFieldID(Example, b"static_base_char_field",    b"C")
        Example__static_base_byte_field    = self.jenv.GetStaticFieldID(Example, b"static_base_byte_field",    b"B")
        Example__static_base_short_field   = self.jenv.GetStaticFieldID(Example, b"static_base_short_field",   b"S")
        Example__static_base_int_field     = self.jenv.GetStaticFieldID(Example, b"static_base_int_field",     b"I")
        Example__static_base_long_field    = self.jenv.GetStaticFieldID(Example, b"static_base_long_field",    b"J")
        Example__static_base_float_field   = self.jenv.GetStaticFieldID(Example, b"static_base_float_field",   b"F")
        Example__static_base_double_field  = self.jenv.GetStaticFieldID(Example, b"static_base_double_field",  b"D")
        Example__static_base_String_field  = self.jenv.GetStaticFieldID(Example, b"static_base_String_field",  b"Ljava/lang/String;")
        self.assertTrue(Example__static_base_boolean_field)
        self.assertTrue(Example__static_base_char_field)
        self.assertTrue(Example__static_base_byte_field)
        self.assertTrue(Example__static_base_short_field)
        self.assertTrue(Example__static_base_int_field)
        self.assertTrue(Example__static_base_long_field)
        self.assertTrue(Example__static_base_float_field)
        self.assertTrue(Example__static_base_double_field)
        self.assertTrue(Example__static_base_String_field)

        # Find Example.static_<type>_field
        Example__static_boolean_field = self.jenv.GetStaticFieldID(Example, b"static_boolean_field", b"Z")
        Example__static_char_field    = self.jenv.GetStaticFieldID(Example, b"static_char_field",    b"C")
        Example__static_byte_field    = self.jenv.GetStaticFieldID(Example, b"static_byte_field",    b"B")
        Example__static_short_field   = self.jenv.GetStaticFieldID(Example, b"static_short_field",   b"S")
        Example__static_int_field     = self.jenv.GetStaticFieldID(Example, b"static_int_field",     b"I")
        Example__static_long_field    = self.jenv.GetStaticFieldID(Example, b"static_long_field",    b"J")
        Example__static_float_field   = self.jenv.GetStaticFieldID(Example, b"static_float_field",   b"F")
        Example__static_double_field  = self.jenv.GetStaticFieldID(Example, b"static_double_field",  b"D")
        Example__static_String_field  = self.jenv.GetStaticFieldID(Example, b"static_String_field",  b"Ljava/lang/String;")
        self.assertTrue(Example__static_boolean_field)
        self.assertTrue(Example__static_char_field)
        self.assertTrue(Example__static_byte_field)
        self.assertTrue(Example__static_short_field)
        self.assertTrue(Example__static_int_field)
        self.assertTrue(Example__static_long_field)
        self.assertTrue(Example__static_float_field)
        self.assertTrue(Example__static_double_field)
        self.assertTrue(Example__static_String_field)

        # Find the BaseExample.get_static_base_<type>_field() and BaseExample.set_static_base_<type>_int_field() methods on Example
        Example__get_static_base_boolean_field = self.jenv.GetStaticMethodID(Example, b"get_static_base_boolean_field", b"()Z")
        Example__set_static_base_boolean_field = self.jenv.GetStaticMethodID(Example, b"set_static_base_boolean_field", b"(Z)V")
        Example__get_static_base_char_field    = self.jenv.GetStaticMethodID(Example, b"get_static_base_char_field",    b"()C")
        Example__set_static_base_char_field    = self.jenv.GetStaticMethodID(Example, b"set_static_base_char_field",    b"(C)V")
        Example__get_static_base_byte_field    = self.jenv.GetStaticMethodID(Example, b"get_static_base_byte_field",    b"()B")
        Example__set_static_base_byte_field    = self.jenv.GetStaticMethodID(Example, b"set_static_base_byte_field",    b"(B)V")
        Example__get_static_base_short_field   = self.jenv.GetStaticMethodID(Example, b"get_static_base_short_field",   b"()S")
        Example__set_static_base_short_field   = self.jenv.GetStaticMethodID(Example, b"set_static_base_short_field",   b"(S)V")
        Example__get_static_base_int_field     = self.jenv.GetStaticMethodID(Example, b"get_static_base_int_field",     b"()I")
        Example__set_static_base_int_field     = self.jenv.GetStaticMethodID(Example, b"set_static_base_int_field",     b"(I)V")
        Example__get_static_base_long_field    = self.jenv.GetStaticMethodID(Example, b"get_static_base_long_field",    b"()J")
        Example__set_static_base_long_field    = self.jenv.GetStaticMethodID(Example, b"set_static_base_long_field",    b"(J)V")
        Example__get_static_base_float_field   = self.jenv.GetStaticMethodID(Example, b"get_static_base_float_field",   b"()F")
        Example__set_static_base_float_field   = self.jenv.GetStaticMethodID(Example, b"set_static_base_float_field",   b"(F)V")
        Example__get_static_base_double_field  = self.jenv.GetStaticMethodID(Example, b"get_static_base_double_field",  b"()D")
        Example__set_static_base_double_field  = self.jenv.GetStaticMethodID(Example, b"set_static_base_double_field",  b"(D)V")
        Example__get_static_base_String_field  = self.jenv.GetStaticMethodID(Example, b"get_static_base_String_field",  b"()Ljava/lang/String;")
        Example__set_static_base_String_field  = self.jenv.GetStaticMethodID(Example, b"set_static_base_String_field",  b"(Ljava/lang/String;)V")
        self.assertTrue(Example__get_static_base_boolean_field)
        self.assertTrue(Example__set_static_base_boolean_field)
        self.assertTrue(Example__get_static_base_char_field)
        self.assertTrue(Example__set_static_base_char_field)
        self.assertTrue(Example__get_static_base_byte_field)
        self.assertTrue(Example__set_static_base_byte_field)
        self.assertTrue(Example__get_static_base_short_field)
        self.assertTrue(Example__set_static_base_short_field)
        self.assertTrue(Example__get_static_base_int_field)
        self.assertTrue(Example__set_static_base_int_field)
        self.assertTrue(Example__get_static_base_long_field)
        self.assertTrue(Example__set_static_base_long_field)
        self.assertTrue(Example__get_static_base_float_field)
        self.assertTrue(Example__set_static_base_float_field)
        self.assertTrue(Example__get_static_base_double_field)
        self.assertTrue(Example__set_static_base_double_field)
        self.assertTrue(Example__get_static_base_String_field)
        self.assertTrue(Example__set_static_base_String_field)

        # Find the Example.get_static_<type>_field() and Example.set_static_<type>_field() methods
        Example__get_static_boolean_field = self.jenv.GetStaticMethodID(Example, b"get_static_boolean_field", b"()Z")
        Example__set_static_boolean_field = self.jenv.GetStaticMethodID(Example, b"set_static_boolean_field", b"(Z)V")
        Example__get_static_char_field    = self.jenv.GetStaticMethodID(Example, b"get_static_char_field",    b"()C")
        Example__set_static_char_field    = self.jenv.GetStaticMethodID(Example, b"set_static_char_field",    b"(C)V")
        Example__get_static_byte_field    = self.jenv.GetStaticMethodID(Example, b"get_static_byte_field",    b"()B")
        Example__set_static_byte_field    = self.jenv.GetStaticMethodID(Example, b"set_static_byte_field",    b"(B)V")
        Example__get_static_short_field   = self.jenv.GetStaticMethodID(Example, b"get_static_short_field",   b"()S")
        Example__set_static_short_field   = self.jenv.GetStaticMethodID(Example, b"set_static_short_field",   b"(S)V")
        Example__get_static_int_field     = self.jenv.GetStaticMethodID(Example, b"get_static_int_field",     b"()I")
        Example__set_static_int_field     = self.jenv.GetStaticMethodID(Example, b"set_static_int_field",     b"(I)V")
        Example__get_static_long_field    = self.jenv.GetStaticMethodID(Example, b"get_static_long_field",    b"()J")
        Example__set_static_long_field    = self.jenv.GetStaticMethodID(Example, b"set_static_long_field",    b"(J)V")
        Example__get_static_float_field   = self.jenv.GetStaticMethodID(Example, b"get_static_float_field",   b"()F")
        Example__set_static_float_field   = self.jenv.GetStaticMethodID(Example, b"set_static_float_field",   b"(F)V")
        Example__get_static_double_field  = self.jenv.GetStaticMethodID(Example, b"get_static_double_field",  b"()D")
        Example__set_static_double_field  = self.jenv.GetStaticMethodID(Example, b"set_static_double_field",  b"(D)V")
        Example__get_static_String_field  = self.jenv.GetStaticMethodID(Example, b"get_static_String_field",  b"()Ljava/lang/String;")
        Example__set_static_String_field  = self.jenv.GetStaticMethodID(Example, b"set_static_String_field",  b"(Ljava/lang/String;)V")
        self.assertTrue(Example__get_static_boolean_field)
        self.assertTrue(Example__set_static_boolean_field)
        self.assertTrue(Example__get_static_char_field)
        self.assertTrue(Example__set_static_char_field)
        self.assertTrue(Example__get_static_byte_field)
        self.assertTrue(Example__set_static_byte_field)
        self.assertTrue(Example__get_static_short_field)
        self.assertTrue(Example__set_static_short_field)
        self.assertTrue(Example__get_static_int_field)
        self.assertTrue(Example__set_static_int_field)
        self.assertTrue(Example__get_static_long_field)
        self.assertTrue(Example__set_static_long_field)
        self.assertTrue(Example__get_static_float_field)
        self.assertTrue(Example__set_static_float_field)
        self.assertTrue(Example__get_static_double_field)
        self.assertTrue(Example__set_static_double_field)
        self.assertTrue(Example__get_static_String_field)
        self.assertTrue(Example__set_static_String_field)

        # Save static fields values

        Example__static_base_boolean_field_save = self.jenv.GetStaticBooleanField(Example, Example__static_base_boolean_field)
        Example__static_base_char_field_save    = self.jenv.GetStaticCharField(Example, Example__static_base_char_field)
        Example__static_base_byte_field_save    = self.jenv.GetStaticByteField(Example, Example__static_base_byte_field)
        Example__static_base_short_field_save   = self.jenv.GetStaticShortField(Example, Example__static_base_short_field)
        Example__static_base_int_field_save     = self.jenv.GetStaticIntField(Example, Example__static_base_int_field)
        Example__static_base_long_field_save    = self.jenv.GetStaticLongField(Example, Example__static_base_long_field)
        Example__static_base_float_field_save   = self.jenv.GetStaticFloatField(Example, Example__static_base_float_field)
        Example__static_base_double_field_save  = self.jenv.GetStaticDoubleField(Example, Example__static_base_double_field)
        Example__static_base_String_field_save  = self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_base_String_field))

        Example__static_boolean_field_save = self.jenv.GetStaticBooleanField(Example, Example__static_boolean_field)
        Example__static_char_field_save    = self.jenv.GetStaticCharField(Example, Example__static_char_field)
        Example__static_byte_field_save    = self.jenv.GetStaticByteField(Example, Example__static_byte_field)
        Example__static_short_field_save   = self.jenv.GetStaticShortField(Example, Example__static_short_field)
        Example__static_int_field_save     = self.jenv.GetStaticIntField(Example, Example__static_int_field)
        Example__static_long_field_save    = self.jenv.GetStaticLongField(Example, Example__static_long_field)
        Example__static_float_field_save   = self.jenv.GetStaticFloatField(Example, Example__static_float_field)
        Example__static_double_field_save  = self.jenv.GetStaticDoubleField(Example, Example__static_double_field)
        Example__static_String_field_save  = self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_String_field))

        try:
            # Use the static_base_<type>_field and static_<type>_field methods

            self.assertEqual(self.jenv.GetStaticBooleanField(Example, Example__static_base_boolean_field), False)
            self.assertEqual(self.jenv.GetStaticCharField(Example, Example__static_base_char_field), u'\u0001')
            self.assertEqual(self.jenv.GetStaticByteField(Example, Example__static_base_byte_field), 1)
            self.assertEqual(self.jenv.GetStaticShortField(Example, Example__static_base_short_field), 1)
            self.assertEqual(self.jenv.GetStaticIntField(Example, Example__static_base_int_field), 1)
            self.assertEqual(self.jenv.GetStaticLongField(Example, Example__static_base_long_field), 1)
            self.assertEqual(self.jenv.GetStaticFloatField(Example, Example__static_base_float_field), 1.0)
            self.assertEqual(self.jenv.GetStaticDoubleField(Example, Example__static_base_double_field), 1.0)
            self.assertEqual(self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_base_String_field)), "1")

            self.assertEqual(self.jenv.GetStaticBooleanField(Example, Example__static_boolean_field), False)
            self.assertEqual(self.jenv.GetStaticCharField(Example, Example__static_char_field), u'\u000B')
            self.assertEqual(self.jenv.GetStaticByteField(Example, Example__static_byte_field), 11)
            self.assertEqual(self.jenv.GetStaticShortField(Example, Example__static_short_field), 11)
            self.assertEqual(self.jenv.GetStaticIntField(Example, Example__static_int_field), 11)
            self.assertEqual(self.jenv.GetStaticLongField(Example, Example__static_long_field), 11)
            self.assertEqual(self.jenv.GetStaticFloatField(Example, Example__static_float_field), 11.0)
            self.assertEqual(self.jenv.GetStaticDoubleField(Example, Example__static_double_field), 11.0)
            self.assertEqual(self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_String_field)), "11")

            # Use the get_static_base_<type>_field and get_static_<type>_field methods

            self.assertEqual(self.jenv.CallStaticBooleanMethod(Example, Example__get_static_base_boolean_field), False)
            self.assertEqual(self.jenv.CallStaticCharMethod(Example, Example__get_static_base_char_field), u'\u0001')
            self.assertEqual(self.jenv.CallStaticByteMethod(Example, Example__get_static_base_byte_field), 1)
            self.assertEqual(self.jenv.CallStaticShortMethod(Example, Example__get_static_base_short_field), 1)
            self.assertEqual(self.jenv.CallStaticIntMethod(Example, Example__get_static_base_int_field), 1)
            self.assertEqual(self.jenv.CallStaticLongMethod(Example, Example__get_static_base_long_field), 1)
            self.assertEqual(self.jenv.CallStaticFloatMethod(Example, Example__get_static_base_float_field), 1.0)
            self.assertEqual(self.jenv.CallStaticDoubleMethod(Example, Example__get_static_base_double_field), 1.0)
            self.assertEqual(self.jstring2unicode(self.jenv.CallStaticObjectMethod(Example, Example__get_static_base_String_field)), "1")

            self.assertEqual(self.jenv.CallStaticBooleanMethod(Example, Example__get_static_boolean_field), False)
            self.assertEqual(self.jenv.CallStaticCharMethod(Example, Example__get_static_char_field), u'\u000B')
            self.assertEqual(self.jenv.CallStaticByteMethod(Example, Example__get_static_byte_field), 11)
            self.assertEqual(self.jenv.CallStaticShortMethod(Example, Example__get_static_short_field), 11)
            self.assertEqual(self.jenv.CallStaticIntMethod(Example, Example__get_static_int_field), 11)
            self.assertEqual(self.jenv.CallStaticLongMethod(Example, Example__get_static_long_field), 11)
            self.assertEqual(self.jenv.CallStaticFloatMethod(Example, Example__get_static_float_field), 11.0)
            self.assertEqual(self.jenv.CallStaticDoubleMethod(Example, Example__get_static_double_field), 11.0)
            self.assertEqual(self.jstring2unicode(self.jenv.CallStaticObjectMethod(Example, Example__get_static_String_field)), "11")

            # Use the set_static_base_<type>_field and set_static_<type>_field methods

            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].z = True
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_boolean_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].c = u'\u0471'
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_char_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].b = 37
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_byte_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].s = 1137
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_short_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].i = 1137
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_int_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].j = 1137
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_long_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].f = 1137
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_float_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].d = 1137
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_double_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = self.jenv.NewStringUTF("1137".encode("utf-8"))
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_base_String_field, jargs)

            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].z = True
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_boolean_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].c = u'\u0476'
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_char_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].b = 42
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_byte_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].s = 1142
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_short_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].i = 1142
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_int_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].j = 1142
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_long_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].f = 1142
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_float_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].d = 1142
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_double_field, jargs)
            jargs = jni.new_array(jni.jvalue, 1)
            jargs[0].l = self.jenv.NewStringUTF("1142".encode("utf-8"))
            self.jenv.CallStaticVoidMethod(Example, Example__set_static_String_field, jargs)

            # Confirm that the values have changed

            self.assertEqual(self.jenv.CallStaticBooleanMethod(Example, Example__get_static_base_boolean_field), True)
            self.assertEqual(self.jenv.CallStaticCharMethod(Example, Example__get_static_base_char_field), u'\u0471')
            self.assertEqual(self.jenv.CallStaticByteMethod(Example, Example__get_static_base_byte_field), 37)
            self.assertEqual(self.jenv.CallStaticShortMethod(Example, Example__get_static_base_short_field), 1137)
            self.assertEqual(self.jenv.CallStaticIntMethod(Example, Example__get_static_base_int_field), 1137)
            self.assertEqual(self.jenv.CallStaticLongMethod(Example, Example__get_static_base_long_field), 1137)
            self.assertEqual(self.jenv.CallStaticFloatMethod(Example, Example__get_static_base_float_field), 1137.0)
            self.assertEqual(self.jenv.CallStaticDoubleMethod(Example, Example__get_static_base_double_field), 1137.0)
            self.assertEqual(self.jstring2unicode(self.jenv.CallStaticObjectMethod(Example, Example__get_static_base_String_field)), "1137")

            self.assertEqual(self.jenv.CallStaticBooleanMethod(Example, Example__get_static_boolean_field), True)
            self.assertEqual(self.jenv.CallStaticCharMethod(Example, Example__get_static_char_field), u'\u0476')
            self.assertEqual(self.jenv.CallStaticByteMethod(Example, Example__get_static_byte_field), 42)
            self.assertEqual(self.jenv.CallStaticShortMethod(Example, Example__get_static_short_field), 1142)
            self.assertEqual(self.jenv.CallStaticIntMethod(Example, Example__get_static_int_field), 1142)
            self.assertEqual(self.jenv.CallStaticLongMethod(Example, Example__get_static_long_field), 1142)
            self.assertEqual(self.jenv.CallStaticFloatMethod(Example, Example__get_static_float_field), 1142.0)
            self.assertEqual(self.jenv.CallStaticDoubleMethod(Example, Example__get_static_double_field), 1142.0)
            self.assertEqual(self.jstring2unicode(self.jenv.CallStaticObjectMethod(Example, Example__get_static_String_field)), "1142")

            self.assertEqual(self.jenv.GetStaticBooleanField(Example, Example__static_base_boolean_field), True)
            self.assertEqual(self.jenv.GetStaticCharField(Example, Example__static_base_char_field), u'\u0471')
            self.assertEqual(self.jenv.GetStaticByteField(Example, Example__static_base_byte_field), 37)
            self.assertEqual(self.jenv.GetStaticShortField(Example, Example__static_base_short_field), 1137)
            self.assertEqual(self.jenv.GetStaticIntField(Example, Example__static_base_int_field), 1137)
            self.assertEqual(self.jenv.GetStaticLongField(Example, Example__static_base_long_field), 1137)
            self.assertEqual(self.jenv.GetStaticFloatField(Example, Example__static_base_float_field), 1137.0)
            self.assertEqual(self.jenv.GetStaticDoubleField(Example, Example__static_base_double_field), 1137.0)
            self.assertEqual(self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_base_String_field)), "1137")

            self.assertEqual(self.jenv.GetStaticBooleanField(Example, Example__static_boolean_field), True)
            self.assertEqual(self.jenv.GetStaticCharField(Example, Example__static_char_field), u'\u0476')
            self.assertEqual(self.jenv.GetStaticByteField(Example, Example__static_byte_field), 42)
            self.assertEqual(self.jenv.GetStaticShortField(Example, Example__static_short_field), 1142)
            self.assertEqual(self.jenv.GetStaticIntField(Example, Example__static_int_field), 1142)
            self.assertEqual(self.jenv.GetStaticLongField(Example, Example__static_long_field), 1142)
            self.assertEqual(self.jenv.GetStaticFloatField(Example, Example__static_float_field), 1142.0)
            self.assertEqual(self.jenv.GetStaticDoubleField(Example, Example__static_double_field), 1142.0)
            self.assertEqual(self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_String_field)), "1142")

            # Use the static_base_<type>_field and static_<type>_field methods

            self.jenv.SetStaticBooleanField(Example, Example__static_base_boolean_field, False)
            self.jenv.SetStaticCharField(Example, Example__static_base_char_field, u'\u0485')
            self.jenv.SetStaticByteField(Example, Example__static_base_byte_field, 57)
            self.jenv.SetStaticShortField(Example, Example__static_base_short_field, 1157)
            self.jenv.SetStaticIntField(Example, Example__static_base_int_field, 1157)
            self.jenv.SetStaticLongField(Example, Example__static_base_long_field, 1157)
            self.jenv.SetStaticFloatField(Example, Example__static_base_float_field, 1157)
            self.jenv.SetStaticDoubleField(Example, Example__static_base_double_field, 1157)
            self.jenv.SetStaticObjectField(Example, Example__static_base_String_field,
                                           self.jenv.NewStringUTF("1157".encode("utf-8")))

            self.jenv.SetStaticBooleanField(Example, Example__static_boolean_field, False)
            self.jenv.SetStaticCharField(Example, Example__static_char_field, u'\u048A')
            self.jenv.SetStaticByteField(Example, Example__static_byte_field, 62)
            self.jenv.SetStaticShortField(Example, Example__static_short_field, 1162)
            self.jenv.SetStaticIntField(Example, Example__static_int_field, 1162)
            self.jenv.SetStaticLongField(Example, Example__static_long_field, 1162)
            self.jenv.SetStaticFloatField(Example, Example__static_float_field, 1162)
            self.jenv.SetStaticDoubleField(Example, Example__static_double_field, 1162)
            self.jenv.SetStaticObjectField(Example, Example__static_String_field,
                                           self.jenv.NewStringUTF("1162".encode("utf-8")))

            # Confirm that the values have changed

            self.assertEqual(self.jenv.CallStaticBooleanMethod(Example, Example__get_static_base_boolean_field), False)
            self.assertEqual(self.jenv.CallStaticCharMethod(Example, Example__get_static_base_char_field), u'\u0485')
            self.assertEqual(self.jenv.CallStaticByteMethod(Example, Example__get_static_base_byte_field), 57)
            self.assertEqual(self.jenv.CallStaticShortMethod(Example, Example__get_static_base_short_field), 1157)
            self.assertEqual(self.jenv.CallStaticIntMethod(Example, Example__get_static_base_int_field), 1157)
            self.assertEqual(self.jenv.CallStaticLongMethod(Example, Example__get_static_base_long_field), 1157)
            self.assertEqual(self.jenv.CallStaticFloatMethod(Example, Example__get_static_base_float_field), 1157.0)
            self.assertEqual(self.jenv.CallStaticDoubleMethod(Example, Example__get_static_base_double_field), 1157.0)
            self.assertEqual(self.jstring2unicode(self.jenv.CallStaticObjectMethod(Example, Example__get_static_base_String_field)), "1157")

            self.assertEqual(self.jenv.CallStaticBooleanMethod(Example, Example__get_static_boolean_field), False)
            self.assertEqual(self.jenv.CallStaticCharMethod(Example, Example__get_static_char_field), u'\u048A')
            self.assertEqual(self.jenv.CallStaticByteMethod(Example, Example__get_static_byte_field), 62)
            self.assertEqual(self.jenv.CallStaticShortMethod(Example, Example__get_static_short_field), 1162)
            self.assertEqual(self.jenv.CallStaticIntMethod(Example, Example__get_static_int_field), 1162)
            self.assertEqual(self.jenv.CallStaticLongMethod(Example, Example__get_static_long_field), 1162)
            self.assertEqual(self.jenv.CallStaticFloatMethod(Example, Example__get_static_float_field), 1162.0)
            self.assertEqual(self.jenv.CallStaticDoubleMethod(Example, Example__get_static_double_field), 1162.0)
            self.assertEqual(self.jstring2unicode(self.jenv.CallStaticObjectMethod(Example, Example__get_static_String_field)), "1162")

            self.assertEqual(self.jenv.GetStaticBooleanField(Example, Example__static_base_boolean_field), False)
            self.assertEqual(self.jenv.GetStaticCharField(Example, Example__static_base_char_field), u'\u0485')
            self.assertEqual(self.jenv.GetStaticByteField(Example, Example__static_base_byte_field), 57)
            self.assertEqual(self.jenv.GetStaticShortField(Example, Example__static_base_short_field), 1157)
            self.assertEqual(self.jenv.GetStaticIntField(Example, Example__static_base_int_field), 1157)
            self.assertEqual(self.jenv.GetStaticLongField(Example, Example__static_base_long_field), 1157)
            self.assertEqual(self.jenv.GetStaticFloatField(Example, Example__static_base_float_field), 1157.0)
            self.assertEqual(self.jenv.GetStaticDoubleField(Example, Example__static_base_double_field), 1157.0)
            self.assertEqual(self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_base_String_field)), "1157")

            self.assertEqual(self.jenv.GetStaticBooleanField(Example, Example__static_boolean_field), False)
            self.assertEqual(self.jenv.GetStaticCharField(Example, Example__static_char_field), u'\u048A')
            self.assertEqual(self.jenv.GetStaticByteField(Example, Example__static_byte_field), 62)
            self.assertEqual(self.jenv.GetStaticShortField(Example, Example__static_short_field), 1162)
            self.assertEqual(self.jenv.GetStaticIntField(Example, Example__static_int_field), 1162)
            self.assertEqual(self.jenv.GetStaticLongField(Example, Example__static_long_field), 1162)
            self.assertEqual(self.jenv.GetStaticFloatField(Example, Example__static_float_field), 1162.0)
            self.assertEqual(self.jenv.GetStaticDoubleField(Example, Example__static_double_field), 1162.0)
            self.assertEqual(self.jstring2unicode(self.jenv.GetStaticObjectField(Example, Example__static_String_field)), "1162")
        finally:
            # Restore static fields values

            self.jenv.SetStaticBooleanField(Example, Example__static_base_boolean_field, Example__static_base_boolean_field_save)
            self.jenv.SetStaticCharField(Example, Example__static_base_char_field, Example__static_base_char_field_save)
            self.jenv.SetStaticByteField(Example, Example__static_base_byte_field, Example__static_base_byte_field_save)
            self.jenv.SetStaticShortField(Example, Example__static_base_short_field, Example__static_base_short_field_save)
            self.jenv.SetStaticIntField(Example, Example__static_base_int_field, Example__static_base_int_field_save)
            self.jenv.SetStaticLongField(Example, Example__static_base_long_field, Example__static_base_long_field_save)
            self.jenv.SetStaticFloatField(Example, Example__static_base_float_field, Example__static_base_float_field_save)
            self.jenv.SetStaticDoubleField(Example, Example__static_base_double_field, Example__static_base_double_field_save)
            self.jenv.SetStaticObjectField(Example, Example__static_base_String_field,
                                           self.jenv.NewStringUTF(Example__static_base_String_field_save.encode("utf-8")))

            self.jenv.SetStaticBooleanField(Example, Example__static_boolean_field, Example__static_boolean_field_save)
            self.jenv.SetStaticCharField(Example, Example__static_char_field, Example__static_char_field_save)
            self.jenv.SetStaticByteField(Example, Example__static_byte_field, Example__static_byte_field_save)
            self.jenv.SetStaticShortField(Example, Example__static_short_field, Example__static_short_field_save)
            self.jenv.SetStaticIntField(Example, Example__static_int_field, Example__static_int_field_save)
            self.jenv.SetStaticLongField(Example, Example__static_long_field, Example__static_long_field_save)
            self.jenv.SetStaticFloatField(Example, Example__static_float_field, Example__static_float_field_save)
            self.jenv.SetStaticDoubleField(Example, Example__static_double_field, Example__static_double_field_save)
            self.jenv.SetStaticObjectField(Example, Example__static_String_field,
                                           self.jenv.NewStringUTF(Example__static_String_field_save.encode("utf-8")))

    def test_arrays(self):

        import jni

        # Create an instances of primitve arrays

        String = self.jenv.FindClass(b"java/lang/String")
        self.assertTrue(String)
        String__init = self.jenv.GetMethodID(String, b"<init>", b"()V")
        self.assertTrue(String__init)

        boolean_array = self.jenv.NewBooleanArray(110) 
        char_array    = self.jenv.NewCharArray(120) 
        byte_array    = self.jenv.NewByteArray(130) 
        short_array   = self.jenv.NewShortArray(140) 
        int_array     = self.jenv.NewIntArray(150) 
        long_array    = self.jenv.NewLongArray(160) 
        float_array   = self.jenv.NewFloatArray(170) 
        double_array  = self.jenv.NewDoubleArray(180) 
        String_array  = self.jenv.NewObjectArray(190, String)
        self.assertTrue(boolean_array)
        self.assertTrue(char_array)
        self.assertTrue(byte_array)
        self.assertTrue(short_array)
        self.assertTrue(int_array)
        self.assertTrue(long_array)
        self.assertTrue(float_array)
        self.assertTrue(double_array)
        self.assertTrue(String_array)

        boolean_array_length = self.jenv.GetArrayLength(boolean_array)
        char_array_length    = self.jenv.GetArrayLength(char_array)
        byte_array_length    = self.jenv.GetArrayLength(byte_array)
        short_array_length   = self.jenv.GetArrayLength(short_array)
        int_array_length     = self.jenv.GetArrayLength(int_array)
        long_array_length    = self.jenv.GetArrayLength(long_array)
        float_array_length   = self.jenv.GetArrayLength(float_array)
        double_array_length  = self.jenv.GetArrayLength(double_array)
        String_array_length  = self.jenv.GetArrayLength(String_array)
        self.assertIs(type(boolean_array_length), int)
        self.assertIs(type(char_array_length),    int)
        self.assertIs(type(byte_array_length),    int)
        self.assertIs(type(short_array_length),   int)
        self.assertIs(type(int_array_length),     int)
        self.assertIs(type(long_array_length),    int)
        self.assertIs(type(float_array_length),   int)
        self.assertIs(type(double_array_length),  int)
        self.assertIs(type(String_array_length),  int)
        self.assertEqual(boolean_array_length, 110)
        self.assertEqual(char_array_length,    120)
        self.assertEqual(byte_array_length,    130)
        self.assertEqual(short_array_length,   140)
        self.assertEqual(int_array_length,     150)
        self.assertEqual(long_array_length,    160)
        self.assertEqual(float_array_length,   170)
        self.assertEqual(double_array_length,  180)
        self.assertEqual(String_array_length,  190)

    def test_string(self):
        """A Java string can be created, and the content returned"""

        import jni

        # This string contains unicode characters
        s = u"H\xe9llo world"

        java_string = self.jenv.NewStringUTF(s.encode("utf-8"))
        self.assertEqual(self.jstring2unicode(java_string), s)
        self.assertEqual(self.jenv.GetStringLength(java_string), len(s))
        self.assertEqual(self.jenv.GetStringUTFLength(java_string), len(s) + 1)

        java_string = self.jenv.NewString(s, len(s))
        self.assertEqual(self.jstring2unicode(java_string), s)
        self.assertEqual(self.jenv.GetStringLength(java_string), len(s))
        self.assertEqual(self.jenv.GetStringUTFLength(java_string), len(s) + 1)

    def test_string_method(self):
        """A Java string can be created, and the content returned"""

        import jni

        # This string contains unicode characters
        s = "Woop"
        java_string = self.jenv.NewStringUTF(s.encode("utf-8"))

        Example = self.jenv.FindClass(b"org/jt/jni/test/Example")
        self.assertTrue(Example)

        # Find the default constructor
        Example__init = self.jenv.GetMethodID(Example, b"<init>", b"()V")
        self.assertTrue(Example__init)

        # Find the Example.duplicate_string() method on Example
        Example__duplicate_string = self.jenv.GetMethodID(Example, b"duplicate_string", b"(Ljava/lang/String;)Ljava/lang/String;")
        self.assertTrue(Example__duplicate_string)

        # Create an instance of org.jt.jni.test.Example using the default constructor
        obj1 = self.jenv.NewObject(Example, Example__init)
        self.assertTrue(obj1)

        # Invoke the string duplication method
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].l = java_string
        result = self.jenv.CallObjectMethod(obj1, Example__duplicate_string, jargs)
        self.assertEqual(self.jstring2unicode(jni.cast(result, jni.jstring)), "WoopWoop")

    def test_float_method(self):
        """A Java float can be created, and the content returned"""

        import jni

        # This string contains unicode characters
        Example = self.jenv.FindClass(b"org/jt/jni/test/Example")
        self.assertTrue(Example)

        # Find the default constructor
        Example__init = self.jenv.GetMethodID(Example, b"<init>", b"()V")
        self.assertTrue(Example__init)

        # Find the Example.area_of_square() method on Example
        Example__area_of_square = self.jenv.GetMethodID(Example, b"area_of_square", b"(F)F")
        self.assertTrue(Example__area_of_square)

        # Create an instance of Example using the default constructor
        obj1 = self.jenv.NewObject(Example, Example__init)
        self.assertTrue(obj1)

        # Invoke the area method
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].f = 1.5
        result = self.jenv.CallFloatMethod(obj1, Example__area_of_square, jargs)
        self.assertEqual(result, 2.25)

    def test_double_method(self):
        """A Java double can be created, and the content returned"""

        import jni

        # This string contains unicode characters
        Example = self.jenv.FindClass(b"org/jt/jni/test/Example")
        self.assertTrue(Example)

        # Find the default constructor
        Example__init = self.jenv.GetMethodID(Example, b"<init>", b"()V")
        self.assertTrue(Example__init)

        # Find the Example.area_of_circle() method on Example
        Example__area_of_circle = self.jenv.GetMethodID(Example, b"area_of_circle", b"(D)D")
        self.assertTrue(Example__area_of_circle)

        # Create an instance of Example using the default constructor
        obj1 = self.jenv.NewObject(Example, Example__init)
        self.assertTrue(obj1)

        # Invoke the area method
        jargs = jni.new_array(jni.jvalue, 1)
        jargs[0].d = 1.5
        result = self.jenv.CallDoubleMethod(obj1, Example__area_of_circle, jargs)
        self.assertEqual(result, 0.25 * (math.pi * 2.25))

    def test_ClassStaticField(self):

        import jni

        #self.assertEqual(self.StringClass, self.ClassArrayTest.staticField[0])
        #self.ClassArrayTest.staticField = self.ClassArray([self.MapClass])
        #self.assertEqual(self.MapClass, self.ClassArrayTest.staticField[0])

    def test_WrongType(self):

        import jni

        #a = self.ClassArray([self.FloatClass])
        #with self.assertRaises(TypeError):
        #    a[0] = 1

    def jstring2unicode(self, jstr) -> Optional[str]:
        import jni
        utf8_chars = self.jenv.GetStringUTFChars(jstr)
        try:
            return jni.to_bytes(utf8_chars).decode("utf-8")
        finally:
            self.jenv.ReleaseStringUTFChars(jstr, utf8_chars)
