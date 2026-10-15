Changelog
=========

1.3.0b3 (2026-10-15)
--------------------
- Added support for Python 3.15
- Added support for PyPy 3.12
- Added support for GraalPy 3.13
- GraalPy <= 3.12 is not supported due to 'ctypes' incompatibility.
- Dropped support for Python 3.10 (due to compatibility issues).
- Added support for Java 25
- Moved jni.c and pvm.c to the 'jni' subdirectory.
- Added class2py.py utility.
- 100% code linting.
- 95% code coverage.
- Added typing support and marked the package as typed.
- Copyright year update.
- The documentation has been moved from Read the Docs to GitHub Pages.
- Switched from tox to Nox for project automation.
- Updated nox's default python to version 3.14
- Added the nox's 'cleanup' test environment.
- Fix for nox 'lint' session.
- Setup update, unification and bug fixes.

1.2.0b1 (2025-06-17)
--------------------
- Added support for Python 3.14
- Added support for PyPy 3.11
- Dropped support for Python 3.9 (due to compatibility issues).
- Dropped support for PyPy 3.9
- | Dropped support for Oracle Java 1.8 (jdk, jre) due to licensing issues
  | and the end of support from Oracle.
- Updated Read the Docs' Python version to 3.13
- Updated tox's base_python to version 3.13
- The distribution is now built using 'build' instead of 'setuptools'.
- Copyright year update.
- Setup update (mainly dependencies).

1.1.0b6 (2024-12-01)
--------------------
- Fixes for embedded python.
- Java 17 is now the primary build/test environment.
- Added support for Python 3.13
- Dropped support for Python 3.8
- jni.c and pvm.c (useful for embedded python apps) have been added.
- Unittest have been performed for much more JVMs.
- Tox configuration is now in native (toml) format.
- Setup fixes.
- Setup update (mainly dependencies).

1.0.0b22 (2024-01-26)
---------------------
- The tox configuration has been moved to pyproject.toml
- Setup update (now based on tox >= 4.0).
- Added support for Python 3.10, 3.11 and 3.12
- Dropped support for Python 3.7
- Added support for PyPy 3.9 and 3.10
- Copyright year update.

1.0.0b20 (2022-01-29)
---------------------
- Dropped support for Python 3.6
- Setup update.

1.0.0b18 (2021-10-13)
---------------------
- dll_path argument of load() can also be type os.PathLike.
- Copyright year update.
- Setup update.

1.0.0b17 (2020-11-10)
---------------------
- Added support for Python 3.9
- General update, improvements and cleanup.
- Setup update and improvements.
- Fixed docs setup.

1.0.0b7 (2020-03-08)
--------------------
- Dropped support for Python2
- Update of license info.
- Setup update.

1.0.0b4 (2019-07-10)
--------------------
- Last release for Python2

1.0.0b3 (2018-05-22)
--------------------
- Update of the required setuptools version.

1.0.0b2 (2018-02-26)
--------------------
- Improvement and simplification of setup and packaging.

1.0.0b1 (2017-11-18)
--------------------
- First 'official' version.

0.1.1 (2005-10-05)
------------------
- Initial version.
