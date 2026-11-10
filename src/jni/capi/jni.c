// Copyright (c) 2004 Adam Karpierz
// SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
// Please refer to the accompanying LICENSE file.

#include <Python.h>
#include <structmember.h>

#include <jni.h>

#define member_size(type, member) sizeof(((type *)0)->member)

static const char __name__[] = "jni";
static const char __doc__[]  = "";

typedef struct {
    PyObject_HEAD
    char this[0];
} _CData_Object;

PyTypeObject _CData_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.CData",
    .tp_basicsize = sizeof(_CData_Object),
    .tp_flags     = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
};

//------------ JNI Types -------------//

//--- jboolean ---//

typedef struct {
    PyObject_HEAD
    jboolean value;
} jboolean_Object;

static int jboolean_init(jboolean_Object* self, PyObject* args)
{
    unsigned char value = 0;
    if ( ! PyArg_ParseTuple(args, "|b", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jboolean_bool(jboolean_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jboolean_as_number = {
    .nb_bool = (inquiry)jboolean_bool,
};

static PyMemberDef jboolean_members[] =
{
    {"value", T_BOOL, offsetof(jboolean_Object, value)},
    {NULL}
};

PyTypeObject jboolean_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jboolean",
    .tp_basicsize = sizeof(jboolean_Object),
    .tp_itemsize  = member_size(jboolean_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jboolean_as_number,
    .tp_members   = jboolean_members,
    .tp_init      = (initproc)jboolean_init,
    .tp_new       = PyType_GenericNew,
};

//----- jchar ----//

typedef struct {
    PyObject_HEAD
    jchar value;
} jchar_Object;

static int jchar_init(jchar_Object* self, PyObject* args)
{
    int value = 0;
    if ( ! PyArg_ParseTuple(args, "|C", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jchar_bool(jchar_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jchar_as_number = {
    .nb_bool = (inquiry)jchar_bool,
};

static PyObject* jchar_value_get(jchar_Object* self)
{
    return PyUnicode_FromWideChar((const wchar_t*)&self->value, 1);
}

static int jchar_value_set(jchar_Object* self, PyObject* val)
{
    wchar_t value = 0;
    if ( PyUnicode_AsWideChar(val, &value, 1) == -1 )
        return -1;
    if ( PyUnicode_GetLength(val) != 1 )
    {
        PyErr_SetString(PyExc_TypeError,
                        "one unicode character expected, not str");
        return -1;
    }
    self->value = value;
    return 0;
}

static PyGetSetDef jchar_getsets[] =
{
    {"value", (getter)jchar_value_get, (setter)jchar_value_set},
    {NULL}
};

PyTypeObject jchar_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jchar",
    .tp_basicsize = sizeof(jchar_Object),
    .tp_itemsize  = member_size(jchar_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jchar_as_number,
    .tp_getset    = jchar_getsets,
    .tp_init      = (initproc)jchar_init,
    .tp_new       = PyType_GenericNew,
};

//----- jbyte ----//

typedef struct {
    PyObject_HEAD
    jbyte value;
} jbyte_Object;

static int jbyte_init(jbyte_Object* self, PyObject* args)
{
    jbyte value = 0;
    if ( ! PyArg_ParseTuple(args, "|b", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jbyte_bool(jbyte_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jbyte_as_number = {
    .nb_bool = (inquiry)jbyte_bool,
};

static PyMemberDef jbyte_members[] =
{
    {"value", T_BYTE, offsetof(jbyte_Object, value)},
    {NULL}
};

PyTypeObject jbyte_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jbyte",
    .tp_basicsize = sizeof(jbyte_Object),
    .tp_itemsize  = member_size(jbyte_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jbyte_as_number,
    .tp_members   = jbyte_members,
    .tp_init      = (initproc)jbyte_init,
    .tp_new       = PyType_GenericNew,
};

//---- jshort ----//

typedef struct {
    PyObject_HEAD
    jshort value;
} jshort_Object;

static int jshort_init(jshort_Object* self, PyObject* args)
{
    short value = 0;
    if ( ! PyArg_ParseTuple(args, "|h", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jshort_bool(jshort_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jshort_as_number = {
    .nb_bool = (inquiry)jshort_bool,
};

static PyMemberDef jshort_members[] =
{
    {"value", T_SHORT, offsetof(jshort_Object, value)},
    {NULL}
};

PyTypeObject jshort_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jshort",
    .tp_basicsize = sizeof(jshort_Object),
    .tp_itemsize  = member_size(jshort_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jshort_as_number,
    .tp_members   = jshort_members,
    .tp_init      = (initproc)jshort_init,
    .tp_new       = PyType_GenericNew,
};

//----- jint -----//

typedef struct {
    PyObject_HEAD
    jint value;
} jint_Object;

static int jint_init(jint_Object* self, PyObject* args)
{
    jint value = 0;
    if ( ! PyArg_ParseTuple(args, "|l", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jint_bool(jint_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jint_as_number = {
    .nb_bool = (inquiry)jint_bool,
};

static PyMemberDef jint_members[] =
{
    {"value", T_LONG, offsetof(jint_Object, value)},
    {NULL}
};

PyTypeObject jint_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jint",
    .tp_basicsize = sizeof(jint_Object),
    .tp_itemsize  = member_size(jint_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jint_as_number,
    .tp_members   = jint_members,
    .tp_init      = (initproc)jint_init,
    .tp_new       = PyType_GenericNew,
};

//----- jlong ----//

typedef struct {
    PyObject_HEAD
    jlong value;
} jlong_Object;

static int jlong_init(jlong_Object* self, PyObject* args)
{
    jlong value = 0;
    if ( ! PyArg_ParseTuple(args, "|L", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jlong_bool(jlong_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jlong_as_number = {
    .nb_bool = (inquiry)jlong_bool,
};

static PyMemberDef jlong_members[] =
{
    {"value", T_LONGLONG, offsetof(jlong_Object, value)},
    {NULL}
};

PyTypeObject jlong_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jlong",
    .tp_basicsize = sizeof(jlong_Object),
    .tp_itemsize  = member_size(jlong_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jlong_as_number,
    .tp_members   = jlong_members,
    .tp_init      = (initproc)jlong_init,
    .tp_new       = PyType_GenericNew,
};

//---- jfloat ----//

typedef struct {
    PyObject_HEAD
    jfloat value;
} jfloat_Object;

static int jfloat_init(jfloat_Object* self, PyObject* args)
{
    float value = 0;
    if ( ! PyArg_ParseTuple(args, "|f", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jfloat_bool(jfloat_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jfloat_as_number = {
    .nb_bool = (inquiry)jfloat_bool,
};

static PyMemberDef jfloat_members[] =
{
    {"value", T_FLOAT, offsetof(jfloat_Object, value)},
    {NULL}
};

PyTypeObject jfloat_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jfloat",
    .tp_basicsize = sizeof(jfloat_Object),
    .tp_itemsize  = member_size(jfloat_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jfloat_as_number,
    .tp_members   = jfloat_members,
    .tp_init      = (initproc)jfloat_init,
    .tp_new       = PyType_GenericNew,
};

//---- jdouble ---//

typedef struct {
    PyObject_HEAD
    jdouble value;
} jdouble_Object;

static int jdouble_init(jdouble_Object* self, PyObject* args)
{
    double value = 0;
    if ( ! PyArg_ParseTuple(args, "|d", &value) )
        return -1;
    self->value = value;
    return 0;
}

static int jdouble_bool(jdouble_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jdouble_as_number = {
    .nb_bool = (inquiry)jdouble_bool,
};

static PyMemberDef jdouble_members[] =
{
    {"value", T_DOUBLE, offsetof(jdouble_Object, value)},
    {NULL}
};

PyTypeObject jdouble_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jdouble",
    .tp_basicsize = sizeof(jdouble_Object),
    .tp_itemsize  = member_size(jdouble_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jdouble_as_number,
    .tp_members   = jdouble_members,
    .tp_init      = (initproc)jdouble_init,
    .tp_new       = PyType_GenericNew,
};

//----- jsize ----//

#define jsize_Type jint_Type

//---- jobject ---//

typedef struct {
    PyObject_HEAD
    jobject value;
} jobject_Object;

static int jobject_init(jobject_Object* self, PyObject* args)
{
    PyObject* object = Py_None;
    if ( ! PyArg_ParseTuple(args, "|O", &object) )
        return -1;
    Py_ssize_t value = 0;
    if ( object != Py_None &&
         ! PyArg_ParseTuple(args, "|n", &value) )
        return -1;
    self->value = (jobject)value;
    return 0;
}

static int jobject_bool(jobject_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jobject_as_number = {
    .nb_bool = (inquiry)jobject_bool,
};

static PyObject* jobject_value_get(jobject_Object* self)
{
    if ( self->value == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->value);
}

static int jobject_value_set(jobject_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
    if ( not_None && value == NULL )
        return -1;
    self->value = (jobject)value;
    return 0;
}

static PyGetSetDef jobject_getsets[] =
{
    {"value", (getter)jobject_value_get, (setter)jobject_value_set},
    {NULL}
};

PyTypeObject jobject_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jobject",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jobject_as_number,
    .tp_getset    = jobject_getsets,
    .tp_init      = (initproc)jobject_init,
    .tp_new       = PyType_GenericNew,
};

//-- jclass ... --//

static PyTypeObject jclass_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jclass",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jobject_Type,
    .tp_new       = PyType_GenericNew,
};

//-- jthrowable ... --//

static PyTypeObject jthrowable_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jthrowable",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jobject_Type,
    .tp_new       = PyType_GenericNew,
};

//-- jstring ... --//

static PyTypeObject jstring_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jstring",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jobject_Type,
    .tp_new       = PyType_GenericNew,
};

//-- jarays's ... --//

static PyTypeObject jarray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jarray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_base      = &jobject_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jbooleanArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jbooleanArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jcharArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jcharArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jbyteArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jbyteArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jshortArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jshortArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jintArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jintArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jlongArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jlongArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jfloatArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jfloatArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jdoubleArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jdoubleArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

static PyTypeObject jobjectArray_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jobjectArray",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &jarray_Type,
    .tp_new       = PyType_GenericNew,
};

//-- jweak ... --//

#define jweak_Type jobject_Type

//---- jvalue ----//

typedef struct {
    PyObject_HEAD
    jvalue this;
} jvalue_Object;

static PyObject* jvalue_z_get(jvalue_Object* self)
{
    return PyLong_FromLong((long)self->this.z);
}

static int jvalue_z_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jboolean_Type) )
        self->this.z = ((jboolean_Object*)val)->value;
    else
    {
        long value = PyLong_AsLong(val);
        if ( value == -1 && PyErr_Occurred() )
            return -1;
        self->this.z = (jboolean)value;
    }
    return 0;
}

static PyObject* jvalue_b_get(jvalue_Object* self)
{
    return PyLong_FromLong((long)self->this.b);
}

static int jvalue_b_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jbyte_Type) )
        self->this.b = ((jbyte_Object*)val)->value;
    else
    {
        long value = PyLong_AsLong(val);
        if ( value == -1 && PyErr_Occurred() )
            return -1;
        self->this.b = (jbyte)value;
    }
    return 0;
}

static PyObject* jvalue_c_get(jvalue_Object* self)
{
    return PyUnicode_FromWideChar((const wchar_t*)&self->this.c, 1);
}

static int jvalue_c_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jchar_Type) )
        self->this.c = ((jchar_Object*)val)->value;
    else
    {
        wchar_t value = 0;
        if ( PyUnicode_AsWideChar(val, &value, 1) == -1 )
            return -1;
        if ( PyUnicode_GetLength(val) != 1 )
        {
            PyErr_SetString(PyExc_TypeError,
                            "one unicode character expected, not str");
            return -1;
        }
        self->this.c = (jchar)value;
    }
    return 0;
}

static PyObject* jvalue_s_get(jvalue_Object* self)
{
    return PyLong_FromLong((long)self->this.s);
}

static int jvalue_s_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jshort_Type) )
        self->this.s = ((jshort_Object*)val)->value;
    else
    {
        long value = PyLong_AsLong(val);
        if ( value == -1 && PyErr_Occurred() )
            return -1;
        self->this.s = (jshort)value;
    }
    return 0;
}

static PyObject* jvalue_i_get(jvalue_Object* self)
{
    return PyLong_FromLong((long)self->this.i);
}

static int jvalue_i_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jint_Type) )
        self->this.i = ((jint_Object*)val)->value;
    else
    {
        long value = PyLong_AsLong(val);
        if ( value == -1 && PyErr_Occurred() )
            return -1;
        self->this.i = (jint)value;
    }
    return 0;
}

static PyObject* jvalue_j_get(jvalue_Object* self)
{
    return PyLong_FromLongLong((PY_LONG_LONG)self->this.j);
}

static int jvalue_j_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jlong_Type) )
        self->this.j = ((jlong_Object*)val)->value;
    else
    {
        PY_LONG_LONG value = PyLong_AsLongLong(val);
        if ( value == -1 && PyErr_Occurred() )
            return -1;
        self->this.j = (jlong)value;
    }
    return 0;
}

static PyObject* jvalue_f_get(jvalue_Object* self)
{
    return PyFloat_FromDouble((double)self->this.f);
}

static int jvalue_f_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jfloat_Type) )
        self->this.f = ((jfloat_Object*)val)->value;
    else
    {
        double value = PyFloat_AsDouble(val);
        if ( value == -1.0 && PyErr_Occurred() )
            return -1;
        self->this.f = (jfloat)value;
    }
    return 0;
}

static PyObject* jvalue_d_get(jvalue_Object* self)
{
    return PyFloat_FromDouble((double)self->this.d);
}

static int jvalue_d_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jdouble_Type) )
        self->this.d = ((jdouble_Object*)val)->value;
    else
    {
        double value = PyFloat_AsDouble(val);
        if ( value == -1.0 && PyErr_Occurred() )
            return -1;
        self->this.d = (jdouble)value;
    }
    return 0;
}

static PyObject* jvalue_l_get(jvalue_Object* self)
{
    if ( self->this.l == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->this.l);
}

static int jvalue_l_set(jvalue_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jobject_Type) )
        self->this.l = ((jobject_Object*)val)->value;
    else
    {
        int not_None = (val != Py_None);
        void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
        if ( not_None && value == NULL )
            return -1;
        self->this.l = (jobject)value;
    }
    return 0;
}

