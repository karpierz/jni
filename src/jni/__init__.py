# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from . import __config__ ; del __config__
from .__about__ import * ; del __about__  # noqa
del _util

from .__config__ import config

BACKEND = config.get("BACKEND", "ctypes")

try:
    exec(f"from .{BACKEND} import *", globals())
except ImportError:
    raise ImportError(f"Unknown jni backend: {BACKEND}") from None

del config
