# Copyright (c) 2004-2018 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from __future__ import absolute_import

from os import path
from setuptools import setup

top_dir = path.dirname(path.abspath(__file__))
with open(path.join(top_dir, "jt", "jvm", "jni", "__about__.py")) as f:
    class about: exec(f.read(), None)

setup(
    name             = about.__title__,
    version          = about.__version__,
    description      = about.__summary__,
    url              = about.__uri__,
    download_url     = about.__uri__,

    author           = about.__author__,
    author_email     = about.__email__,
    maintainer       = about.__maintainer__,
    maintainer_email = about.__email__,
    license          = about.__license__,
)