static PyGetSetDef jvalue_getsets[] =
{
    {"z", (getter)jvalue_z_get, (setter)jvalue_z_set},
    {"b", (getter)jvalue_b_get, (setter)jvalue_b_set},
    {"c", (getter)jvalue_c_get, (setter)jvalue_c_set},
    {"s", (getter)jvalue_s_get, (setter)jvalue_s_set},
    {"i", (getter)jvalue_i_get, (setter)jvalue_i_set},
    {"j", (getter)jvalue_j_get, (setter)jvalue_j_set},
    {"f", (getter)jvalue_f_get, (setter)jvalue_f_set},
    {"d", (getter)jvalue_d_get, (setter)jvalue_d_set},
    {"l", (getter)jvalue_l_get, (setter)jvalue_l_set},
    {NULL}
};

PyTypeObject jvalue_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jvalue",
    .tp_basicsize = sizeof(jvalue_Object),
    .tp_itemsize  = member_size(jvalue_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_getset    = jvalue_getsets,
    .tp_new       = PyType_GenericNew,
};

//--- jfieldID ---//

typedef struct {
    PyObject_HEAD
    jfieldID value;
} jfieldID_Object;

static int jfieldID_init(jfieldID_Object* self, PyObject* args)
{
    PyObject* object = Py_None;
    if ( ! PyArg_ParseTuple(args, "|O", &object) )
        return -1;
    Py_ssize_t value = 0;
    if ( object != Py_None &&
         ! PyArg_ParseTuple(args, "|n", &value) )
        return -1;
    self->value = (jfieldID)value;
    return 0;
}

static int jfieldID_bool(jfieldID_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jfieldID_as_number = {
    .nb_bool = (inquiry)jfieldID_bool,
};

static PyObject* jfieldID_value_get(jfieldID_Object* self)
{
    if ( self->value == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->value);
}

static int jfieldID_value_set(jfieldID_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
    if ( not_None && value == NULL )
        return -1;
    self->value = (jfieldID)value;
    return 0;
}

static PyGetSetDef jfieldID_getsets[] =
{
    {"value", (getter)jfieldID_value_get, (setter)jfieldID_value_set},
    {NULL}
};

PyTypeObject jfieldID_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jfieldID",
    .tp_basicsize = sizeof(jfieldID_Object),
    .tp_itemsize  = member_size(jfieldID_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jfieldID_as_number,
    .tp_getset    = jfieldID_getsets,
    .tp_init      = (initproc)jfieldID_init,
    .tp_new       = PyType_GenericNew,
};

//--- jmethodID --//

typedef struct {
    PyObject_HEAD
    jmethodID value;
} jmethodID_Object;

static int jmethodID_init(jmethodID_Object* self, PyObject* args)
{
    PyObject* object = Py_None;
    if ( ! PyArg_ParseTuple(args, "|O", &object) )
        return -1;
    Py_ssize_t value = 0;
    if ( object != Py_None &&
         ! PyArg_ParseTuple(args, "|n", &value) )
        return -1;
    self->value = (jmethodID)value;
    return 0;
}

static int jmethodID_bool(jmethodID_Object* self)
{
    return !!self->value;
}

static PyNumberMethods jmethodID_as_number = {
    .nb_bool = (inquiry)jmethodID_bool,
};

static PyObject* jmethodID_value_get(jmethodID_Object* self)
{
    if ( self->value == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->value);
}

static int jmethodID_value_set(jmethodID_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
    if ( not_None && value == NULL )
        return -1;
    self->value = (jmethodID)value;
    return 0;
}

static PyGetSetDef jmethodID_getsets[] =
{
    {"value", (getter)jmethodID_value_get, (setter)jmethodID_value_set},
    {NULL}
};

PyTypeObject jmethodID_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.jmethodID",
    .tp_basicsize = sizeof(jmethodID_Object),
    .tp_itemsize  = member_size(jmethodID_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jmethodID_as_number,
    .tp_getset    = jmethodID_getsets,
    .tp_init      = (initproc)jmethodID_init,
    .tp_new       = PyType_GenericNew,
};

//-- jobjectRefType --//

#define jobjectRefType_Type PyLong_Type

//----------- null constant ----------//

//NULL   = obj(jobject, 0)
//isNULL = lambda jobj: not bool(jobj)

//---- JNI Native Method Interface ---//

// used in RegisterNatives to describe native method name, signature,
// and function pointer.

typedef struct {
    PyObject_HEAD
    JNINativeMethod this;
} JNINativeMethod_Object;

static PyObject* JNINativeMethod_name_get(JNINativeMethod_Object* self)
{
    if ( self->this.name == NULL )
        Py_RETURN_NONE;
    else
        return PyBytes_FromString(self->this.name);
}

static int JNINativeMethod_name_set(JNINativeMethod_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    char* name = not_None ? PyBytes_AsString(val) : NULL;
    if ( not_None && name == NULL )
        return -1;
    self->this.name = name;
    return 0;
}

static PyObject* JNINativeMethod_signature_get(JNINativeMethod_Object* self)
{
    if ( self->this.signature == NULL )
        Py_RETURN_NONE;
    else
        return PyBytes_FromString(self->this.signature);
}

static int JNINativeMethod_signature_set(JNINativeMethod_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    char* signature = not_None ? PyBytes_AsString(val) : NULL;
    if ( not_None && signature == NULL )
        return -1;
    self->this.signature = signature;
    return 0;
}

static PyObject* JNINativeMethod_fnPtr_get(JNINativeMethod_Object* self)
{
    if ( self->this.fnPtr == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->this.fnPtr);
}

static int JNINativeMethod_fnPtr_set(JNINativeMethod_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jobject_Type) )
        self->this.fnPtr = ((jobject_Object*)val)->value;
    else
    {
        int not_None = (val != Py_None);
        void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
        if ( not_None && value == NULL )
            return -1;
        self->this.fnPtr = (void*)value;
    }
    return 0;
}

static PyGetSetDef JNINativeMethod_getsets[] =
{
    {"name",      (getter)JNINativeMethod_name_get,
                  (setter)JNINativeMethod_name_set},
    {"signature", (getter)JNINativeMethod_signature_get,
                  (setter)JNINativeMethod_signature_set},
    {"fnPtr",     (getter)JNINativeMethod_fnPtr_get,
                  (setter)JNINativeMethod_fnPtr_set},
    {NULL}
};

PyTypeObject JNINativeMethod_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.JNINativeMethod",
    .tp_basicsize = sizeof(JNINativeMethod_Object),
    .tp_itemsize  = member_size(JNINativeMethod_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_getset    = JNINativeMethod_getsets,
    .tp_new       = PyType_GenericNew,
};

//----- JNI Invocation Interface -----//

//------ JavaVMOption ------//

typedef struct {
    PyObject_HEAD
    JavaVMOption this;
} JavaVMOption_Object;

static PyObject* JavaVMOption_optionString_get(JavaVMOption_Object* self)
{
    if ( self->this.optionString == NULL )
        Py_RETURN_NONE;
    else
        return PyBytes_FromString(self->this.optionString);
}

static int JavaVMOption_optionString_set(JavaVMOption_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    char* optionString = not_None ? PyBytes_AsString(val) : NULL;
    if ( not_None && optionString == NULL )
        return -1;
    self->this.optionString = optionString;
    return 0;
}

static PyObject* JavaVMOption_extraInfo_get(JavaVMOption_Object* self)
{
    if ( self->this.extraInfo == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->this.extraInfo);
}

static int JavaVMOption_extraInfo_set(JavaVMOption_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jobject_Type) )
        self->this.extraInfo = ((jobject_Object*)val)->value;
    else
    {
        int not_None = (val != Py_None);
        void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
        if ( not_None && value == NULL )
            return -1;
        self->this.extraInfo = (void*)value;
    }
    return 0;
}

