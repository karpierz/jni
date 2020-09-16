# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

from typing import Optional
import unittest
import os
import re


class UtilTestCaseCFFI(unittest.TestCase):

    def test_preprocessor(self):

        from jni._util import Preprocessor

        char_pattern = Preprocessor.basic_tokens["char"]
        char_regexp  = re.compile(r"^" + char_pattern + r"$")

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
            self.assertTrue(char_regexp.match(val))
