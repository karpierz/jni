# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from . import __config__
from .__about__ import *  # noqa
del __config__, __about__, _util

from .__config__ import config

BACKEND = config.get("BACKEND", "ctypes")

try:
    exec("from .{} import *".format(BACKEND), globals())
except ImportError:
    raise ImportError("Unknown jni backend: {}".format(BACKEND)) from None

del config
