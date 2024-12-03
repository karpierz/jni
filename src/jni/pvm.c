// Copyright (c) 2004 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

#ifndef PVM_C_INCLUDED
#define PVM_C_INCLUDED

//
// Python Virtual Machine
//

#if ( defined(_MSC_VER) && !defined(MAINWIN) )

#ifndef VC_EXTRALEAN
#define VC_EXTRALEAN
#endif
#include <windows.h>

#define DLL_LibPrefix              ""
#define DLL_LibExt                 ".dll"
#define DLL_LibHandle              HINSTANCE
#define DLL_Load(path)             ((DLL_LibHandle)LoadLibrary((const char*)(path)))
#define DLL_Close(handle)          FreeLibrary((DLL_LibHandle)(handle))
#define DLL_Error(handle)          ((const char*)"")
#define DLL_Var(name)              name
#define DLL_Fun(name, args)        (__cdecl *name)args
#define DLL_BindVar(handle, name)  ((void*)GetProcAddress((DLL_LibHandle)(handle), (const char*)(name)))
#define DLL_BindFun(handle, name)  ((void*)GetProcAddress((DLL_LibHandle)(handle), (const char*)(name)))

#elif defined(__GNUG__)

#include <dlfcn.h>

#define DLL_LibPrefix              "lib"
#define DLL_LibExt                 ".so"
#define DLL_LibHandle              void*
#define DLL_Load(path)             ((DLL_LibHandle)dlopen((const char*)(path), RTLD_NOW | RTLD_GLOBAL))
#define DLL_Close(handle)          dlclose((DLL_LibHandle)(handle))
#define DLL_Error(handle)          ((const char*)dlerror())
#define DLL_Var(name)              name
#define DLL_Fun(name, args)        (*name)args
#define DLL_BindVar(handle, name)  ((void*)dlsym((DLL_LibHandle)(handle), (const char*)(name)))
#define DLL_BindFun(handle, name)  ((void*)dlsym((DLL_LibHandle)(handle), (const char*)(name)))

#elif defined(__SUNPRO_CC)

#include <dlfcn.h>

#define DLL_LibPrefix              "lib"
#define DLL_LibExt                 ".so"
#define DLL_LibHandle              void*
#define DLL_Load(path)             ((DLL_LibHandle)dlopen((const char*)(path), RTLD_NOW | RTLD_GLOBAL))
#define DLL_Close(handle)          dlclose((DLL_LibHandle)(handle))
#define DLL_Error(handle)          ((const char*)dlerror())
#define DLL_Var(name)              name
#define DLL_Fun(name, args)        (*name)args
#define DLL_BindVar(handle, name)  ((void*)dlsym((DLL_LibHandle)(handle), (const char*)(name)))
#define DLL_BindFun(handle, name)  ((void*)dlsym((DLL_LibHandle)(handle), (const char*)(name)))

#else
#error Unsupported platform !
#endif

//---------------------------------------------------------------------------//

typedef struct PyInterpreterState PyInterpreterState;
typedef struct PyThreadState      PyThreadState;
typedef struct PyTypeObject       PyTypeObject;
typedef struct PyObject           PyObject;

typedef struct object
{
    void (*_init)(struct object* self);
    void (*_ctor)(struct object* self);
    void (*_dtor)(struct object* self);
} object;
#define object(TYPE)  {{(void (*)(object*))TYPE##_init, \
                        (void (*)(object*))TYPE##_ctor, \
                        (void (*)(object*))TYPE##_dtor}}
#define create(self)  { memset((char*)&(self) + sizeof(object),                \
                               sizeof((self)) - sizeof(object), 0);            \
                        if ( (self).super._init ) (self).super._init(&(self)); \
                        if ( (self).super._ctor ) (self).super._ctor(&(self)); }
#define destroy(self) { if ( (self).super._dtor ) (self).super._dtor(&(self)); \
                        memset((char*)&(self) + sizeof(object),                \
                               sizeof((self)) - sizeof(object), 0); }

