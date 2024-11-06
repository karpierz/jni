# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

import unittest
import sys
import os
from pathlib import Path
import multiprocessing
import logging

from . import test_dir
from . import _jvm

log = logging.getLogger(__name__)


def test_suite(names=None, omit=()):
    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name.startswith("test_") and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def test(jvm_path):
    argv = sys.argv[1:]

    print(f"Running testsuite using JVM: {jvm_path}\n", file=sys.stderr)

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
              "-ea", "-Xms16M", "-Xmx512M")
    try:
        tests = test_suite(argv or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        jvm.shutdown()
    return 0 if result.wasSuccessful() else 1


def main(argv=sys.argv[1:]):

    is_32bit = (sys.maxsize <= 2**32)
    dir_prefix = Path(os.environ["ProgramFiles(x86)" if is_32bit else "ProgramFiles"])
    # https://en.wikipedia.org/wiki/Java_version_history
    jvm_dll_paths = [
        # Oracle JDK/JRE
        dir_prefix/"Java/jdk1.8.0_202/jre/bin/server/jvm.dll",
        dir_prefix/"Java/jdk1.8.0_202/jre/bin/client/jvm.dll",
        dir_prefix/"Java/jre1.8.0_202/bin/server/jvm.dll",
        dir_prefix/"Java/jre1.8.0_202/bin/client/jvm.dll",
        dir_prefix/"Java/jdk-17/bin/server/jvm.dll",
        dir_prefix/"Java/jdk-21/bin/server/jvm.dll",
        # Azul JDK/JRE
        dir_prefix/"Zulu/zulu-8/jre/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-8/jre/bin/client/jvm.dll",
        dir_prefix/"Zulu/zulu-8-jre/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-8-jre/bin/client/jvm.dll",
        dir_prefix/"Zulu/zulu-11/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-11/bin/client/jvm.dll",
        dir_prefix/"Zulu/zulu-11-jre/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-11-jre/bin/client/jvm.dll",
        dir_prefix/"Zulu/zulu-17/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-17/bin/client/jvm.dll",
        dir_prefix/"Zulu/zulu-17-jre/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-17-jre/bin/client/jvm.dll",
        dir_prefix/"Zulu/zulu-21/bin/server/jvm.dll",
        dir_prefix/"Zulu/zulu-21-jre/bin/server/jvm.dll",
        # Liberica JDK/JRE
        dir_prefix/"BellSoft/LibericaJRE-8/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-8/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-8/jre/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-8/jre/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-11/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-11/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-17/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-17/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-21/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJDK-21/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-11/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-11/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-17/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-17/bin/client/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-21/bin/server/jvm.dll",
        dir_prefix/"BellSoft/LibericaJRE-21/bin/client/jvm.dll",
    ]
    jvm_paths = [item for item in jvm_dll_paths if item.exists()]
    if not jvm_paths:
        raise Exception("jvm.dll not found !")

    with multiprocessing.Pool(len(jvm_paths)) as pool:
        result = pool.map(test, jvm_paths)

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
