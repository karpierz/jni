// Copyright (c) 2004-2022 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

#include <Python.h>
#include <structmember.h>

#include "java/jdk/include/jni.h"

#define member_size(type, member) sizeof(((type *)0)->member)

static const char __name__[] = "jni";
static const char __doc__[]  = "";

typedef struct {
    PyObject_HEAD
    char this[0];
} _CData_Object;

PyTypeObject _CData_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "CData",
    .tp_basicsize = sizeof(_CData_Object),
    .tp_flags     = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
};

//------------ JNI Types -------------//

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
    .tp_name      = "jint",
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
    .tp_name      = "jlong",
    .tp_basicsize = sizeof(jlong_Object),
    .tp_itemsize  = member_size(jlong_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jlong_as_number,
    .tp_members   = jlong_members,
    .tp_init      = (initproc)jlong_init,
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
    .tp_name      = "jbyte",
    .tp_basicsize = sizeof(jbyte_Object),
    .tp_itemsize  = member_size(jbyte_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jbyte_as_number,
    .tp_members   = jbyte_members,
    .tp_init      = (initproc)jbyte_init,
    .tp_new       = PyType_GenericNew,
};

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
    .tp_name      = "jboolean",
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
    if ( PyUnicode_GetSize(val) != 1 )
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
    .tp_name      = "jchar",
    .tp_basicsize = sizeof(jchar_Object),
    .tp_itemsize  = member_size(jchar_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jchar_as_number,
    .tp_getset    = jchar_getsets,
    .tp_init      = (initproc)jchar_init,
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
    .tp_name      = "jshort",
    .tp_basicsize = sizeof(jshort_Object),
    .tp_itemsize  = member_size(jshort_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jshort_as_number,
    .tp_members   = jshort_members,
    .tp_init      = (initproc)jshort_init,
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
    .tp_name      = "jfloat",
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
    .tp_name      = "jdouble",
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
    .tp_name      = "jobject",
    .tp_basicsize = sizeof(jobject_Object),
    .tp_itemsize  = member_size(jobject_Object, value),
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_base      = &_CData_Type,
    .tp_as_number = &jobject_as_number,
    .tp_getset    = jobject_getsets,
    .tp_init      = (initproc)jobject_init,
    .tp_new       = PyType_GenericNew,
};

//-- jclass ... --//

#define jclass_Type        jobject_Type
#define jthrowable_Type    jobject_Type
#define jstring_Type       jobject_Type
#define jarray_Type        jobject_Type
#define jbooleanArray_Type jarray_Type
#define jbyteArray_Type    jarray_Type
#define jcharArray_Type    jarray_Type
#define jshortArray_Type   jarray_Type
#define jintArray_Type     jarray_Type
#define jlongArray_Type    jarray_Type
#define jfloatArray_Type   jarray_Type
#define jdoubleArray_Type  jarray_Type
#define jobjectArray_Type  jarray_Type
#define jweak_Type         jobject_Type

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
        if ( PyUnicode_GetSize(val) != 1 )
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
    .tp_name      = "jvalue",
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
    .tp_name      = "jfieldID",
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
    .tp_name      = "jmethodID",
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

// used in RegisterNatives to describe native method name,
// signature, and function pointer.

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
    .tp_name      = "JNINativeMethod",
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
    .tp_name      = "JavaVMOption",
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
    .tp_name      = "JavaVMInitArgs",
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
    .tp_name      = "JavaVMAttachArgs",
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
    //    cause = Throwable.last.getCause()
    //    if cause: fun.DeleteGlobalRef(self, cause)
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
    .tp_name      = "JNIEnv",
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
    .tp_name      = "JavaVM",
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

    if ( PyType_Ready(&jint_Type)  < 0 ||
         PyType_Ready(&jlong_Type) < 0 ||
         PyType_Ready(&jbyte_Type) < 0 ||
         PyType_Ready(&jboolean_Type) < 0 ||
         PyType_Ready(&jchar_Type) < 0 ||
         PyType_Ready(&jshort_Type) < 0 ||
         PyType_Ready(&jfloat_Type) < 0 ||
         PyType_Ready(&jdouble_Type) < 0 ||
         PyType_Ready(&jobject_Type) < 0 ||
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

    Py_INCREF(&jint_Type);
    PyModule_AddObject(module, "jint",  (PyObject*)&jint_Type);
    Py_INCREF(&jlong_Type);
    PyModule_AddObject(module, "jlong", (PyObject*)&jlong_Type);
    Py_INCREF(&jbyte_Type);
    PyModule_AddObject(module, "jbyte", (PyObject*)&jbyte_Type);

    Py_INCREF(&jboolean_Type);
    PyModule_AddObject(module, "jboolean", (PyObject*)&jboolean_Type);
    Py_INCREF(&jchar_Type);
    PyModule_AddObject(module, "jchar",    (PyObject*)&jchar_Type);
    Py_INCREF(&jshort_Type);
    PyModule_AddObject(module, "jshort",   (PyObject*)&jshort_Type);
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
    Py_INCREF(&jbyteArray_Type);
    PyModule_AddObject(module, "jbyteArray",    (PyObject*)&jbyteArray_Type);
    Py_INCREF(&jcharArray_Type);
    PyModule_AddObject(module, "jcharArray",    (PyObject*)&jcharArray_Type);
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
    PyModule_AddObject(module, "jweak",         (PyObject*)&jweak_Type);

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

    return module;
}
