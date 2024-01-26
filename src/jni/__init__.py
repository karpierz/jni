# Copyright (c) 2004 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from .__about__ import * ; del __about__  # noqa
from . import __config__ ; del __config__
from .__config__ import config

BACKEND = config.get("BACKEND", "ctypes")

try:
    exec(f"from .{BACKEND} import *", globals())
except ImportError:  # pragma: no cover
    raise ImportError(f"Unknown jni backend: {BACKEND}") from None

exec(f"del {BACKEND}", globals())
del config
