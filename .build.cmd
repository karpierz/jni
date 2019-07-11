@echo off
setlocal
set JAVA8_HOME=C:\Program Files\Java\jdk1.8.0_202
if not defined JAVA_HOME (set JAVA_HOME=%JAVA8_HOME%)
set javac="%JAVA_HOME%"\bin\javac -encoding UTF-8 -g:none -deprecation -Xlint:unchecked ^
    -source 1.8 -target 1.8 -bootclasspath "%JAVA8_HOME%\jre\lib\rt.jar"
set py=C:\Windows\py.exe -3.7 -B
set py2=C:\Windows\py.exe -2.7 -B
set vc32="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%ProgramFiles(x86)%\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
pushd "%~dp0"
rem # for jni.cffi
del /F/Q src\jt\jni\cffi\jni.py 2> nul
%py% -c "import sys;sys.path.insert(0, 'src/jt');import jni.cffi"
rem # for jni.cython and jni.capi
%py% setup.py build_ext --inplace
popd
pushd "%~dp0"\tests
rmdir /Q/S java\classes 2> nul & mkdir java\classes
dir /S/B/O:N ^
    java\com\jt\jni\test\*.java ^
    2> nul > build.fil
%javac% -d java/classes -classpath java/lib/* @build.fil
del /F/Q build.fil
popd
endlocal
