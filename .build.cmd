@echo off
setlocal
set JAVA8_HOME=C:\Program Files\Java\jdk1.8.0_202
if not defined JAVA_HOME (set JAVA_HOME=%JAVA8_HOME%)
set javac="%JAVA_HOME%"\bin\javac -encoding UTF-8 -g:none -deprecation -Xlint:unchecked ^
    -source 1.8 -target 1.8 -bootclasspath "%JAVA8_HOME%\jre\lib\rt.jar"
set py=C:\Windows\py.exe -3.7 -B
set vcdir=%ProgramFiles(x86)%\Microsoft Visual Studio\2019
set vc32="%vcdir%\Community\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%vcdir%\Community\VC\Auxiliary\Build\vcvars64.bat"
if exist %vc32% goto :start
set vc32="%vcdir%\BuildTools\VC\Auxiliary\Build\vcvars32.bat"
set vc64="%vcdir%\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
if exist %vc32% goto :start
echo VC compiler (2019) should be installed!
goto :exit
:start
pushd "%~dp0"
rem # for jni.cffi
del /F/Q src\jni\cffi\jni.py 2> nul
%py% -c "import sys;sys.path.insert(0, 'src');import jni.cffi"
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
:exit
endlocal
