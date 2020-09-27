//
// JNI bridge
//

// Taken from <jni.h>

#ifndef __has_attribute
  #define __has_attribute(x) 0
#endif
#if defined(_WIN32)
  #define JNIEXPORT __declspec(dllexport)
  #define JNIIMPORT __declspec(dllimport)
  #define JNICALL   __stdcall
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
#elif (defined(__GNUC__) && ((__GNUC__ > 4) || \
                             (__GNUC__ == 4) && (__GNUC_MINOR__ > 2))) || \
      __has_attribute(visibility)
  #ifdef ARM
    #define JNIEXPORT __attribute__((externally_visible,visibility("default")))
    #define JNIIMPORT __attribute__((externally_visible,visibility("default")))
  #else
    #define JNIEXPORT __attribute__((visibility("default")))
    #define JNIIMPORT __attribute__((visibility("default")))
  #endif
  #define JNICALL
  typedef int jint;
#else
  #define JNIEXPORT
  #define JNIIMPORT
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

typedef struct JavaVM JavaVM;

static void JNI_on_load  (JavaVM* jvm);
static void JNI_on_unload(JavaVM* jvm);

JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* jvm, void* reserved)
{
    (void)reserved;
    JNI_on_load(jvm);
    return JNI_VERSION_1_6;
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
