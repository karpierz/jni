# Copyright (c) 2004-2019 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from . import __config__ ; del __config__
from .__about__ import * ; del __about__

from .__config__ import config

BACKEND = config.get("BACKEND", "ctypes")

try:
    exec("from .{} import *".format(BACKEND), globals())
except ImportError:
    raise ImportError("Unknown jtypes.jni backend: {}".format(BACKEND))

del config
