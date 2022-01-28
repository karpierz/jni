# Copyright (c) 2004-2022 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from .__config__ import * ; del __config__  # noqa
from .__about__  import * ; del __about__   # noqa

BACKEND = config.get("BACKEND", "ctypes")

try:
    exec(f"from .{BACKEND} import *", globals())
except ImportError:
    raise ImportError(f"Unknown jni backend: {BACKEND}") from None

del config
