jtypes.jni
==========

Pure Python Java package

Overview
========

  | **jtypes.jni** is a bridge between Python and Java JNI.
  | It is an effort to allow python programs full access to Java JNI API.

  `PyPI record <https://pypi.python.org/pypi/jtypes.jni>`__.

  | **jtypes.jni** is a lightweight Python package, based on the *ctypes* or *cffi* library.
  | It is done by implementing whole JNI API functionality in a clean Python
    instead of C/C++.


What is jtypes.jni:
-------------------

  **jtypes.jni** is an effort to allow python programs full access to Java JNI API.
  This is achieved not through re-implementing Python, as Jython/JPython has done,
  but rather through interfacing at the native level in both virtual machines.

  Known Bugs/Limitations :
    * Because of lack of JVM support, you cannot shutdown the JVM and then
      restart it.


Installation
============

Prerequisites:

+ Python 2.7 or Python 3.4 or later

  * http://www.python.org/
  * 2.7 and 3.7 are primary test environments.

+ pip and setuptools

  * http://pypi.python.org/pypi/pip
  * http://pypi.python.org/pypi/setuptools

To install run::

    python -m pip install --upgrade jtypes.jni

To ensure everything is running correctly you can run the tests using::

    python -m jt.jni.tests

License
=======

  | Copyright (c) 2004-2019 Adam Karpierz
  |
  | Licensed under proprietary License
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>
