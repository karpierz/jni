@echo off
setlocal & pushd "%~dp0"..
del /F/Q src\jni\cython\jni.c
del /F/Q src\jni\cython\jni.cp313-win_amd64.pyd
del /F/Q src\jni\cython\jni.h
py setup.py build_ext --inplace
dos2unix src\jni\cython\jni.c 2> nul
dos2unix src\jni\cython\jni.h 2> nul
popd & endlocal