static PyGetSetDef JavaVMOption_getsets[] =
{
    {"optionString", (getter)JavaVMOption_optionString_get,
                     (setter)JavaVMOption_optionString_set},
    {"extraInfo",    (getter)JavaVMOption_extraInfo_get,
                     (setter)JavaVMOption_extraInfo_set},
    {NULL}
};

PyTypeObject JavaVMOption_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.JavaVMOption",
    .tp_basicsize = sizeof(JavaVMOption_Object),
    .tp_itemsize  = member_size(JavaVMOption_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_getset    = JavaVMOption_getsets,
    .tp_new       = PyType_GenericNew,
};

//----- JavaVMInitArgs -----//

typedef struct {
    PyObject_HEAD
    JavaVMInitArgs this;
} JavaVMInitArgs_Object;

static PyObject* JavaVMInitArgs_version_get(JavaVMInitArgs_Object* self)
{
    return PyLong_FromLong((long)self->this.version);
}

static int JavaVMInitArgs_version_set(JavaVMInitArgs_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jint_Type) )
        self->this.version = ((jint_Object*)val)->value;
    else
    {
        long version = PyLong_AsLong(val);
        if ( version == -1 && PyErr_Occurred() )
            return -1;
        self->this.version = (jint)version;
    }
    return 0;
}

static PyObject* JavaVMInitArgs_nOptions_get(JavaVMInitArgs_Object* self)
{
    return PyLong_FromLong((long)self->this.nOptions);
}

static int JavaVMInitArgs_nOptions_set(JavaVMInitArgs_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jint_Type) )
        self->this.nOptions = ((jint_Object*)val)->value;
    else
    {
        long nOptions = PyLong_AsLong(val);
        if ( nOptions == -1 && PyErr_Occurred() )
            return -1;
        self->this.nOptions = (jint)nOptions;
    }
    return 0;
}

static PyObject* JavaVMInitArgs_options_get(JavaVMInitArgs_Object* self)
{
    if ( self->this.options == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->this.options);
}

static int JavaVMInitArgs_options_set(JavaVMInitArgs_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jobject_Type) )
        self->this.options = (JavaVMOption*)((jobject_Object*)val)->value;
    else
    {
        int not_None = (val != Py_None);
        void* value = not_None ? PyLong_AsVoidPtr(val) : NULL;
        if ( not_None && value == NULL )
            return -1;
        self->this.options = (JavaVMOption*)value;
    }
    return 0;
}

static PyObject* JavaVMInitArgs_ignoreUnrecognized_get(JavaVMInitArgs_Object* self)
{
    return PyLong_FromLong((long)self->this.ignoreUnrecognized);
}

static int JavaVMInitArgs_ignoreUnrecognized_set(JavaVMInitArgs_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jboolean_Type) )
        self->this.ignoreUnrecognized = ((jboolean_Object*)val)->value;
    else
    {
        long value = PyLong_AsLong(val);
        if ( value == -1 && PyErr_Occurred() )
            return -1;
        self->this.ignoreUnrecognized = (jboolean)value;
    }
    return 0;
}

static PyGetSetDef JavaVMInitArgs_getsets[] =
{
    {"version",            (getter)JavaVMInitArgs_version_get,
                           (setter)JavaVMInitArgs_version_set},
    {"nOptions",           (getter)JavaVMInitArgs_nOptions_get,
                           (setter)JavaVMInitArgs_nOptions_set},
    {"options",            (getter)JavaVMInitArgs_options_get,
                           (setter)JavaVMInitArgs_options_set},
    {"ignoreUnrecognized", (getter)JavaVMInitArgs_ignoreUnrecognized_get,
                           (setter)JavaVMInitArgs_ignoreUnrecognized_set},
    {NULL}
};

PyTypeObject JavaVMInitArgs_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.JavaVMInitArgs",
    .tp_basicsize = sizeof(JavaVMInitArgs_Object),/* tp_basicsize */
    .tp_itemsize  = member_size(JavaVMInitArgs_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_getset    = JavaVMInitArgs_getsets,
    .tp_new       = PyType_GenericNew,
};

//---- JavaVMAttachArgs ----//

typedef struct {
    PyObject_HEAD
    JavaVMAttachArgs this;
} JavaVMAttachArgs_Object;

static PyObject* JavaVMAttachArgs_version_get(JavaVMAttachArgs_Object* self)
{
    return PyLong_FromLong((long)self->this.version);
}

static int JavaVMAttachArgs_version_set(JavaVMAttachArgs_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jint_Type) )
        self->this.version = ((jint_Object*)val)->value;
    else
    {
        long version = PyLong_AsLong(val);
        if ( version == -1 && PyErr_Occurred() )
            return -1;
        self->this.version = (jint)version;
    }
    return 0;
}

static PyObject* JavaVMAttachArgs_name_get(JavaVMAttachArgs_Object* self)
{
    if ( self->this.name == NULL )
        Py_RETURN_NONE;
    else
        return PyBytes_FromString(self->this.name);
}

static int JavaVMAttachArgs_name_set(JavaVMAttachArgs_Object* self, PyObject* val)
{
    int not_None = (val != Py_None);
    char* name = not_None ? PyBytes_AsString(val) : NULL;
    if ( not_None && name == NULL )
        return -1;
    self->this.name = name;
    return 0;
}

static PyObject* JavaVMAttachArgs_group_get(JavaVMAttachArgs_Object* self)
{
    if ( self->this.group == NULL )
        Py_RETURN_NONE;
    else
        return PyLong_FromVoidPtr((void*)self->this.group);
}

static int JavaVMAttachArgs_group_set(JavaVMAttachArgs_Object* self, PyObject* val)
{
    if ( PyObject_TypeCheck(val, &jobject_Type) )
        self->this.group = ((jobject_Object*)val)->value;
    else
    {
        int not_None = (val != Py_None);
        void* group = not_None ? PyLong_AsVoidPtr(val) : NULL;
        if ( not_None && group == NULL )
            return -1;
        self->this.group = (jobject)group;
    }
    return 0;
}

static PyGetSetDef JavaVMAttachArgs_getsets[] =
{
    {"version", (getter)JavaVMAttachArgs_version_get,
                (setter)JavaVMAttachArgs_version_set},
    {"name",    (getter)JavaVMAttachArgs_name_get,
                (setter)JavaVMAttachArgs_name_set},
    {"group",   (getter)JavaVMAttachArgs_group_get,
                (setter)JavaVMAttachArgs_group_set},
    {NULL}
};

PyTypeObject JavaVMAttachArgs_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.JavaVMAttachArgs",
    .tp_basicsize = sizeof(JavaVMAttachArgs_Object),
    .tp_itemsize  = member_size(JavaVMAttachArgs_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_getset    = JavaVMAttachArgs_getsets,
    .tp_new       = PyType_GenericNew,
};

//-------------- JNIEnv --------------//

typedef struct {
    PyObject_HEAD
    JNIEnv this; // JNIEnv* jenv; ???
} JNIEnv_Object;

static PyObject* _handle_JNIException(jint err)
{
    //import sys
    //fun_name = sys._getframe(1).f_code.co_name
    //raise JNIException(err, info=fun_name)
    return NULL;
}

static PyObject* _handle_JavaException(JNIEnv_Object* self)
{
    //fun = self.functions[0]
    //jthr = fun.ExceptionOccurred(self)
    //fun.ExceptionClear(self)
    //jexc = fun.NewGlobalRef(self, jthr)
    //fun.DeleteLocalRef(self, jthr)
    //if Throwable.last:
    //    jthr = Throwable.last.getJThrowable()
    //    if jthr: fun.DeleteGlobalRef(self, jthr)
    //    Throwable.last = None
    //fun.ExceptionClear(self)
    //Throwable.last = thr = Throwable(jexc)#!!!, fname)
    //raise thr
    return NULL;
}

// Java version

static PyObject* GetVersion(JNIEnv_Object* self)
{
    JNIEnv jenv = self->this;
    jint ret = jenv->GetVersion(&jenv);
    return PyLong_FromLong((long)ret);
}

