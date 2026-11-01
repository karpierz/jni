@echo off
setlocal & pushd "%~dp0..\include\jdk\android"
get https://android.googlesource.com/platform/libnativehelper/+/refs/heads/master/include_jni/jni.h?format=TEXT
certutil -f -decode jni.h jni.h > nul
popd & endlocal
