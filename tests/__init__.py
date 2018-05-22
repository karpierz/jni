# Copyright (c) 2004-2018 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from __future__ import absolute_import

__all__ = ('top_dir', 'test_dir')

import sys, os, importlib
if sys.version_info.major <= 2:  # pragma: no cover
    sys.modules["unittest"] = importlib.import_module("unittest2")
    sys.modules["unittest.mock"] = importlib.import_module("mock")
sys.dont_write_bytecode = True
test_dir = os.path.dirname(os.path.abspath(__file__))
top_dir = os.path.dirname(test_dir)
del sys, os, importlib
