@echo off
setlocal enableDelayedExpansion
set JAVA_HOME=C:\Program Files\Zulu\zulu-11
set javac="%JAVA_HOME%\bin\javac" -encoding UTF-8 -g:none ^
          -deprecation -Xlint:unchecked --release 8

rem pushd "%~dp0"
rem rem for jni.cffi
rem del /F/Q src\jni\cffi\jni.i  2> nul
rem del /F/Q src\jni\cffi\jni.py 2> nul
rem rem for jni.cython
rem del /F/Q src\jni\cython\jni.c 2> nul
rem del /F/Q src\jni\cython\jni.h 2> nul
rem rem for jni.cffi, jni.cython and jni.capi
rem rmdir /Q/S build 2> nul
rem popd

pushd "%~dp0"\tests
rmdir /Q/S java\classes 2> nul & mkdir java\classes
dir /S/B/O:N ^
    java\org\jt\jni\test\*.java ^
    2> nul > build.fil
%javac% -d java/classes -classpath java/lib/* @build.fil
del /F/Q build.fil
popd

:exit
endlocal
