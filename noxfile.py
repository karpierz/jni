# Copyright (c) 2026 Adam Karpierz
# SPDX-License-Identifier: Zlib

# /// script
# dependencies = ["nox>=2026.8.17", "nox_ext", "nox_lib"]
# ///

from __future__ import annotations

from typing import Any
import sys
import os
import shutil
import subprocess
import warnings

import nox
import nox_ext
import nox_lib
from nox_ext import print, pprint
from nox_lib.util import Path, copytree, rmtree

env = os.environ

# Configuration

PKG = nox.get_package_data()

PYPROJECT   = nox.project.load_toml("pyproject.toml")
PY_VERSIONS = nox.project.python_versions(PYPROJECT)
PY_DEFAULT  = "3.14"

# Prevent Python from writing bytecode
env["PYTHONDONTWRITEBYTECODE"] = "1"
# pass_env = ["JAVA_HOME"]
# env["PKG_INITIAL_BUILD"] = "1"

# Sessions

@nox.session(python=[PY_DEFAULT], default=False,
    requires=["cleanup"])
def prepare(session: nox.Session) -> None:
    """Preparing the repository"""
    session.install("setuptools>=81.0.0", "packaging>=26.3.0",
                    "py-utlx>=2.5.0", "cffi>=2.1.1", "cython>=3.3.0")
    from functools import partial
    from itertools import chain
    import tempfile
    from utlx import Path

    JAVA_HOME = r"C:\Program Files\Zulu\zulu-17"

    javac = partial(session.run, rf"{JAVA_HOME}\bin\javac", "-encoding", "UTF-8",
                    "-g:none", "-deprecation", "-Xlint:unchecked", "--release", "8",
                    external=True)
    dos2unix = partial(session.run_quiet, "dos2unix", external=True)

    os.environ["JAVA_HOME"] = JAVA_HOME

    root_dir = Path(session.root_dir)
    build_dir = root_dir/"build"
    dist_dir  = root_dir/"dist"
    src_dir   = root_dir/"src"
    tests_dir = root_dir/"tests"

    # Please use manually for the first time:
    #   py -3.14 -m build --sdist --no-isolation
    session.py_quiet("-m", "build", "--sdist", "--no-isolation")
    print("Clean for jni.cffi ...")
    (src_dir/"jni/cffi/jni.i").unlink()
    (src_dir/"jni/cffi/jni.py").unlink()
    print("Clean for jni.cython ...")
    (src_dir/"jni/cython/jni.c").unlink()
    (src_dir/"jni/cython/jni.h").unlink()
    print("Regenerate for jni.cffi, jni.cython and jni.capi ...")
    session.py("-m", "build", "--sdist", "--no-isolation")
    dos2unix(src_dir/"jni/cffi/jni.py")
    dos2unix(src_dir/"jni/cython/jni.c")
    dos2unix(src_dir/"jni/cython/jni.h")
    print("Clean for jni.cffi, jni.cython and jni.capi ...")
    (root_dir/"build").rmtree()
    (root_dir/"dist").rmtree()

    session.install(".")
    print("Compile java classes ...")
    tests_java_dir  = tests_dir/"java"
    tests_class_dir = tests_java_dir/"classes"
    tests_class_dir.mkdir()
    tests_class_dir.cleartree()
    with tempfile.NamedTemporaryFile("wt", encoding="utf-8",
                                     delete_on_close=False) as fp:
        java_files = (tests_java_dir/"org/python").rglob("*.java")
        fp.writelines(str(item) + "\n" for item in java_files)
        fp.close()
        javac("-d", tests_class_dir, "-classpath", tests_java_dir/"lib/*", f"@{fp.name}")
    session.py("-m", "jni.java.class2py",
               tests_class_dir/"org/python/jni/test/BaseExample.class",
               tests_java_dir/"org/python/jni/test")

    print("Done")

@nox.session(python=[PY_DEFAULT], default=False)
def cleanup(session: nox.Session) -> None:
    """Cleaning the repository"""
    nox_lib.cleanup.clean_cmd(session)
    nox_lib.cleanup.cleanup(session)

@nox.session(python=[*PY_VERSIONS,
                     "pypy3.11", "pypy3.12",
                     "graalpy3.13"])
def tests(session: nox.Session) -> None:
    """Running tests"""
    session.install(".", "--group=test")
    nox_lib.tests.unittests(session)

@nox.session(python=[PY_DEFAULT], default=False)
def coverage(session: nox.Session) -> None:
    """Running code coverage analysis"""
    session.install(".", "--group=coverage")
    nox_lib.coverage.coverage(session)

@nox.session(python=[PY_DEFAULT])
def docs(session: nox.Session) -> None:
    """Building documentation and running doc tests"""
    session.install(".", "--group=docs")
    nox_lib.docs.sphinx(session)

for python in tests.python:
    @nox.session(name=f"build_py-{python}", python=[python],
                 default=False, requires=[f"tests-{python}"])
    def build_py(session: nox.Session) -> None:
        """Building the package - for particular Python version"""
        session.install("--group=build-py")
        nox_lib.build.build_wheel_py(session, with_pyc_wheel=True)

@nox.session(python=[PY_DEFAULT], default=False,
    requires=[f"build_py-{python}" for python in tests.python] + ["docs"])
def build(session: nox.Session) -> None:
    """Building the package - final stage"""
    session.install("--group=build")
    nox_lib.build.build_sdist(session)

@nox.session(python=[PY_DEFAULT], default=False,
    requires=["build"])
def publish(session: nox.Session) -> None:
    """Publishing the package and documentation"""
    session.install("--group=publish")
    nox_lib.publish.on_pypi(session)
    nox_lib.publish.docs_on_gh_pages(session)

@nox.session(python=[PY_DEFAULT])
def typing(session: nox.Session) -> None:
    """Static type checking"""
    session.install(".", "--group=typing")
    nox_lib.typing.mypy(session)

@nox.session(python=[PY_DEFAULT])
def lint(session: nox.Session) -> None:
    """Checking code style and quality"""
    session.install(".", "--group=lint")
    nox_lib.lint.flake8(session)