/*
static PyObject* jint GetVersion()
{
    j??? ret = jenv->GetVersion(&jenv);
}

static PyObject* jclass DefineClass(const char *name, jobject loader, const jbyte *buf,
                       jsize len)
{
    j??? ret = jenv->DefineClass(&jenv, name, loader, buf, len);
}

static PyObject* jclass FindClass(const char *name)
{
    j??? ret = jenv->FindClass(&jenv, name);
}

static PyObject* jmethodID FromReflectedMethod(jobject method)
{
    j??? ret = jenv->FromReflectedMethod(&jenv,method);
}

static PyObject* jfieldID FromReflectedField(jobject field)
{
    j??? ret = jenv->FromReflectedField(&jenv,field);
}


static PyObject* jobject ToReflectedMethod(jclass cls, jmethodID methodID, jboolean isStatic)
{
    j??? ret = jenv->ToReflectedMethod(&jenv, cls, methodID, isStatic);
}


static PyObject* jclass GetSuperclass(jclass sub)
{
    j??? ret = jenv->GetSuperclass(&jenv, sub);
}

static PyObject* jboolean IsAssignableFrom(jclass sub, jclass sup)
{
    j??? ret = jenv->IsAssignableFrom(&jenv, sub, sup);
}


static PyObject* jobject ToReflectedField(jclass cls, jfieldID fieldID, jboolean isStatic)
{
    j??? ret = jenv->ToReflectedField(&jenv,cls,fieldID,isStatic);
}


static PyObject* jint Throw(jthrowable obj)
{
    j??? ret = jenv->Throw(&jenv, obj);
}

static PyObject* jint ThrowNew(jclass clazz, const char *msg)
{
    j??? ret = jenv->ThrowNew(&jenv, clazz, msg);
}

static PyObject* jthrowable ExceptionOccurred()
{
    j??? ret = jenv->ExceptionOccurred(&jenv);
}

static PyObject* ExceptionDescribe()
{
    jenv->ExceptionDescribe(&jenv);
}

static PyObject* ExceptionClear()
{
    jenv->ExceptionClear(&jenv);
}

static PyObject* FatalError(const char *msg)
{
    jenv->FatalError(&jenv, msg);
}


static PyObject* jint PushLocalFrame(jint capacity)
{
    j??? ret = jenv->PushLocalFrame(&jenv,capacity);
}

static PyObject* jobject PopLocalFrame(jobject result)
{
    j??? ret = jenv->PopLocalFrame(&jenv,result);
}


static PyObject* jobject NewGlobalRef(jobject lobj)
{
    j??? ret = jenv->NewGlobalRef(&jenv,lobj);
}

static PyObject* DeleteGlobalRef(jobject gref)
{
    jenv->DeleteGlobalRef(&jenv,gref);
}

static PyObject* DeleteLocalRef(jobject obj)
{
    jenv->DeleteLocalRef(&jenv, obj);
}


static PyObject* jboolean IsSameObject(jobject obj1, jobject obj2)
{
    j??? ret = jenv->IsSameObject(&jenv,obj1,obj2);
}


static PyObject* jobject NewLocalRef(jobject ref)
{
    j??? ret = jenv->NewLocalRef(&jenv,ref);
}

static PyObject* jint EnsureLocalCapacity(jint capacity)
{
    j??? ret = jenv->EnsureLocalCapacity(&jenv,capacity);
}


static PyObject* jobject AllocObject(jclass clazz)
{
    j??? ret = jenv->AllocObject(&jenv,clazz);
}

static PyObject* jobject NewObject(jclass clazz, jmethodID methodID, ...)
{
        va_list args;
        jobject result;
        va_start(args, methodID);
        result = functions->NewObjectV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jobject NewObjectV(jclass clazz, jmethodID methodID,
                       va_list args)
{
    j??? ret = jenv->NewObjectV(&jenv,clazz,methodID,args);
}

static PyObject* jobject NewObjectA(jclass clazz, jmethodID methodID,
                       const jvalue *args)
{
    j??? ret = jenv->NewObjectA(&jenv,clazz,methodID,args);
}


static PyObject* jclass GetObjectClass(jobject obj)
{
    j??? ret = jenv->GetObjectClass(&jenv,obj);
}

static PyObject* jboolean IsInstanceOf(jobject obj, jclass clazz)
{
    j??? ret = jenv->IsInstanceOf(&jenv,obj,clazz);
}


static PyObject* jmethodID GetMethodID(jclass clazz, const char *name,
                          const char *sig)
{
    j??? ret = jenv->GetMethodID(&jenv,clazz,name,sig);
}


static PyObject* jobject CallObjectMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jobject result;
        va_start(args,methodID);
        result = functions->CallObjectMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jobject CallObjectMethodV(jobject obj, jmethodID methodID,
                        va_list args)
{
    j??? ret = jenv->CallObjectMethodV(&jenv,obj,methodID,args);
}

static PyObject* jobject CallObjectMethodA(jobject obj, jmethodID methodID,
                        const jvalue * args)
{
    j??? ret = jenv->CallObjectMethodA(&jenv,obj,methodID,args);
}


static PyObject* jboolean CallBooleanMethod(jobject obj,
                               jmethodID methodID, ...)
{
        va_list args;
        jboolean result;
        va_start(args,methodID);
        result = functions->CallBooleanMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jboolean CallBooleanMethodV(jobject obj, jmethodID methodID,
                                va_list args)
{
    j??? ret = jenv->CallBooleanMethodV(&jenv,obj,methodID,args);
}

static PyObject* jboolean CallBooleanMethodA(jobject obj, jmethodID methodID,
                                const jvalue * args)
{
    j??? ret = jenv->CallBooleanMethodA(&jenv,obj,methodID, args);
}


static PyObject* jbyte CallByteMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jbyte result;
        va_start(args,methodID);
        result = functions->CallByteMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jbyte CallByteMethodV(jobject obj, jmethodID methodID,
                          va_list args)
{
    j??? ret = jenv->CallByteMethodV(&jenv,obj,methodID,args);
}

static PyObject* jbyte CallByteMethodA(jobject obj, jmethodID methodID,
                          const jvalue * args)
{
    j??? ret = jenv->CallByteMethodA(&jenv,obj,methodID,args);
}


static PyObject* jchar CallCharMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jchar result;
        va_start(args,methodID);
        result = functions->CallCharMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jchar CallCharMethodV(jobject obj, jmethodID methodID,
                          va_list args)
{
    j??? ret = jenv->CallCharMethodV(&jenv,obj,methodID,args);
}

static PyObject* jchar CallCharMethodA(jobject obj, jmethodID methodID,
                          const jvalue * args)
{
    j??? ret = jenv->CallCharMethodA(&jenv,obj,methodID,args);
}


static PyObject* jshort CallShortMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jshort result;
        va_start(args,methodID);
        result = functions->CallShortMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jshort CallShortMethodV(jobject obj, jmethodID methodID,
                            va_list args)
{
    j??? ret = jenv->CallShortMethodV(&jenv,obj,methodID,args);
}

static PyObject* jshort CallShortMethodA(jobject obj, jmethodID methodID,
                            const jvalue * args)
{
    j??? ret = jenv->CallShortMethodA(&jenv,obj,methodID,args);
}


static PyObject* jint CallIntMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jint result;
        va_start(args,methodID);
        result = functions->CallIntMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jint CallIntMethodV(jobject obj, jmethodID methodID,
                        va_list args)
{
    j??? ret = jenv->CallIntMethodV(&jenv,obj,methodID,args);
}

static PyObject* jint CallIntMethodA(jobject obj, jmethodID methodID,
                        const jvalue * args)
{
    j??? ret = jenv->CallIntMethodA(&jenv,obj,methodID,args);
}


static PyObject* jlong CallLongMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jlong result;
        va_start(args,methodID);
        result = functions->CallLongMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jlong CallLongMethodV(jobject obj, jmethodID methodID,
                          va_list args)
{
    j??? ret = jenv->CallLongMethodV(&jenv,obj,methodID,args);
}

static PyObject* jlong CallLongMethodA(jobject obj, jmethodID methodID,
                          const jvalue * args)
{
    j??? ret = jenv->CallLongMethodA(&jenv,obj,methodID,args);
}


static PyObject* jfloat CallFloatMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jfloat result;
        va_start(args,methodID);
        result = functions->CallFloatMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jfloat CallFloatMethodV(jobject obj, jmethodID methodID,
                            va_list args)
{
    j??? ret = jenv->CallFloatMethodV(&jenv,obj,methodID,args);
}

static PyObject* jfloat CallFloatMethodA(jobject obj, jmethodID methodID,
                            const jvalue * args)
{
    j??? ret = jenv->CallFloatMethodA(&jenv,obj,methodID,args);
}


static PyObject* jdouble CallDoubleMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        jdouble result;
        va_start(args,methodID);
        result = functions->CallDoubleMethodV(&jenv,obj,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jdouble CallDoubleMethodV(jobject obj, jmethodID methodID,
                        va_list args)
{
    j??? ret = jenv->CallDoubleMethodV(&jenv,obj,methodID,args);
}

static PyObject* jdouble CallDoubleMethodA(jobject obj, jmethodID methodID,
                        const jvalue * args)
{
    j??? ret = jenv->CallDoubleMethodA(&jenv,obj,methodID,args);
}


static PyObject* CallVoidMethod(jobject obj, jmethodID methodID, ...)
{
        va_list args;
        va_start(args,methodID);
    jenv->CallVoidMethodV(&jenv,obj,methodID,args);
        va_end(args);
}

static PyObject* CallVoidMethodV(jobject obj, jmethodID methodID,
                         va_list args)
{
    jenv->CallVoidMethodV(&jenv,obj,methodID,args);
}

static PyObject* CallVoidMethodA(jobject obj, jmethodID methodID,
                         const jvalue * args)
{
    jenv->CallVoidMethodA(&jenv,obj,methodID,args);
}


static PyObject* jobject CallNonvirtualObjectMethod(jobject obj, jclass clazz,
                                       jmethodID methodID, ...)
{
        va_list args;
        jobject result;
        va_start(args,methodID);
        result = functions->CallNonvirtualObjectMethodV(&jenv,obj,clazz,
                                                        methodID,args);
        va_end(args);
        return result;
}

static PyObject* jobject CallNonvirtualObjectMethodV(jobject obj, jclass clazz,
                                        jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualObjectMethodV(&jenv,obj,clazz,
                                                      methodID,args);
}

static PyObject* jobject CallNonvirtualObjectMethodA(jobject obj, jclass clazz,
                                        jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualObjectMethodA(&jenv,obj,clazz,
                                                      methodID,args);
}


static PyObject* jboolean CallNonvirtualBooleanMethod(jobject obj, jclass clazz,
                                         jmethodID methodID, ...)
{
        va_list args;
        jboolean result;
        va_start(args,methodID);
        result = functions->CallNonvirtualBooleanMethodV(&jenv,obj,clazz,
                                                         methodID,args);
        va_end(args);
        return result;
}

static PyObject* jboolean CallNonvirtualBooleanMethodV(jobject obj, jclass clazz,
                                          jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualBooleanMethodV(&jenv,obj,clazz,
                                                       methodID,args);
}

static PyObject* jboolean CallNonvirtualBooleanMethodA(jobject obj, jclass clazz,
                                          jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualBooleanMethodA(&jenv,obj,clazz,
                                                       methodID, args);
}


static PyObject* jbyte CallNonvirtualByteMethod(jobject obj, jclass clazz,
                                   jmethodID methodID, ...)
{
        va_list args;
        jbyte result;
        va_start(args,methodID);
        result = functions->CallNonvirtualByteMethodV(&jenv,obj,clazz,
                                                      methodID,args);
        va_end(args);
        return result;
}

static PyObject* jbyte CallNonvirtualByteMethodV(jobject obj, jclass clazz,
                                    jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualByteMethodV(&jenv,obj,clazz,
                                                    methodID,args);
}

static PyObject* jbyte CallNonvirtualByteMethodA(jobject obj, jclass clazz,
                                    jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualByteMethodA(&jenv,obj,clazz,
                                                    methodID,args);
}


static PyObject* jchar CallNonvirtualCharMethod(jobject obj, jclass clazz,
                                   jmethodID methodID, ...)
{
        va_list args;
        jchar result;
        va_start(args,methodID);
        result = functions->CallNonvirtualCharMethodV(&jenv,obj,clazz,
                                                      methodID,args);
        va_end(args);
        return result;
}

static PyObject* jchar CallNonvirtualCharMethodV(jobject obj, jclass clazz,
                                    jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualCharMethodV(&jenv,obj,clazz,
                                                    methodID,args);
}

static PyObject* jchar CallNonvirtualCharMethodA(jobject obj, jclass clazz,
                                    jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualCharMethodA(&jenv,obj,clazz,
                                                    methodID,args);
}


static PyObject* jshort CallNonvirtualShortMethod(jobject obj, jclass clazz,
                                     jmethodID methodID, ...)
{
        va_list args;
        jshort result;
        va_start(args,methodID);
        result = functions->CallNonvirtualShortMethodV(&jenv,obj,clazz,
                                                       methodID,args);
        va_end(args);
        return result;
}

static PyObject* jshort CallNonvirtualShortMethodV(jobject obj, jclass clazz,
                                      jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualShortMethodV(&jenv,obj,clazz,
                                                     methodID,args);
}

static PyObject* jshort CallNonvirtualShortMethodA(jobject obj, jclass clazz,
                                      jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualShortMethodA(&jenv,obj,clazz,
                                                     methodID,args);
}


static PyObject* jint CallNonvirtualIntMethod(jobject obj, jclass clazz,
                                 jmethodID methodID, ...)
{
        va_list args;
        jint result;
        va_start(args,methodID);
        result = functions->CallNonvirtualIntMethodV(&jenv,obj,clazz,
                                                     methodID,args);
        va_end(args);
        return result;
}

static PyObject* jint CallNonvirtualIntMethodV(jobject obj, jclass clazz,
                                  jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualIntMethodV(&jenv,obj,clazz,
                                                   methodID,args);
}

static PyObject* jint CallNonvirtualIntMethodA(jobject obj, jclass clazz,
                                  jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualIntMethodA(&jenv,obj,clazz,
                                                   methodID,args);
}


static PyObject* jlong CallNonvirtualLongMethod(jobject obj, jclass clazz,
                                   jmethodID methodID, ...)
{
        va_list args;
        jlong result;
        va_start(args,methodID);
        result = functions->CallNonvirtualLongMethodV(&jenv,obj,clazz,
                                                      methodID,args);
        va_end(args);
        return result;
}

static PyObject* jlong CallNonvirtualLongMethodV(jobject obj, jclass clazz,
                                    jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallNonvirtualLongMethodV(&jenv,obj,clazz,
                                                    methodID,args);
}

static PyObject* jlong CallNonvirtualLongMethodA(jobject obj, jclass clazz,
                                    jmethodID methodID, const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualLongMethodA(&jenv,obj,clazz,
                                                    methodID,args);
}


static PyObject* jfloat CallNonvirtualFloatMethod(jobject obj, jclass clazz,
                                     jmethodID methodID, ...)
{
        va_list args;
        jfloat result;
        va_start(args,methodID);
        result = functions->CallNonvirtualFloatMethodV(&jenv,obj,clazz,
                                                       methodID,args);
        va_end(args);
        return result;
}

static PyObject* jfloat CallNonvirtualFloatMethodV(jobject obj, jclass clazz,
                                      jmethodID methodID,
                                      va_list args)
{
    j??? ret = jenv->CallNonvirtualFloatMethodV(&jenv,obj,clazz,
                                                     methodID,args);
}

static PyObject* jfloat CallNonvirtualFloatMethodA(jobject obj, jclass clazz,
                                      jmethodID methodID,
                                      const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualFloatMethodA(&jenv,obj,clazz,
                                                     methodID,args);
}


static PyObject* jdouble CallNonvirtualDoubleMethod(jobject obj, jclass clazz,
                                       jmethodID methodID, ...)
{
        va_list args;
        jdouble result;
        va_start(args,methodID);
        result = functions->CallNonvirtualDoubleMethodV(&jenv,obj,clazz,
                                                        methodID,args);
        va_end(args);
        return result;
}

static PyObject* jdouble CallNonvirtualDoubleMethodV(jobject obj, jclass clazz,
                                        jmethodID methodID,
                                        va_list args)
{
    j??? ret = jenv->CallNonvirtualDoubleMethodV(&jenv,obj,clazz,
                                                      methodID,args);
}

static PyObject* jdouble CallNonvirtualDoubleMethodA(jobject obj, jclass clazz,
                                        jmethodID methodID,
                                        const jvalue * args)
{
    j??? ret = jenv->CallNonvirtualDoubleMethodA(&jenv,obj,clazz,
                                                      methodID,args);
}


static PyObject* CallNonvirtualVoidMethod(jobject obj, jclass clazz,
                                  jmethodID methodID, ...)
{
        va_list args;
        va_start(args,methodID);
    jenv->CallNonvirtualVoidMethodV(&jenv,obj,clazz,methodID,args);
        va_end(args);
}

static PyObject* CallNonvirtualVoidMethodV(jobject obj, jclass clazz,
                                   jmethodID methodID,
                                   va_list args)
{
    jenv->CallNonvirtualVoidMethodV(&jenv,obj,clazz,methodID,args);
}

static PyObject* CallNonvirtualVoidMethodA(jobject obj, jclass clazz,
                                   jmethodID methodID,
                                   const jvalue * args)
{
    jenv->CallNonvirtualVoidMethodA(&jenv,obj,clazz,methodID,args);
}


static PyObject* jfieldID GetFieldID(jclass clazz, const char *name,
                        const char *sig)
{
    j??? ret = jenv->GetFieldID(&jenv,clazz,name,sig);
}


static PyObject* jobject GetObjectField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetObjectField(&jenv,obj,fieldID);
}

static PyObject* jboolean GetBooleanField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetBooleanField(&jenv,obj,fieldID);
}

static PyObject* jbyte GetByteField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetByteField(&jenv,obj,fieldID);
}

static PyObject* jchar GetCharField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetCharField(&jenv,obj,fieldID);
}

static PyObject* jshort GetShortField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetShortField(&jenv,obj,fieldID);
}

static PyObject* jint GetIntField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetIntField(&jenv,obj,fieldID);
}

static PyObject* jlong GetLongField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetLongField(&jenv,obj,fieldID);
}

static PyObject* jfloat GetFloatField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetFloatField(&jenv,obj,fieldID);
}

static PyObject* jdouble GetDoubleField(jobject obj, jfieldID fieldID)
{
    j??? ret = jenv->GetDoubleField(&jenv,obj,fieldID);
}


static PyObject* SetObjectField(jobject obj, jfieldID fieldID, jobject val)
{
    jenv->SetObjectField(&jenv,obj,fieldID,val);
}

static PyObject* SetBooleanField(jobject obj, jfieldID fieldID,
                         jboolean val)
{
    jenv->SetBooleanField(&jenv,obj,fieldID,val);
}

static PyObject* SetByteField(jobject obj, jfieldID fieldID,
                      jbyte val)
{
    jenv->SetByteField(&jenv,obj,fieldID,val);
}

static PyObject* SetCharField(jobject obj, jfieldID fieldID,
                      jchar val)
{
    jenv->SetCharField(&jenv,obj,fieldID,val);
}

static PyObject* SetShortField(jobject obj, jfieldID fieldID,
                       jshort val)
{
    jenv->SetShortField(&jenv,obj,fieldID,val);
}

static PyObject* SetIntField(jobject obj, jfieldID fieldID,
                     jint val)
{
    jenv->SetIntField(&jenv,obj,fieldID,val);
}

static PyObject* SetLongField(jobject obj, jfieldID fieldID,
                      jlong val)
{
    jenv->SetLongField(&jenv,obj,fieldID,val);
}

static PyObject* SetFloatField(jobject obj, jfieldID fieldID,
                       jfloat val)
{
    jenv->SetFloatField(&jenv,obj,fieldID,val);
}

static PyObject* SetDoubleField(jobject obj, jfieldID fieldID,
                        jdouble val)
{
    jenv->SetDoubleField(&jenv,obj,fieldID,val);
}


static PyObject* jmethodID GetStaticMethodID(jclass clazz, const char *name,
                                const char *sig)
{
    j??? ret = jenv->GetStaticMethodID(&jenv,clazz,name,sig);
}


static PyObject* jobject CallStaticObjectMethod(jclass clazz, jmethodID methodID,
                             ...)
{
        va_list args;
        jobject result;
        va_start(args,methodID);
        result = functions->CallStaticObjectMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jobject CallStaticObjectMethodV(jclass clazz, jmethodID methodID,
                              va_list args)
{
    j??? ret = jenv->CallStaticObjectMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jobject CallStaticObjectMethodA(jclass clazz, jmethodID methodID,
                              const jvalue *args)
{
    j??? ret = jenv->CallStaticObjectMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jboolean CallStaticBooleanMethod(jclass clazz,
                                     jmethodID methodID, ...)
{
        va_list args;
        jboolean result;
        va_start(args,methodID);
        result = functions->CallStaticBooleanMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jboolean CallStaticBooleanMethodV(jclass clazz,
                                      jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticBooleanMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jboolean CallStaticBooleanMethodA(jclass clazz,
                                      jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticBooleanMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jbyte CallStaticByteMethod(jclass clazz,
                               jmethodID methodID, ...)
{
        va_list args;
        jbyte result;
        va_start(args,methodID);
        result = functions->CallStaticByteMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jbyte CallStaticByteMethodV(jclass clazz,
                                jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticByteMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jbyte CallStaticByteMethodA(jclass clazz,
                                jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticByteMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jchar CallStaticCharMethod(jclass clazz,
                               jmethodID methodID, ...)
{
        va_list args;
        jchar result;
        va_start(args,methodID);
        result = functions->CallStaticCharMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jchar CallStaticCharMethodV(jclass clazz,
                                jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticCharMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jchar CallStaticCharMethodA(jclass clazz,
                                jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticCharMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jshort CallStaticShortMethod(jclass clazz,
                                 jmethodID methodID, ...)
{
        va_list args;
        jshort result;
        va_start(args,methodID);
        result = functions->CallStaticShortMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jshort CallStaticShortMethodV(jclass clazz,
                                  jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticShortMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jshort CallStaticShortMethodA(jclass clazz,
                                  jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticShortMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jint CallStaticIntMethod(jclass clazz,
                             jmethodID methodID, ...)
{
        va_list args;
        jint result;
        va_start(args,methodID);
        result = functions->CallStaticIntMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jint CallStaticIntMethodV(jclass clazz,
                              jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticIntMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jint CallStaticIntMethodA(jclass clazz,
                              jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticIntMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jlong CallStaticLongMethod(jclass clazz,
                               jmethodID methodID, ...)
{
        va_list args;
        jlong result;
        va_start(args,methodID);
        result = functions->CallStaticLongMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jlong CallStaticLongMethodV(jclass clazz,
                                jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticLongMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jlong CallStaticLongMethodA(jclass clazz,
                                jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticLongMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jfloat CallStaticFloatMethod(jclass clazz,
                                 jmethodID methodID, ...)
{
        va_list args;
        jfloat result;
        va_start(args,methodID);
        result = functions->CallStaticFloatMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jfloat CallStaticFloatMethodV(jclass clazz,
                                  jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticFloatMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jfloat CallStaticFloatMethodA(jclass clazz,
                                  jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticFloatMethodA(&jenv,clazz,methodID,args);
}


static PyObject* jdouble CallStaticDoubleMethod(jclass clazz,
                                   jmethodID methodID, ...)
{
        va_list args;
        jdouble result;
        va_start(args,methodID);
        result = functions->CallStaticDoubleMethodV(&jenv,clazz,methodID,args);
        va_end(args);
        return result;
}

static PyObject* jdouble CallStaticDoubleMethodV(jclass clazz,
                                    jmethodID methodID, va_list args)
{
    j??? ret = jenv->CallStaticDoubleMethodV(&jenv,clazz,methodID,args);
}

static PyObject* jdouble CallStaticDoubleMethodA(jclass clazz,
                                    jmethodID methodID, const jvalue *args)
{
    j??? ret = jenv->CallStaticDoubleMethodA(&jenv,clazz,methodID,args);
}


static PyObject* CallStaticVoidMethod(jclass cls, jmethodID methodID, ...)
{
        va_list args;
        va_start(args,methodID);
    jenv->CallStaticVoidMethodV(&jenv,cls,methodID,args);
        va_end(args);
}

static PyObject* CallStaticVoidMethodV(jclass cls, jmethodID methodID,
                               va_list args)
{
    jenv->CallStaticVoidMethodV(&jenv,cls,methodID,args);
}

static PyObject* CallStaticVoidMethodA(jclass cls, jmethodID methodID,
                               const jvalue * args)
{
    jenv->CallStaticVoidMethodA(&jenv,cls,methodID,args);
}


static PyObject* jfieldID GetStaticFieldID(jclass clazz, const char *name,
                              const char *sig)
{
    j??? ret = jenv->GetStaticFieldID(&jenv,clazz,name,sig);
}

static PyObject* jobject GetStaticObjectField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticObjectField(&jenv,clazz,fieldID);
}

static PyObject* jboolean GetStaticBooleanField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticBooleanField(&jenv,clazz,fieldID);
}

static PyObject* jbyte GetStaticByteField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticByteField(&jenv,clazz,fieldID);
}

static PyObject* jchar GetStaticCharField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticCharField(&jenv,clazz,fieldID);
}

static PyObject* jshort GetStaticShortField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticShortField(&jenv,clazz,fieldID);
}

static PyObject* jint GetStaticIntField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticIntField(&jenv,clazz,fieldID);
}

static PyObject* jlong GetStaticLongField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticLongField(&jenv,clazz,fieldID);
}

static PyObject* jfloat GetStaticFloatField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticFloatField(&jenv,clazz,fieldID);
}

static PyObject* jdouble GetStaticDoubleField(jclass clazz, jfieldID fieldID)
{
    j??? ret = jenv->GetStaticDoubleField(&jenv,clazz,fieldID);
}


static PyObject* SetStaticObjectField(jclass clazz, jfieldID fieldID,
                        jobject value)
{
      functions->SetStaticObjectField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticBooleanField(jclass clazz, jfieldID fieldID,
                        jboolean value)
{
      functions->SetStaticBooleanField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticByteField(jclass clazz, jfieldID fieldID,
                        jbyte value)
{
      functions->SetStaticByteField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticCharField(jclass clazz, jfieldID fieldID,
                        jchar value)
{
      functions->SetStaticCharField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticShortField(jclass clazz, jfieldID fieldID,
                        jshort value)
{
      functions->SetStaticShortField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticIntField(jclass clazz, jfieldID fieldID,
                        jint value)
{
      functions->SetStaticIntField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticLongField(jclass clazz, jfieldID fieldID,
                        jlong value)
{
      functions->SetStaticLongField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticFloatField(jclass clazz, jfieldID fieldID,
                        jfloat value)
{
      functions->SetStaticFloatField(&jenv,clazz,fieldID,value);
}

static PyObject* SetStaticDoubleField(jclass clazz, jfieldID fieldID,
                        jdouble value)
{
      functions->SetStaticDoubleField(&jenv,clazz,fieldID,value);
}


static PyObject* jstring NewString(const jchar *unicode, jsize len)
{
    j??? ret = jenv->NewString(&jenv,unicode,len);
}

static PyObject* jsize GetStringLength(jstring str)
{
    j??? ret = jenv->GetStringLength(&jenv,str);
}

    const jchar *GetStringChars(jstring str, jboolean *isCopy)
{
    j??? ret = jenv->GetStringChars(&jenv,str,isCopy);
}

static PyObject* ReleaseStringChars(jstring str, const jchar *chars)
{
    jenv->ReleaseStringChars(&jenv,str,chars);
}


static PyObject* jstring NewStringUTF(const char *utf)
{
    j??? ret = jenv->NewStringUTF(&jenv,utf);
}

static PyObject* jsize GetStringUTFLength(jstring str)
{
    j??? ret = jenv->GetStringUTFLength(&jenv,str);
}

static PyObject* jlong GetStringUTFLengthAsLong(jstring str)
{
    j??? ret = jenv->GetStringUTFLengthAsLong(&jenv,str);
}

    const char* GetStringUTFChars(jstring str, jboolean *isCopy)
{
    j??? ret = jenv->GetStringUTFChars(&jenv,str,isCopy);
}

static PyObject* ReleaseStringUTFChars(jstring str, const char* chars)
{
    jenv->ReleaseStringUTFChars(&jenv,str,chars);
}


static PyObject* jsize GetArrayLength(jarray array)
{
    j??? ret = jenv->GetArrayLength(&jenv,array);
}


static PyObject* jobjectArray NewObjectArray(jsize len, jclass clazz,
                                jobject init)
{
    j??? ret = jenv->NewObjectArray(&jenv,len,clazz,init);
}

static PyObject* jobject GetObjectArrayElement(jobjectArray array, jsize index)
{
    j??? ret = jenv->GetObjectArrayElement(&jenv,array,index);
}

static PyObject* SetObjectArrayElement(jobjectArray array, jsize index,
                               jobject val)
{
    jenv->SetObjectArrayElement(&jenv,array,index,val);
}


static PyObject* jbooleanArray NewBooleanArray(jsize len)
{
    j??? ret = jenv->NewBooleanArray(&jenv,len);
}

static PyObject* jbyteArray NewByteArray(jsize len)
{
    j??? ret = jenv->NewByteArray(&jenv,len);
}

static PyObject* jcharArray NewCharArray(jsize len)
{
    j??? ret = jenv->NewCharArray(&jenv,len);
}

static PyObject* jshortArray NewShortArray(jsize len)
{
    j??? ret = jenv->NewShortArray(&jenv,len);
}

static PyObject* jintArray NewIntArray(jsize len)
{
    j??? ret = jenv->NewIntArray(&jenv,len);
}

static PyObject* jlongArray NewLongArray(jsize len)
{
    j??? ret = jenv->NewLongArray(&jenv,len);
}

static PyObject* jfloatArray NewFloatArray(jsize len)
{
    j??? ret = jenv->NewFloatArray(&jenv,len);
}

static PyObject* jdoubleArray NewDoubleArray(jsize len)
{
    j??? ret = jenv->NewDoubleArray(&jenv,len);
}


static PyObject* jboolean * GetBooleanArrayElements(jbooleanArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetBooleanArrayElements(&jenv,array,isCopy);
}

static PyObject* jbyte * GetByteArrayElements(jbyteArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetByteArrayElements(&jenv,array,isCopy);
}

static PyObject* jchar * GetCharArrayElements(jcharArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetCharArrayElements(&jenv,array,isCopy);
}

static PyObject* jshort * GetShortArrayElements(jshortArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetShortArrayElements(&jenv,array,isCopy);
}

static PyObject* jint * GetIntArrayElements(jintArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetIntArrayElements(&jenv,array,isCopy);
}

static PyObject* jlong * GetLongArrayElements(jlongArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetLongArrayElements(&jenv,array,isCopy);
}

static PyObject* jfloat * GetFloatArrayElements(jfloatArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetFloatArrayElements(&jenv,array,isCopy);
}

static PyObject* jdouble * GetDoubleArrayElements(jdoubleArray array, jboolean *isCopy)
{
    j??? ret = jenv->GetDoubleArrayElements(&jenv,array,isCopy);
}


static PyObject* ReleaseBooleanArrayElements(jbooleanArray array,
                                     jboolean *elems,
                                     jint mode)
{
    jenv->ReleaseBooleanArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseByteArrayElements(jbyteArray array,
                                  jbyte *elems,
                                  jint mode)
{
    jenv->ReleaseByteArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseCharArrayElements(jcharArray array,
                                  jchar *elems,
                                  jint mode)
{
    jenv->ReleaseCharArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseShortArrayElements(jshortArray array,
                                   jshort *elems,
                                   jint mode)
{
    jenv->ReleaseShortArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseIntArrayElements(jintArray array,
                                 jint *elems,
                                 jint mode)
{
    jenv->ReleaseIntArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseLongArrayElements(jlongArray array,
                                  jlong *elems,
                                  jint mode)
{
    jenv->ReleaseLongArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseFloatArrayElements(jfloatArray array,
                                   jfloat *elems,
                                   jint mode)
{
    jenv->ReleaseFloatArrayElements(&jenv,array,elems,mode);
}

static PyObject* ReleaseDoubleArrayElements(jdoubleArray array,
                                    jdouble *elems,
                                    jint mode)
{
    jenv->ReleaseDoubleArrayElements(&jenv,array,elems,mode);
}


static PyObject* GetBooleanArrayRegion(jbooleanArray array,
                               jsize start, jsize len, jboolean *buf)
{
    jenv->GetBooleanArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetByteArrayRegion(jbyteArray array,
                            jsize start, jsize len, jbyte *buf)
{
    jenv->GetByteArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetCharArrayRegion(jcharArray array,
                            jsize start, jsize len, jchar *buf)
{
    jenv->GetCharArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetShortArrayRegion(jshortArray array,
                             jsize start, jsize len, jshort *buf)
{
    jenv->GetShortArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetIntArrayRegion(jintArray array,
                           jsize start, jsize len, jint *buf)
{
    jenv->GetIntArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetLongArrayRegion(jlongArray array,
                            jsize start, jsize len, jlong *buf)
{
    jenv->GetLongArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetFloatArrayRegion(jfloatArray array,
                             jsize start, jsize len, jfloat *buf)
{
    jenv->GetFloatArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* GetDoubleArrayRegion(jdoubleArray array,
                              jsize start, jsize len, jdouble *buf)
{
    jenv->GetDoubleArrayRegion(&jenv,array,start,len,buf);
}


static PyObject* SetBooleanArrayRegion(jbooleanArray array, jsize start, jsize len,
                               const jboolean *buf)
{
    jenv->SetBooleanArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetByteArrayRegion(jbyteArray array, jsize start, jsize len,
                            const jbyte *buf)
{
    jenv->SetByteArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetCharArrayRegion(jcharArray array, jsize start, jsize len,
                            const jchar *buf)
{
    jenv->SetCharArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetShortArrayRegion(jshortArray array, jsize start, jsize len,
                             const jshort *buf)
{
    jenv->SetShortArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetIntArrayRegion(jintArray array, jsize start, jsize len,
                           const jint *buf)
{
    jenv->SetIntArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetLongArrayRegion(jlongArray array, jsize start, jsize len,
                            const jlong *buf)
{
    jenv->SetLongArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetFloatArrayRegion(jfloatArray array, jsize start, jsize len,
                             const jfloat *buf)
{
    jenv->SetFloatArrayRegion(&jenv,array,start,len,buf);
}

static PyObject* SetDoubleArrayRegion(jdoubleArray array, jsize start, jsize len,
                              const jdouble *buf)
{
    jenv->SetDoubleArrayRegion(&jenv,array,start,len,buf);
}


static PyObject* jint RegisterNatives(jclass clazz, const JNINativeMethod *methods,
                         jint nMethods)
{
    j??? ret = jenv->RegisterNatives(&jenv,clazz,methods,nMethods);
}

static PyObject* jint UnregisterNatives(jclass clazz)
{
    j??? ret = jenv->UnregisterNatives(&jenv,clazz);
}


static PyObject* jint MonitorEnter(jobject obj)
{
    j??? ret = jenv->MonitorEnter(&jenv,obj);
}

static PyObject* jint MonitorExit(jobject obj)
{
    j??? ret = jenv->MonitorExit(&jenv,obj);
}


static PyObject* jint GetJavaVM(JavaVM **vm)
{
    j??? ret = jenv->GetJavaVM(&jenv,vm);
}


static PyObject* GetStringRegion(jstring str, jsize start, jsize len, jchar *buf)
{
    jenv->GetStringRegion(&jenv,str,start,len,buf);
}

static PyObject* GetStringUTFRegion(jstring str, jsize start, jsize len, char *buf)
{
    jenv->GetStringUTFRegion(&jenv,str,start,len,buf);
}


static PyObject* * GetPrimitiveArrayCritical(jarray array, jboolean *isCopy)
{
    j??? ret = jenv->GetPrimitiveArrayCritical(&jenv,array,isCopy);
}

static PyObject* ReleasePrimitiveArrayCritical(jarray array, void *carray, jint mode)
{
    jenv->ReleasePrimitiveArrayCritical(&jenv,array,carray,mode);
}


    const jchar * GetStringCritical(jstring string, jboolean *isCopy)
{
    j??? ret = jenv->GetStringCritical(&jenv,string,isCopy);
}

static PyObject* ReleaseStringCritical(jstring string, const jchar *cstring)
{
    jenv->ReleaseStringCritical(&jenv,string,cstring);
}


static PyObject* jweak NewWeakGlobalRef(jobject obj)
{
    j??? ret = jenv->NewWeakGlobalRef(&jenv,obj);
}

static PyObject* DeleteWeakGlobalRef(jweak ref)
{
    jenv->DeleteWeakGlobalRef(&jenv,ref);
}


static PyObject* jboolean ExceptionCheck()
{
    j??? ret = jenv->ExceptionCheck(&jenv);
}


static PyObject* jobject NewDirectByteBuffer(void* address, jlong capacity)
{
    j??? ret = jenv->NewDirectByteBuffer(&jenv, address, capacity);
}

    void* GetDirectBufferAddress(jobject buf)
{
    j??? ret = jenv->GetDirectBufferAddress(&jenv, buf);
}

static PyObject* jlong GetDirectBufferCapacity(jobject buf)
{
    j??? ret = jenv->GetDirectBufferCapacity(&jenv, buf);
}

static PyObject* jobjectRefType GetObjectRefType(jobject obj)
{
    j??? ret = jenv->GetObjectRefType(&jenv, obj);
}


    // Module Features

static PyObject* jobject GetModule(jclass clazz)
{
    j??? ret = jenv->GetModule(&jenv, clazz);
}


    // Virtual threads

static PyObject* jboolean IsVirtualThread(jobject obj)
{
    j??? ret = jenv->IsVirtualThread(&jenv, obj);
}


*/

