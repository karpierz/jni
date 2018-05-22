# Copyright (c) 2004-2018 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from __future__ import absolute_import, print_function

import unittest
import sys
import os
import logging

from . import test_dir


def test_suite(names=None, omit=()):

    from .python import __name__ as pkg_name
    from .python import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main():

    from ._jvm import JVM

    jvm_dll_paths = [
        r"C:\Program Files\Java\jre7\bin\client\jvm.dll",
        r"C:\Program Files\Java\jre7\bin\server\jvm.dll",
        r"C:\Program Files (x86)\Java\jre7\bin\client\jvm.dll",
        r"C:\Program Files (x86)\Java\jre7\bin\server\jvm.dll",
        r"C:\Program Files\Java\jre1.8.0_161\bin\client\jvm.dll",
        r"C:\Program Files\Java\jre1.8.0_161\bin\server\jvm.dll",
        r"C:\Program Files (x86)\Java\jre1.8.0_161\bin\client\jvm.dll",
        r"C:\Program Files (x86)\Java\jre1.8.0_161\bin\server\jvm.dll",
        r"C:\Program Files\Java\jdk-9\bin\client\jvm.dll",
        r"C:\Program Files\Java\jdk-9\bin\server\jvm.dll",
        r"C:\Program Files (x86)\Java\jdk-9\bin\client\jvm.dll",
        r"C:\Program Files (x86)\Java\jdk-9\bin\server\jvm.dll",
    ]

    try:
        jvm_path = next(item for item in jvm_dll_paths if os.path.exists(item))
    except:
        raise Exception("jvm.dll not found !")

    print("Running testsuite using JVM:", jvm_path, "\n", file=sys.stderr)

    package = sys.modules[__package__]
    package.jvm = jvm = JVM(jvm_path)
    jvm.start("-ea", "-Xms16M", "-Xmx512M")
    try:
        tests = test_suite(sys.argv[1:] or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        jvm.shutdown()

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    main()