typedef struct PVM
{
    object super;

    // private:

    DLL_LibHandle _handle;

    // public:

    int  (*load)  (struct PVM* self, const char* dll_path);
    void (*unload)(struct PVM* self);

    // Python API:

    int*           DLL_Var(Py_Version);
    int*           DLL_Var(Py_OptimizeFlag);
    int*           DLL_Var(Py_DontWriteBytecodeFlag);
    int*           DLL_Var(Py_NoSiteFlag);
    int*           DLL_Var(Py_NoUserSiteDirectory);
    void           DLL_Fun(Py_SetProgramName,(char*));
    char*          DLL_Fun(Py_GetProgramName,(void));
    void           DLL_Fun(Py_SetPythonHome,(char*));
    char*          DLL_Fun(Py_GetPythonHome,(void));
    void           DLL_Fun(Py_Initialize,(void));
    int            DLL_Fun(Py_IsInitialized,(void));
    void           DLL_Fun(Py_Finalize,(void));
    void           DLL_Fun(PySys_SetArgv,(int, char**));
    void           DLL_Fun(PySys_SetArgvEx,(int, char**, int));
    void           DLL_Fun(PySys_SetPath,(char *));
    char*          DLL_Fun(Py_GetPrefix,(void));
    char*          DLL_Fun(Py_GetExecPrefix,(void));
    char*          DLL_Fun(Py_GetPath,(void));
    void           DLL_Fun(PyEval_InitThreads,(void));
    int            DLL_Fun(PyEval_ThreadsInitialized,(void));
    PyThreadState* DLL_Fun(PyEval_SaveThread,(void)); 
    void           DLL_Fun(PyEval_RestoreThread,(PyThreadState*));
    PyThreadState* DLL_Fun(PyThreadState_Get,(void));
    PyThreadState* DLL_Fun(PyThreadState_Swap,(PyThreadState*));
    void           DLL_Fun(PyEval_AcquireThread,(PyThreadState*));
    void           DLL_Fun(PyEval_ReleaseThread,(PyThreadState*));
    void           DLL_Fun(PyEval_AcquireLock,(void));
    void           DLL_Fun(PyEval_ReleaseLock,(void));
    PyThreadState* DLL_Fun(Py_NewInterpreter,(void));
    void           DLL_Fun(Py_EndInterpreter,(PyThreadState*));
    PyObject*      DLL_Fun(PySys_GetObject,(char*));
    int            DLL_Fun(PyRun_SimpleString,(char*));
    PyObject*      DLL_Fun(PyImport_ImportModule,(const char*));
    void           DLL_Fun(Py_IncRef,(PyObject*));
    void           DLL_Fun(Py_DecRef,(PyObject*));
    PyObject*      DLL_Fun(PyErr_Occurred,(void));
    int            DLL_Fun(PyErr_GivenExceptionMatches,(PyObject*, PyObject*));
    void           DLL_Fun(PyErr_Clear,(void));
    PyObject*      DLL_Var(Py_None);
    PyObject*      DLL_Var(Py_True);
    PyObject*      DLL_Var(Py_False);

} PVM;

void PVM_ctor(PVM* self) {}
void PVM_dtor(PVM* self) {}