// JNIEnv* env; 
// return env->functions->CallObjectMethodA(env, obj, mid, val); 
//
// jstring v = (*jenv)->CallObjectMethodA(jenv, objectRef, method->mid, jArgs);

//PyObject* JMethod_is_param_mutable(JPy_JMethod* self, PyObject* args)
//{
//    int index;
//    int value;
//    if (!PyArg_ParseTuple(args, "i:is_param_mutable", &index)) {
//        return NULL;
//    }
//    JMethod_CHECK_PARAMETER_INDEX(self, index);
//    value = self->paramDescriptors[index].isMutable;
//    return PyBool_FromLong(value);
//}

static PyMethodDef JNIEnv_methods[] = {
    {"GetVersion",    (PyCFunction)GetVersion, METH_NOARGS, NULL},
//    {"get_param_type",    (PyCFunction)JNIEnv_get_param_type,    METH_VARARGS, "Gets the type of the parameter given by index"},
    {NULL}
};

PyTypeObject JNIEnv_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.JNIEnv",
    .tp_basicsize = sizeof(JNIEnv_Object),
    .tp_itemsize  = member_size(JNIEnv_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_methods   = JNIEnv_methods,
};

//-------------- JavaVM --------------//

typedef struct {
    PyObject_HEAD
    JavaVM this; // JavaVM* jvm; ???
} JavaVM_Object;

