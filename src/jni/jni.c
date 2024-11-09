// Copyright (c) 2004 Adam Karpierz
// Licensed under CC BY-NC-ND 4.0
// Licensed under proprietary License
// Please refer to the accompanying LICENSE file.

#ifndef JNI_C_INCLUDED
#define JNI_C_INCLUDED

//
// JNI bridge
//

// Taken from <jni.h>

#ifndef __has_attribute
  #define __has_attribute(x) 0
#endif

#if defined(_WIN32)
  #ifndef JNIEXPORT
    #define JNIEXPORT __declspec(dllexport)
  #endif
  #define JNIIMPORT __declspec(dllimport)
  #define JNICALL __stdcall
  #if defined(__CYGWIN__)
    typedef int jint;
  #elif defined(__GNUC__)
    // JNICALL causes problem for function prototypes
    // .. since I am not defining any JNI methods there is no need for it
    #undef  JNICALL
    #define JNICALL
    typedef long jint;
  #else
    typedef long jint;
  #endif
#else
  #ifndef JNIEXPORT
    #if (defined(__GNUC__) && ((__GNUC__ > 4) || \
                               (__GNUC__ == 4) && (__GNUC_MINOR__ > 2))) || \
        __has_attribute(visibility)
      #ifdef ARM
        #define JNIEXPORT __attribute__((externally_visible,visibility("default")))
      #else
        #define JNIEXPORT __attribute__((visibility("default")))
      #endif
    #else
      #define JNIEXPORT
    #endif
  #endif
  #if (defined(__GNUC__) && ((__GNUC__ > 4) || \
                             (__GNUC__ == 4) && (__GNUC_MINOR__ > 2))) || \
      __has_attribute(visibility)
    #ifdef ARM
      #define JNIIMPORT __attribute__((externally_visible,visibility("default")))
    #else
      #define JNIIMPORT __attribute__((visibility("default")))
    #endif
  #else
    #define JNIIMPORT
  #endif
  #define JNICALL
  typedef int jint;
#endif

#define JNI_VERSION_1_1 0x00010001
#define JNI_VERSION_1_2 0x00010002
#define JNI_VERSION_1_4 0x00010004
#define JNI_VERSION_1_6 0x00010006
#define JNI_VERSION_1_8 0x00010008
#define JNI_VERSION_9   0x00090000
#define JNI_VERSION_10  0x000a0000
#define JNI_VERSION_19  0x00130000
#define JNI_VERSION_20  0x00140000
#define JNI_VERSION_21  0x00150000

typedef struct JavaVM JavaVM;

int  JNI_on_load(JavaVM* jvm);
void JNI_on_unload(JavaVM* jvm);

JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* jvm, void* reserved)
{
    (void)reserved;
    return (JNI_on_load(jvm)) ? JNI_VERSION_1_6 : 0;
}

JNIEXPORT void JNICALL JNI_OnUnload(JavaVM* jvm, void* reserved)
{
    (void)reserved;
    JNI_on_unload(jvm);
}

//-- OS dependents --//

#if defined(_WIN32)

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

BOOL WINAPI DllMain(HINSTANCE hinst, DWORD reason, LPVOID reserved)
{
    (void)hinst; (void)reason; (void)reserved;
    return TRUE;
}

#endif

#endif /* JNI_C_INCLUDED */
