@echo off
setlocal
set JAVA8_HOME=C:\Program Files\Java\jdk1.8.0_202
if not defined JAVA_HOME (set JAVA_HOME=%JAVA8_HOME%)
set javac="%JAVA_HOME%"\bin\javac -encoding UTF-8 -g:none -deprecation -Xlint:unchecked ^
    -source 1.8 -target 1.8 -bootclasspath "%JAVA8_HOME%\jre\lib\rt.jar"
set py=C:\Windows\py.exe -3.7 -B
pushd "%~dp0"
rem # for jni.cffi
del /F/Q src\jni\cffi\jni.i  2> nul
del /F/Q src\jni\cffi\jni.py 2> nul
rem # for jni.cython
del /F/Q src\jni\cython\jni.c 2> nul
del /F/Q src\jni\cython\jni.h 2> nul
rem # for jni.cffi, jni.cython and jni.capi
rmdir /Q/S build 2> nul
%py% setup.py build_ext --inplace
rmdir /Q/S build 2> nul
popd
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