/*
def AttachCurrentThread(self, penv, args=None):
    fun = self.functions[0]
    ret = fun.AttachCurrentThread(self, penv, args)
    if ret != JNI_OK: self._handle_JNIException(ret)

def AttachCurrentThreadAsDaemon(self, penv, args=None):
    fun = self.functions[0]
    ret = fun.AttachCurrentThreadAsDaemon(self, penv, args)
    if ret != JNI_OK: self._handle_JNIException(ret)

def GetEnv(self, penv, version):
    fun = self.functions[0]
    ret = fun.GetEnv(self, penv, version)
    if ret != JNI_OK: self._handle_JNIException(ret)

	JavaVM* s_JavaVM = NULL;
	JNIEnv* env;
	jint res = s_JavaVM->functions->AttachCurrentThread(s_JavaVM, (void**) &env, NULL);
	if (res != JNI_OK)
		JP_RAISE_RUNTIME_ERROR("Unable to attach to thread");

*/

static PyObject* DestroyJavaVM(JavaVM_Object* self)
{
    // jint (JNICALL *DestroyJavaVM)(JavaVM *vm);
    JavaVM* jvm = &self->this;
    jint ret = (*jvm)->DestroyJavaVM(jvm);
    if ( ret != JNI_OK ) return _handle_JNIException(ret);
    Py_RETURN_NONE;
}

