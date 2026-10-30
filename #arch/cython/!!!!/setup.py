# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("mystruct.pyx", language_level=3, force=None),
    include_dirs=["."],
    script_args=["build_ext", "--inplace"]
)
