jni
===

Python bridge for the Java Native Interface.

Overview
========

| |package_bold| is a complete bridge between Python and Java JNI.
| It is an effort to allow python programs full access to Java JNI API.

`PyPI record`_.

`Documentation`_.

| |package_bold| is a lightweight Python package, based on the *ctypes*, or *cffi* library,
  or Cython wrapper (currently under development).
| It is done by implementing whole JNI API functionality in a clean Python instead of C/C++.
| |package_bold| also contains a JNI wrapper in pure C based on Python C-API (currently under
  development) - mainly for performance reasons.

What is |package|:
------------------

| |package_bold| is an effort to allow python programs full access to Java JNI API.
| This is achieved not through re-implementing Python, as Jython has done,
  but rather through interfacing at the native level in both virtual machines.

Known Bugs/Limitations :
  * Because of lack of JVM support, you cannot shutdown the JVM and then restart it.

Installation
============

Prerequisites:

+ Python 3.6 or higher

  * https://www.python.org/
  * 3.7 with Java 8 is a primary test environment.

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | Copyright (c) 2004-2022 Adam Karpierz
  | Licensed under CC BY-NC-ND 4.0
  | Licensed under proprietary License
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: jni
.. |package_bold| replace:: **jni**
.. |respository| replace:: https://github.com/karpierz/jni.git
.. _development page: https://github.com/karpierz/jni
.. _PyPI record: https://pypi.org/project/jni/
.. _Documentation: https://jni.readthedocs.io/
