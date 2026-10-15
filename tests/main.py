# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

import unittest
import sys
import os
from pathlib import Path
import multiprocessing as mp
import logging

from utlx.platform import is_32bits, is_pypy, is_graalpy

from . import test_dir

log = logging.getLogger(__name__)


def test_suite(names=None, include=(), exclude=()):
    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:  # pragma: no branch
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if (name.startswith("test_") or name in include)
                     and name not in exclude]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def test_func(jvm_path, backend="ctypes"):
    argv = sys.argv[1:]

    from jni import config
    config(BACKEND=backend)
    from . import _jvm

    print(f"\nRunning testsuite for backend: {backend} using JVM: {jvm_path}\n",
          flush=True, file=sys.stderr)
    print(end="", flush=True)

    package = sys.modules[__package__]
    package.jvm = jvm = _jvm.JVM(jvm_path)
    jvm.JavaException = JavaException
    jvm.ExceptionsMap = {
        _jvm.EStatusCode.ERR:       UnknownError,
        _jvm.EStatusCode.EDETACHED: ThreadNotAttachedError,
        _jvm.EStatusCode.EVERSION:  VersionNotSupportedError,
        _jvm.EStatusCode.ENOMEM:    NotEnoughMemoryError,
        _jvm.EStatusCode.EEXIST:    JVMAlreadyExistError,
        _jvm.EStatusCode.EINVAL:    InvalidArgumentError,
    }
    jvm.start("-Djava.class.path={}".format(
              os.pathsep.join([str(test_dir/"java/classes")])),
              "-ea", "-Xms64M", "-Xmx512M")
    try:
        tests = test_suite(argv or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        jvm.shutdown()
        del jvm, package.jvm
    return 0 if result.wasSuccessful() else 1


def main(argv=sys.argv[1:]):

    dir_prefix = Path(os.environ["ProgramFiles(x86)" if is_32bits else "ProgramFiles"])
    # https://en.wikipedia.org/wiki/Java_version_history
    jvm_dll_paths = [dir_prefix/jvm_path
                     for path in (test_dir/"jvm.txt").open("rt")
                     if (jvm_path := path.strip())
                     and not jvm_path.startswith("#")
                     and (dir_prefix/jvm_path).exists()]
    if not jvm_dll_paths:
        raise Exception("jvm.dll not found !")  # pragma: no cover

    result = []
    # because GraalPy has multiprocessing issues
    if not is_graalpy:  # pragma: no branch
        backends = ("ctypes",) if is_pypy or is_graalpy else ("ctypes",)  # "cffi")
        for backend in backends:  # , "cython", "capi"
            with mp.Pool(len(jvm_dll_paths)) as pool:
                result += pool.starmap(test_func, ((jvm_path, backend)
                                                   for jvm_path in jvm_dll_paths))
    # Needed for coverage
    try:
        test_func(1)
        raise RuntimeError(f"Expected DLL loading to fail "
                           "for {jvm_path!r}")  # pragma: no cover
    except RuntimeError as exc:
        if not str(exc).startswith("First parameter must be a string"):
            raise exc  # pragma: no cover
    jvm_path = "nonexistent path"
    try:
        test_func("nonexistent path")
        raise RuntimeError(f"Expected DLL loading to fail "
                           "for {jvm_path!r}")  # pragma: no cover
    except RuntimeError as exc:
        if not str(exc).startswith(f"Unable to load DLL [{jvm_path}]"):
            raise exc  # pragma: no cover
    jvm_path = jvm_dll_paths[-1]
    result += [test_func(jvm_path, "ctypes")]
    #result += [test_func(jvm_path, "cffi")]

    return 0 if not any(result) else 1


class JavaException(Exception):
    """ """

class UnknownError(Exception):
    """ """

class ThreadNotAttachedError(Exception):
    """ """

class VersionNotSupportedError(Exception):
    """ """

class NotEnoughMemoryError(Exception):
    """ """

class JVMAlreadyExistError(Exception):
    """ """

class InvalidArgumentError(Exception):
    """ """