static PyObject* AttachCurrentThread(JavaVM_Object* self, PyObject* args)
{
    // jint (JNICALL *AttachCurrentThread)(JavaVM *vm, void **penv, void *args);
    PyObject* penv;
    if ( ! PyArg_ParseTuple(args, "O", &penv) )
        return NULL;
    JavaVM* jvm = &self->this;
    JNIEnv* jenv;
    jint ret = (*jvm)->AttachCurrentThread(jvm, (void**)&jenv, NULL);
    if ( ret != JNI_OK ) return _handle_JNIException(ret);
    Py_RETURN_NONE;
}

static PyObject* AttachCurrentThreadAsDaemon(JavaVM_Object* self, PyObject* args)
{
    //jint (JNICALL *AttachCurrentThreadAsDaemon)(JavaVM *vm, void **penv, void *args);
    PyObject* penv;
    if ( ! PyArg_ParseTuple(args, "O", &penv) )
        return NULL;
    JavaVM* jvm = &self->this;
    JNIEnv* jenv;
    jint ret = (*jvm)->AttachCurrentThreadAsDaemon(jvm, (void**)&jenv, NULL);
    if ( ret != JNI_OK ) return _handle_JNIException(ret);
    Py_RETURN_NONE;
}

static PyObject* DetachCurrentThread(JavaVM_Object* self)
{
    // jint (JNICALL *DetachCurrentThread)(JavaVM *vm);
    JavaVM* jvm = &self->this;
    jint ret = (*jvm)->DetachCurrentThread(jvm);
    if ( ret != JNI_OK ) return _handle_JNIException(ret);
    Py_RETURN_NONE;
}

static PyObject* GetEnv(JavaVM_Object* self, PyObject* args)
{
    // jint (JNICALL *GetEnv)(JavaVM *vm, void **penv, jint version);
    PyObject* penv;
    long version;
    if ( ! PyArg_ParseTuple(args, "Ol", &penv, &version) )
        return NULL;
  //JNIEnv* jenv = ((JNIEnv*)penv)->this;
    JavaVM* jvm = &self->this;
    JNIEnv* jenv;
    jint ret = (*jvm)->GetEnv(jvm, (void **)&jenv, (jint)version);
    return PyLong_FromLong((long)ret);
}

static PyMethodDef JavaVM_methods[] = {
    {"DestroyJavaVM",               (PyCFunction)DestroyJavaVM,               METH_NOARGS},
    {"AttachCurrentThread",         (PyCFunction)AttachCurrentThread,         METH_VARARGS},
    {"AttachCurrentThreadAsDaemon", (PyCFunction)AttachCurrentThreadAsDaemon, METH_VARARGS},
    {"DetachCurrentThread",         (PyCFunction)DetachCurrentThread,         METH_NOARGS},
    {"GetEnv",                      (PyCFunction)GetEnv,                      METH_VARARGS},
    {NULL}
};

PyTypeObject JavaVM_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "jni.capi.JavaVM",
    .tp_basicsize = sizeof(JavaVM_Object),
    .tp_itemsize  = member_size(JavaVM_Object, this),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_methods   = JavaVM_methods,
};

//------------------------------------//

static PyObject* POINTER(PyObject* self, PyObject* cls)
{
    PyObject* result = NULL;
    PyTypeObject* type;
    char* name;

    // if ( ! PyType_Check(cls) )
    if ( PyObject_IsInstance(cls, (PyObject*)&PyType_Type) <= 0 ||
         PyType_IsSubtype((PyTypeObject*)cls, (PyTypeObject*)&_CData_Type) <= 0 )
    {
        PyErr_SetString(PyExc_TypeError, "must be a jni type");
        return NULL;
    }

    type = (PyTypeObject*)cls;
    name = PyMem_Malloc(strlen(type->tp_name) + 3 + 1);
    if ( name == NULL )
        return PyErr_NoMemory();
    sprintf(name, "LP_%s", type->tp_name);
/* !!!
    result = PyObject_CallFunction((PyObject*)Py_TYPE(&PyCPointer_Type),
                                   "s(O){sO}", name, &PyCPointer_Type, "_type_", cls);
    PyMem_Free(name);
!!! */
    if ( result == NULL )
        return NULL;
    return result;
}

static PyObject* pointer(PyObject* self, PyObject* obj)
{
    PyObject* result;
    PyObject* type;
    type = POINTER(NULL, (PyObject*)Py_TYPE(obj));
    if ( type == NULL )
        return NULL;
    result = PyObject_CallFunctionObjArgs(type, obj, NULL);
    Py_DECREF(type);
    return result;
}

static PyObject* addressof(PyObject* self, PyObject* obj)
{
    if ( PyObject_IsInstance(obj, (PyObject*)&_CData_Type) <= 0 )
    {
        PyErr_SetString(PyExc_TypeError, "must be a jni type");
        return NULL;
    }

    return PyLong_FromVoidPtr((void*)&((_CData_Object*)obj)->this);
}

static PyObject* size_of(PyObject* self, PyObject* obj_or_type)
{
    if ( PyObject_IsInstance(obj_or_type, (PyObject*)&_CData_Type) > 0 )
        return PyLong_FromSsize_t((Py_ssize_t)Py_TYPE(obj_or_type)->tp_itemsize);
    else if ( PyObject_IsInstance(obj_or_type, (PyObject*)&PyType_Type) > 0 &&
              PyType_IsSubtype((PyTypeObject*)obj_or_type, (PyTypeObject*)&_CData_Type) > 0 )
        return PyLong_FromSsize_t((Py_ssize_t)((PyTypeObject*)obj_or_type)->tp_itemsize);
    else
    {
        PyErr_SetString(PyExc_TypeError, "this type has no size");
        return NULL;
    }
}

static PyMethodDef module_functions[] = {
    {"POINTER",   (PyCFunction)POINTER,   METH_O},
    {"pointer",   (PyCFunction)pointer,   METH_O},
    {"addressof", (PyCFunction)addressof, METH_O},
    {"sizeof",    (PyCFunction)size_of,   METH_O},
    {NULL}
};

static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    __name__,          /* m_name     */
    NULL,              /* m_doc      */
    -1,                /* m_size     */
    module_functions,  /* m_methods  */
    NULL,              /* m_reload   */
    NULL,              /* m_traverse */
    NULL,              /* m_clear    */
    NULL,              /* m_free     */
};

//------------------------------------//

