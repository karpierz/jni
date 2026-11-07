# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

import unittest
import sys
from pathlib import Path
import re
import tempfile

from . import test_dir, top_dir


class UtilTestCaseCffi(unittest.TestCase):

    def test_C_preprocessor(self):

        from jni._util import Preprocessor

        src_dir  = top_dir/"src"
        cffi_dir = src_dir/"jni/cffi"

        sys.path.insert(0, str(src_dir))
        from jni._util import Preprocessor
        sys.path.pop(0)
        jni_h_path = cffi_dir/"jni.h"
        source = jni_h_path.read_text(encoding="utf-8")
        source = Preprocessor().preprocess(source,
            define_macros = (
                ("JNICALL",   ""),
                ("JNIIMPORT", ""),
                ("JNIEXPORT", ""),
            ),
            undef_macros = (
                "_JAVASOFT_JNI_H_",
                "__cplusplus",
                "JNI_TYPES_ALREADY_DEFINED_IN_JNI_MD_H",
                "_JNI_IMPLEMENTATION_",
            ))
        with tempfile.NamedTemporaryFile(suffix="_jni.i",
                                         delete=False) as tmp_file:
            tmp_file.file.close()
            jni_i_path = Path(tmp_file.name)
            jni_i_path.write_text(source, newline="",
                                  encoding="utf-8")

        self.assertTrue(jni_i_path.exists())

    def test_C_preprocessor_regex(self):

        from jni._util import Preprocessor

        char_pattern = Preprocessor.basic_tokens["char"]
        char_regex   = re.compile(r"^" + char_pattern + r"$")

        vals = [
            r"'a'",
            r"L'a'",
            r"'$'",
            r"L'$'",
            r"'*'",
            r"L'*'",
            r"'\''",
            r"'\"'",
            r"'\\'",
            r"'\a'",
            r"'\b'",
            r"'\f'",
            r"'\n'",
            r"'\r'",
            r"'\t'",
            r"'\v'",
            r"'\0'",
            r"'\06'",
            r"'\075'",
            r"'\x0'",
            r"'\x0aF'",
            r"'\x0aF23B87c98'",
        ]

        for val in vals:
            self.assertTrue(char_regex.match(val))
