# flake8-in-file-ignores: noqa: E501

# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

__all__ = ("Preprocessor",)

from typing import TypeAlias, Any
from typing_extensions import TypedDict, NotRequired
from collections.abc import Callable, Iterable, Mapping
import re

Pattern:    TypeAlias = re.Pattern[str]
Match:      TypeAlias = re.Match[str]
Attrs:      TypeAlias = Mapping[str, Any]
MacroScope: TypeAlias = Mapping[str, str | None]

class Node(TypedDict):
    kind: str
    attrs: Attrs
    matched: str
    replacement: NotRequired[str]


class Preprocessor:

    comment_pattern: Pattern = re.compile(r"//.*?$|"
                                          r"/\*.*?\*/|"
                                          r"'(?:\\.|[^\\'])*'|"
                                          r'"(?:\\.|[^\\"])*"',
                                          re.DOTALL | re.MULTILINE)

    @staticmethod
    def comment_replacer(m: Match) -> str:
        s = m.group(0)
        return "" if s.startswith("//") else " " if s.startswith("/*") else s
        # return "" if s.startswith("//") else " " + ("\n" * s.count("\n")) if s.startswith("/*") else s

    basic_tokens: dict[str, str] = dict(
        bol     = r"^",
        eol     = r"$",
        ws      = r"[ \t\v\f]+",
        ws_opt  = r"[ \t\v\f]*",
        digits  = r"[0123456789]+",
        id      = r"[_a-zA-Z][_a-zA-Z0-9]*",
        any     = r".*?",  # ?
        lparen  = r"\(",
        rparen  = r"\)",
        dec_int = r"[-+]?\s*[0123456789]" + "[uU]?[lL]?|[lL]?[uU]?",  # ?
        hex_int = r"0[xX][0-9a-fA-F]+"    + "[uU]?[lL]?|[lL]?[uU]?",
        char    = r"L?'([^'\\]|\\['\"?\\abfnrtv]|\\[0-7][0-7]?[0-7]?|\\x[0-9a-fA-F]+)+'",
    )

    include_pattern: str = r"{bol}({ws_opt}#{ws_opt}include{ws_opt})(\"{any}\"|<{any}>){ws_opt}{eol}".format(**basic_tokens)
    define_pattern0: str = r"{bol}({ws_opt}#{ws_opt}define{ws})({id})(({ws})(({lparen}{ws_opt})?({dec_int}|{hex_int})({ws_opt}{rparen})?))?{ws_opt}{eol}".format(**basic_tokens)
    define_pattern:  str = r"{bol}({ws_opt}#{ws_opt}define{ws})({id})({ws})({any}){ws_opt}{eol}".format(**basic_tokens)
    undef_pattern:   str = r"{bol}({ws_opt}#{ws_opt}undef{ws})({id}){ws_opt}{eol}".format(**basic_tokens)
    ifdef_pattern:   str = r"{bol}({ws_opt}#{ws_opt}ifdef{ws})({id}){ws_opt}{eol}".format(**basic_tokens)
    ifndef_pattern:  str = r"{bol}({ws_opt}#{ws_opt}ifndef{ws})({id}){ws_opt}{eol}".format(**basic_tokens)
    if_def_pattern:  str = r"{bol}({ws_opt}#{ws_opt}if{ws}defined({ws}|{ws_opt}{lparen}))({id})({ws_opt}{rparen})?{ws_opt}{eol}".format(**basic_tokens)
    if_ndef_pattern: str = r"{bol}({ws_opt}#{ws_opt}if{ws_opt}!{ws_opt}defined({ws}|{ws_opt}{lparen}))({id})({ws_opt}{rparen})?{ws_opt}{eol}".format(**basic_tokens)
    if_pattern:      str = r"{bol}({ws_opt}#{ws_opt}if{ws})({any}){ws_opt}{eol}".format(**basic_tokens)
    elif_pattern:    str = r"{bol}({ws_opt}#{ws_opt}elif{ws})({any}){ws_opt}{eol}".format(**basic_tokens)
    else_pattern:    str = r"{bol}({ws_opt}#{ws_opt}else)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    endif_pattern:   str = r"{bol}({ws_opt}#{ws_opt}endif)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    error_pattern:   str = r"{bol}({ws_opt}#{ws_opt}error)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    pragma_pattern:  str = r"{bol}({ws_opt}#{ws_opt}pragma)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    line_pattern:    str = r"{bol}({ws_opt}#{ws_opt}line{ws})({digits})(({ws_opt})\"({any})\")?{ws_opt}{eol}".format(**basic_tokens)
    null_pattern:    str = r"{bol}({ws_opt}#){ws_opt}{eol}".format(**basic_tokens)
    subst_pattern:   str = r"({bol}|[^\w])({{macro}})({eol}|[^\w\d])".format(**basic_tokens)

    def eval_expr(self, expr_str: str, scope: MacroScope) -> Any:
        return eval(expr_str, {}, scope)

    def include_action(self, m: Match) -> Node:
        header = m.group(2)
        return dict(kind="#include",
                    attrs=dict(header=header[1:-1],
                               is_user_header=header.startswith('"')),
                    matched=m.group(0))

    def define_action0(self, m: Match) -> Node:
        macro, subst = m.group(2), m.group(5)
        return dict(kind="#define0",
                    attrs=dict(macro=macro, subst=subst),
                    matched=m.group(0),
                    replacement=m.group(1) + macro + (m.group(4) + m.group(7)
                                if m.group(7) is not None else " 1"))

    def define_action(self, m: Match) -> Node:
        macro, subst = m.group(2), m.group(4)
        expr_str = str(self.eval_expr(subst, self.define_macros))
        return dict(kind="#define",
                    attrs=dict(macro=macro, subst=subst),
                    matched=m.group(0),
                    replacement=m.group(1) + macro + m.group(3) + expr_str
                                if expr_str else "")

    def undef_action(self, m: Match) -> Node:
        macro = m.group(2)
        return dict(kind="#undef",
                    attrs=dict(macro=macro),
                    matched=m.group(0))

    def ifdef_action(self, m: Match) -> Node:
        macro = m.group(2)
        return dict(kind="#ifdef",
                    attrs=dict(macro=macro),
                    matched=m.group(0))

    def ifndef_action(self, m: Match) -> Node:
        macro = m.group(2)
        return dict(kind="#ifndef",
                    attrs=dict(macro=macro),
                    matched=m.group(0))

    def if_defined_action(self, m: Match) -> Node:
        macro = m.group(3)
        return dict(kind="#ifdef",
                    attrs=dict(macro=macro),
                    matched=m.group(0))

    def if_not_defined_action(self, m: Match) -> Node:
        macro = m.group(3)
        return dict(kind="#ifndef",
                    attrs=dict(macro=macro),
                    matched=m.group(0))

    def if_action(self, m: Match) -> Node:
        return dict(kind="#if",
                    attrs=dict(condition=m.group(2)),
                    matched=m.group(0))

    def elif_action(self, m: Match) -> Node:
        return dict(kind="#elif",
                    attrs=dict(condition=m.group(2)),
                    matched=m.group(0))

    def else_action(self, m: Match) -> Node:
        return dict(kind="#else",
                    attrs=dict(),
                    matched=m.group(0))

    def endif_action(self, m: Match) -> Node:
        return dict(kind="#endif",
                    attrs=dict(),
                    matched=m.group(0))

    def error_action(self, m: Match) -> Node:  # NOK
        return dict(kind="#error",
                    attrs=dict(),
                    matched=m.group(0))

    def pragma_action(self, m: Match) -> Node:  # NOK
        return dict(kind="#pragma",
                    attrs=dict(),
                    matched=m.group(0))

    def line_action(self, m: Match) -> Node:
        return dict(kind="#line",
                    attrs=dict(number=int(m.group(2)),
                               filename=m.group(5)),
                    matched=m.group(0))

    def null_action(self, m: Match) -> Node:
        return dict(kind="#null",
                    attrs=dict(),
                    matched=m.group(0))

    def substitute(self, text: str, scope: MacroScope) -> str:
        for macro, subst in scope.items():
            if subst is not None:
                pattern  = re.compile(self.subst_pattern.format(macro=macro))
                text, nsubs = pattern.subn(lambda m: m.group(1) + subst + m.group(3), text)
        return text

    patterns: tuple[tuple[Pattern, Callable[[Preprocessor, Match], Node]], ...] = (
        (re.compile(include_pattern), include_action),
        (re.compile(define_pattern0), define_action0),
        (re.compile(define_pattern),  define_action),
        (re.compile(undef_pattern),   undef_action),
        (re.compile(ifdef_pattern),   ifdef_action),
        (re.compile(ifndef_pattern),  ifndef_action),
        (re.compile(if_def_pattern),  if_defined_action),
        (re.compile(if_ndef_pattern), if_not_defined_action),
        (re.compile(if_pattern),      if_action),
        (re.compile(elif_pattern),    elif_action),
        (re.compile(else_pattern),    else_action),
        (re.compile(endif_pattern),   endif_action),
        (re.compile(error_pattern),   error_action),
        (re.compile(pragma_pattern),  pragma_action),
        (re.compile(line_pattern),    line_action),
        (re.compile(null_pattern),    null_action),
    )

    def preprocess(self, source: str,
                   define_macros: Iterable[tuple[str, str | None]] = (),
                   undef_macros:  Iterable[str] = ()) -> str:
        self.define_macros: MacroScope = dict(define_macros)
        self.undef_macros: set[str] = set(undef_macros)
        source = self.comment_pattern.sub(self.comment_replacer, source)
        source_lines = (line for line in source.splitlines())
        lines  = []
        insert = [True]
        for line in source_lines:
            for pattern, action in self.patterns:
                match = pattern.match(line)
                if match:
                    node = action(self, match)
                    # print("Node:", node["kind"])
                    # print("  attributes  ->", node["attrs"])
                    # print("  matched     ->", node["matched"])
                    # if "replacement" in node and node["replacement"] is not None:
                    #     print("  replacement ->", node["replacement"])
                    if node["kind"] == "#define0":
                        if insert[-1]:
                            self.define_macros[node["attrs"]["macro"]] = node["attrs"]["subst"]
                    elif node["kind"] == "#define":
                        if insert[-1]:
                            expr_str = str(self.eval_expr(node["attrs"]["subst"], self.define_macros))
                            self.define_macros[node["attrs"]["macro"]] = ("("+expr_str+")"
                                                                          if expr_str else "")
                    elif node["kind"] == "#undef":
                        if insert[-1]:
                            self.define_macros.pop(node["attrs"]["macro"], None)
                    elif node["kind"] == "#ifdef":
                        insert.append(insert[-1]
                                      and node["attrs"]["macro"] in self.define_macros)
                    elif node["kind"] == "#ifndef":
                        insert.append(insert[-1]
                                      and node["attrs"]["macro"] not in self.define_macros)
                    elif node["kind"] == "#if":
                        insert.append(insert[-1]
                                      and self.eval_expr(node["attrs"]["condition"], self.define_macros))
                    elif node["kind"] == "#elif":
                        condition = (not insert.pop()
                                     and self.eval_expr(node["attrs"]["condition"], self.define_macros))
                        insert.append(insert[-1] and condition)
                    elif node["kind"] == "#else":
                        condition = not insert.pop()
                        insert.append(insert[-1] and condition)
                    elif node["kind"] == "#endif":
                        insert.pop()

                    if (insert[-1]
                       and "replacement" in node and node["replacement"] is not None):
                        lines.append(node["replacement"])
                    break
            else:
                if insert[-1]:
                    lines.append(self.substitute(line, self.define_macros))
        return "\n".join(lines)