static int traverse_GC(PyObject* self, visitproc visit, void* arg)
{
    return 0;
}

static int clear_GC(PyObject* self)
{
    return 0;
}

static void dealloc_GC(PyObject* self)
{
    PyObject_GC_UnTrack(self);
    PyObject_GC_Del(self);
}

//------------------------------------//

#define MODINIT_FUNC(name) PyInit_##name(void)

PyMODINIT_FUNC MODINIT_FUNC(jni)
{
    static PyObject* module = NULL;

    module = PyModule_Create(&module_def);
    if ( module == NULL )
        return NULL;

    /* JNI Types */

    if ( PyType_Ready(&jboolean_Type) < 0 ||
         PyType_Ready(&jchar_Type) < 0 ||
         PyType_Ready(&jbyte_Type) < 0 ||
         PyType_Ready(&jshort_Type) < 0 ||
         PyType_Ready(&jint_Type)  < 0 ||
         PyType_Ready(&jlong_Type) < 0 ||
         PyType_Ready(&jfloat_Type) < 0 ||
         PyType_Ready(&jdouble_Type) < 0 ||
         // PyType_Ready(&jsize_Type)  < 0 ||
         PyType_Ready(&jobject_Type) < 0 ||
         PyType_Ready(&jclass_Type) < 0 ||
         PyType_Ready(&jthrowable_Type) < 0 ||
         PyType_Ready(&jstring_Type) < 0 ||
         PyType_Ready(&jarray_Type) < 0 ||
         PyType_Ready(&jbooleanArray_Type) < 0 ||
         PyType_Ready(&jcharArray_Type) < 0 ||
         PyType_Ready(&jbyteArray_Type) < 0 ||
         PyType_Ready(&jshortArray_Type) < 0 ||
         PyType_Ready(&jintArray_Type) < 0 ||
         PyType_Ready(&jlongArray_Type) < 0 ||
         PyType_Ready(&jfloatArray_Type) < 0 ||
         PyType_Ready(&jdoubleArray_Type) < 0 ||
         PyType_Ready(&jobjectArray_Type) < 0 ||
         // PyType_Ready(&jweak_Type) < 0 ||
         PyType_Ready(&jvalue_Type) < 0 ||
         PyType_Ready(&jfieldID_Type) < 0 ||
         PyType_Ready(&jmethodID_Type) < 0 ||
         PyType_Ready(&JNINativeMethod_Type) < 0 ||
         PyType_Ready(&JNIEnv_Type) < 0 ||
         PyType_Ready(&JavaVMOption_Type) < 0 ||
         PyType_Ready(&JavaVMInitArgs_Type) < 0 ||
         PyType_Ready(&JavaVMAttachArgs_Type) < 0 ||
         PyType_Ready(&JavaVM_Type) < 0 )
        return NULL;

    Py_INCREF(&jboolean_Type);
    PyModule_AddObject(module, "jboolean", (PyObject*)&jboolean_Type);
    Py_INCREF(&jchar_Type);
    PyModule_AddObject(module, "jchar",    (PyObject*)&jchar_Type);
    Py_INCREF(&jbyte_Type);
    PyModule_AddObject(module, "jbyte", (PyObject*)&jbyte_Type);
    Py_INCREF(&jshort_Type);
    PyModule_AddObject(module, "jshort",   (PyObject*)&jshort_Type);
    Py_INCREF(&jint_Type);
    PyModule_AddObject(module, "jint",  (PyObject*)&jint_Type);
    Py_INCREF(&jlong_Type);
    PyModule_AddObject(module, "jlong", (PyObject*)&jlong_Type);
    Py_INCREF(&jfloat_Type);
    PyModule_AddObject(module, "jfloat",   (PyObject*)&jfloat_Type);
    Py_INCREF(&jdouble_Type);
    PyModule_AddObject(module, "jdouble",  (PyObject*)&jdouble_Type);
    Py_INCREF(&jsize_Type);
    PyModule_AddObject(module, "jsize",    (PyObject*)&jsize_Type);
    Py_INCREF(&jobject_Type);
    PyModule_AddObject(module, "jobject",       (PyObject*)&jobject_Type);
    Py_INCREF(&jclass_Type);
    PyModule_AddObject(module, "jclass",        (PyObject*)&jclass_Type);
    Py_INCREF(&jthrowable_Type);
    PyModule_AddObject(module, "jthrowable",    (PyObject*)&jthrowable_Type);
    Py_INCREF(&jstring_Type);
    PyModule_AddObject(module, "jstring",       (PyObject*)&jstring_Type);
    Py_INCREF(&jarray_Type);
    PyModule_AddObject(module, "jarray",        (PyObject*)&jarray_Type);
    Py_INCREF(&jbooleanArray_Type);
    PyModule_AddObject(module, "jbooleanArray", (PyObject*)&jbooleanArray_Type);
    Py_INCREF(&jcharArray_Type);
    PyModule_AddObject(module, "jcharArray",    (PyObject*)&jcharArray_Type);
    Py_INCREF(&jbyteArray_Type);
    PyModule_AddObject(module, "jbyteArray",    (PyObject*)&jbyteArray_Type);
    Py_INCREF(&jshortArray_Type);
    PyModule_AddObject(module, "jshortArray",   (PyObject*)&jshortArray_Type);
    Py_INCREF(&jintArray_Type);
    PyModule_AddObject(module, "jintArray",     (PyObject*)&jintArray_Type);
    Py_INCREF(&jlongArray_Type);
    PyModule_AddObject(module, "jlongArray",    (PyObject*)&jlongArray_Type);
    Py_INCREF(&jfloatArray_Type);
    PyModule_AddObject(module, "jfloatArray",   (PyObject*)&jfloatArray_Type);
    Py_INCREF(&jdoubleArray_Type);
    PyModule_AddObject(module, "jdoubleArray",  (PyObject*)&jdoubleArray_Type);
    Py_INCREF(&jobjectArray_Type);
    PyModule_AddObject(module, "jobjectArray",  (PyObject*)&jobjectArray_Type);

    Py_INCREF(&jweak_Type);
    PyModule_AddObject(module, "jweak", (PyObject*)&jweak_Type);

    Py_INCREF(&jvalue_Type);
    PyModule_AddObject(module, "jvalue", (PyObject*)&jvalue_Type);

    Py_INCREF(&jfieldID_Type);
    PyModule_AddObject(module, "jfieldID",  (PyObject*)&jfieldID_Type);

    Py_INCREF(&jmethodID_Type);
    PyModule_AddObject(module, "jmethodID", (PyObject*)&jmethodID_Type);

    /* Return values from jobjectRefType */
    Py_INCREF(&jobjectRefType_Type);
    PyModule_AddObject(module, "jobjectRefType", (PyObject*)&jobjectRefType_Type);
    PyModule_AddIntConstant(module, "JNIInvalidRefType",    JNIInvalidRefType);
    PyModule_AddIntConstant(module, "JNILocalRefType",      JNILocalRefType);
    PyModule_AddIntConstant(module, "JNIGlobalRefType",     JNIGlobalRefType);
    PyModule_AddIntConstant(module, "JNIWeakGlobalRefType", JNIWeakGlobalRefType);

    /* jboolean constants */
    PyModule_AddIntConstant(module, "JNI_FALSE", JNI_FALSE);
    PyModule_AddIntConstant(module, "JNI_TRUE",  JNI_TRUE);

    /* null constant */
    PyModule_AddObject(module, "NULL",
                       (PyObject*)PyObject_New(jobject_Object, &jobject_Type));

    /* possible return values for JNI functions. */
    PyModule_AddIntConstant(module, "JNI_OK",        JNI_OK);
    PyModule_AddIntConstant(module, "JNI_ERR",       JNI_ERR);
    PyModule_AddIntConstant(module, "JNI_EDETACHED", JNI_EDETACHED);
    PyModule_AddIntConstant(module, "JNI_EVERSION",  JNI_EVERSION);
    PyModule_AddIntConstant(module, "JNI_ENOMEM",    JNI_ENOMEM);
    PyModule_AddIntConstant(module, "JNI_EEXIST",    JNI_EEXIST);
    PyModule_AddIntConstant(module, "JNI_EINVAL",    JNI_EINVAL);

    /* used in ReleaseScalarArrayElements */
    PyModule_AddIntConstant(module, "JNI_COMMIT", JNI_COMMIT);
    PyModule_AddIntConstant(module, "JNI_ABORT",  JNI_ABORT);

    /* JNI Native Method Interface. */

    /* used in RegisterNatives to describe native method name,
       signature, and function pointer. */
    Py_INCREF(&JNINativeMethod_Type);
    PyModule_AddObject(module, "JNINativeMethod", (PyObject*)&JNINativeMethod_Type);

    /* JNI Invocation Interface. */

    Py_INCREF(&JavaVMOption_Type);
    PyModule_AddObject(module, "JavaVMOption", (PyObject*)&JavaVMOption_Type);

    Py_INCREF(&JavaVMInitArgs_Type);
    PyModule_AddObject(module, "JavaVMInitArgs", (PyObject*)&JavaVMInitArgs_Type);

    Py_INCREF(&JavaVMAttachArgs_Type);
    PyModule_AddObject(module, "JavaVMAttachArgs", (PyObject*)&JavaVMAttachArgs_Type);

    Py_INCREF(&JNIEnv_Type);
    PyModule_AddObject(module, "JNIEnv", (PyObject*)&JNIEnv_Type);

    Py_INCREF(&JavaVM_Type);
    PyModule_AddObject(module, "JavaVM", (PyObject*)&JavaVM_Type);

    /* These will be VM-specific. */
    #ifdef JDK1_2
      PyModule_AddIntConstant(module, "JDK1_2", 1);
    #else
      PyModule_AddIntConstant(module, "JDK1_2", 0);
    #endif
    #ifdef JDK1_4
      PyModule_AddIntConstant(module, "JDK1_4", 1);
    #else
      PyModule_AddIntConstant(module, "JDK1_4", 0);
    #endif

    /* JNI constants. */
    PyModule_AddIntConstant(module, "JNI_VERSION_1_1", JNI_VERSION_1_1);
    PyModule_AddIntConstant(module, "JNI_VERSION_1_2", JNI_VERSION_1_2);
    PyModule_AddIntConstant(module, "JNI_VERSION_1_4", JNI_VERSION_1_4);
    PyModule_AddIntConstant(module, "JNI_VERSION_1_6", JNI_VERSION_1_6);
    PyModule_AddIntConstant(module, "JNI_VERSION_1_8", JNI_VERSION_1_8);
    PyModule_AddIntConstant(module, "JNI_VERSION_9",   JNI_VERSION_9);
    PyModule_AddIntConstant(module, "JNI_VERSION_10",  JNI_VERSION_10);
    PyModule_AddIntConstant(module, "JNI_VERSION_19",  JNI_VERSION_19);
    PyModule_AddIntConstant(module, "JNI_VERSION_20",  JNI_VERSION_20);
    PyModule_AddIntConstant(module, "JNI_VERSION_21",  JNI_VERSION_21);
    PyModule_AddIntConstant(module, "JNI_VERSION_24",  JNI_VERSION_24);

    return module;
}
