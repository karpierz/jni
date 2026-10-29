# flake8-in-file-ignores: noqa: E402,F401,F403,F821

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from typing import TYPE_CHECKING
import importlib

from .__about__ import * ; del __about__    # type: ignore[name-defined]
from .__about__ import __all__ as __ab_all  # type: ignore[attr-defined]
from . import __config__ ; del __config__
from .__config__ import config, set_config  # type: ignore[attr-defined]

BACKEND: str = config.get("BACKEND", "ctypes")

if TYPE_CHECKING:
    from .ctypes import *
else:
    try:
        mod = importlib.import_module(f"{__package__}.{BACKEND}")
    except ImportError:  # pragma: no cover
        raise ImportError(f"Unknown jni backend: {BACKEND}") from None
    for name in mod.__all__: globals()[name] = getattr(mod, name)
    __all__ = tuple(__ab_all) + tuple(mod.__all__)
    __all__ += ("defined", "from_oid", "config")

del BACKEND

from utlx import defined
from utlx.platform import from_oid
config = set_config