int PVM_load(PVM* self, const char* dll_path)
{
    // Load the Python VM DLL
    self->_handle = DLL_Load(dll_path);
    if ( self->_handle == 0 )
        //throw std::runtime_error("Can't load Python VM from %s : %s", dll_path, DLL_Error(self->_handle));
        return 2;

    self->Py_Version                   = DLL_BindVar(self->_handle, "Py_Version");
    self->Py_OptimizeFlag              = DLL_BindVar(self->_handle, "Py_OptimizeFlag");
    self->Py_DontWriteBytecodeFlag     = DLL_BindVar(self->_handle, "Py_DontWriteBytecodeFlag");
    self->Py_NoSiteFlag                = DLL_BindVar(self->_handle, "Py_NoSiteFlag");
    self->Py_NoUserSiteDirectory       = DLL_BindVar(self->_handle, "Py_NoUserSiteDirectory");
    self->Py_SetProgramName            = DLL_BindFun(self->_handle, "Py_SetProgramName");
    self->Py_GetProgramName            = DLL_BindFun(self->_handle, "Py_GetProgramName");
    self->Py_SetPythonHome             = DLL_BindFun(self->_handle, "Py_SetPythonHome");
    self->Py_GetPythonHome             = DLL_BindFun(self->_handle, "Py_GetPythonHome");
    self->Py_Initialize                = DLL_BindFun(self->_handle, "Py_Initialize");
    self->Py_IsInitialized             = DLL_BindFun(self->_handle, "Py_IsInitialized");
    self->Py_Finalize                  = DLL_BindFun(self->_handle, "Py_Finalize");
    self->PySys_SetArgv                = DLL_BindFun(self->_handle, "PySys_SetArgv");
    self->PySys_SetArgvEx              = DLL_BindFun(self->_handle, "PySys_SetArgvEx");
    self->PySys_SetPath                = DLL_BindFun(self->_handle, "PySys_SetPath");
    self->Py_GetPrefix                 = DLL_BindFun(self->_handle, "Py_GetPrefix");
    self->Py_GetExecPrefix             = DLL_BindFun(self->_handle, "Py_GetExecPrefix");
    self->Py_GetPath                   = DLL_BindFun(self->_handle, "Py_GetPath");
    self->PyEval_InitThreads           = DLL_BindFun(self->_handle, "PyEval_InitThreads");
    self->PyEval_ThreadsInitialized    = DLL_BindFun(self->_handle, "PyEval_ThreadsInitialized");
    self->PyEval_SaveThread            = DLL_BindFun(self->_handle, "PyEval_SaveThread");
    self->PyEval_RestoreThread         = DLL_BindFun(self->_handle, "PyEval_RestoreThread");
    self->PyThreadState_Get            = DLL_BindFun(self->_handle, "PyThreadState_Get");
    self->PyThreadState_Swap           = DLL_BindFun(self->_handle, "PyThreadState_Swap");
    self->PyEval_AcquireThread         = DLL_BindFun(self->_handle, "PyEval_AcquireThread");
    self->PyEval_ReleaseThread         = DLL_BindFun(self->_handle, "PyEval_ReleaseThread");
    self->PyEval_AcquireLock           = DLL_BindFun(self->_handle, "PyEval_AcquireLock");
    self->PyEval_ReleaseLock           = DLL_BindFun(self->_handle, "PyEval_ReleaseLock");
    self->Py_NewInterpreter            = DLL_BindFun(self->_handle, "Py_NewInterpreter");
    self->Py_EndInterpreter            = DLL_BindFun(self->_handle, "Py_EndInterpreter");
    self->PySys_GetObject              = DLL_BindFun(self->_handle, "PySys_GetObject");
    self->PyRun_SimpleString           = DLL_BindFun(self->_handle, "PyRun_SimpleString");
    self->PyImport_ImportModule        = DLL_BindFun(self->_handle, "PyImport_ImportModule");
    self->Py_IncRef                    = DLL_BindFun(self->_handle, "Py_IncRef");
    self->Py_DecRef                    = DLL_BindFun(self->_handle, "Py_DecRef");
    self->PyErr_Occurred               = DLL_BindFun(self->_handle, "PyErr_Occurred");
    self->PyErr_GivenExceptionMatches  = DLL_BindFun(self->_handle, "PyErr_GivenExceptionMatches");
    self->PyErr_Clear                  = DLL_BindFun(self->_handle, "PyErr_Clear");
    self->Py_None                      = DLL_BindVar(self->_handle, "_Py_NoneStruct");
    self->Py_True                      = DLL_BindVar(self->_handle, "_Py_TrueStruct");
    self->Py_False                     = DLL_BindVar(self->_handle, "_Py_ZeroStruct");

    return 0;
}

void PVM_unload(PVM* self)
{
    if ( self->_handle != 0 )
    {
        DLL_Close(self->_handle);
        self->_handle = 0;
    }
}

void PVM_init(PVM* self)
{
    self->load   = PVM_load;
    self->unload = PVM_unload;
}

#undef DLL_LibHandle
#undef DLL_Load
#undef DLL_Close
#undef DLL_Error
#undef DLL_Var
#undef DLL_Fun
#undef DLL_BindVar
#undef DLL_BindFun

#endif /* PVM_C_INCLUDED */
