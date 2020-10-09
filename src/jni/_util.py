# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.


def get_config(cfg_path, cfg_section):
    from os import path
    from configparser import ConfigParser, ExtendedInterpolation
    if not path.isfile(cfg_path):
        return {}
    cfg = ConfigParser(interpolation=ExtendedInterpolation(),
                       inline_comment_prefixes=('#', ';'),
                       default_section=cfg_section)
    cfg.read(cfg_path, "utf-8")
    return cfg[cfg_section]


def make_config(cfg_fname, cfg_section):
    import sys
    from pathlib import Path
    fglobals = sys._getframe(1).f_globals
    cfg_path = Path(fglobals["__file__"]).parent/cfg_fname
    fglobals["config"] = get_config(str(cfg_path), cfg_section)
    fglobals.pop("__builtins__", None)
    fglobals.pop("__cached__",   None)
    fglobals["__all__"] = ("config",)


class Preprocessor:

    import re

    class adict(dict):
        __getattr__ = dict.__getitem__
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__
        copy = lambda self: self.__class__(self)

    comment_pattern = re.compile(r"//.*?$|"
                                 r"/\*.*?\*/|"
                                 r"'(?:\\.|[^\\'])*'|"
                                 r'"(?:\\.|[^\\"])*"',
                                 re.DOTALL | re.MULTILINE)
    @staticmethod
    def comment_replacer(m):
        s = m.group(0)
        return "" if s.startswith("//") else " " if s.startswith("/*") else s
       #return "" if s.startswith("//") else " " + ("\n" * s.count("\n")) if s.startswith("/*") else s

    basic_tokens = dict(
        bol     = r"^",
        eol     = r"$",
        ws      = r"[ \t\v\f]+",
        ws_opt  = r"[ \t\v\f]*",
        digits  = r"[0123456789]+",
        id      = r"[_a-zA-Z][_a-zA-Z0-9]*",
        any     = r".*?", # ?
        lparen  = r"\(",
        rparen  = r"\)",
        dec_int = r"[-+]?\s*[0123456789]" + "[uU]?[lL]?|[lL]?[uU]?",  # ?
        hex_int = r"0[xX][0-9a-fA-F]+"    + "[uU]?[lL]?|[lL]?[uU]?",
        char    = r"L?'([^'\\]|\\['\"?\\abfnrtv]|\\[0-7][0-7]?[0-7]?|\\x[0-9a-fA-F]+)+'",
    )

    include_pattern = r"{bol}({ws_opt}#{ws_opt}include{ws_opt})(\"{any}\"|<{any}>){ws_opt}{eol}".format(**basic_tokens)
    define_pattern0 = r"{bol}({ws_opt}#{ws_opt}define{ws})({id})(({ws})(({lparen}{ws_opt})?({dec_int}|{hex_int})({ws_opt}{rparen})?))?{ws_opt}{eol}".format(**basic_tokens)
    define_pattern  = r"{bol}({ws_opt}#{ws_opt}define{ws})({id})({ws})({any}){ws_opt}{eol}".format(**basic_tokens)
    undef_pattern   = r"{bol}({ws_opt}#{ws_opt}undef{ws})({id}){ws_opt}{eol}".format(**basic_tokens)
    ifdef_pattern   = r"{bol}({ws_opt}#{ws_opt}ifdef{ws})({id}){ws_opt}{eol}".format(**basic_tokens)
    ifndef_pattern  = r"{bol}({ws_opt}#{ws_opt}ifndef{ws})({id}){ws_opt}{eol}".format(**basic_tokens)
    if_def_pattern  = r"{bol}({ws_opt}#{ws_opt}if{ws}defined({ws}|{ws_opt}{lparen}))({id})({ws_opt}{rparen})?{ws_opt}{eol}".format(**basic_tokens)
    if_ndef_pattern = r"{bol}({ws_opt}#{ws_opt}if{ws_opt}!{ws_opt}defined({ws}|{ws_opt}{lparen}))({id})({ws_opt}{rparen})?{ws_opt}{eol}".format(**basic_tokens)
    if_pattern      = r"{bol}({ws_opt}#{ws_opt}if{ws})({any}){ws_opt}{eol}".format(**basic_tokens)
    elif_pattern    = r"{bol}({ws_opt}#{ws_opt}elif{ws})({any}){ws_opt}{eol}".format(**basic_tokens)
    else_pattern    = r"{bol}({ws_opt}#{ws_opt}else)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    endif_pattern   = r"{bol}({ws_opt}#{ws_opt}endif)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    error_pattern   = r"{bol}({ws_opt}#{ws_opt}error)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    pragma_pattern  = r"{bol}({ws_opt}#{ws_opt}pragma)({ws}({any}))?{ws_opt}{eol}".format(**basic_tokens)
    line_pattern    = r"{bol}({ws_opt}#{ws_opt}line{ws})({digits})(({ws_opt})\"({any})\")?{ws_opt}{eol}".format(**basic_tokens)
    null_pattern    = r"{bol}({ws_opt}#){ws_opt}{eol}".format(**basic_tokens)
    subst_pattern   = r"({bol}|[^\w])({{macro}})({eol}|[^\w\d])".format(**basic_tokens)

    eval_expr = lambda self, str, scope: eval(str, {}, scope)

    def include_action(self, m):
        header = m.group(2)
        return self.adict(kind="#include",
                          attrs=self.adict(header=header[1:-1],
                                           is_user_header=header.startswith('"')),
                          matched=m.group(0))

    def define_action0(self, m):
        macro, subst = m.group(2), m.group(5)
        return self.adict(kind="#define0",
                          attrs=self.adict(macro=macro,
                                           subst=subst),
                          matched=m.group(0),
                          replacement=m.group(1) + macro + (m.group(4) + m.group(7)
                                      if m.group(7) is not None else " 1"))

    def define_action(self, m):
        macro, subst = m.group(2), m.group(4)
        expr_str = str(self.eval_expr(subst, self.define_macros))
        return self.adict(kind="#define",
                          attrs=self.adict(macro=macro,
                                           subst=subst),
                          matched=m.group(0),
                          replacement=m.group(1) + macro + m.group(3) +
                                      expr_str if expr_str else "")

    def undef_action(self, m):
        macro = m.group(2)
        return self.adict(kind="#undef",
                          attrs=self.adict(macro=macro),
                          matched=m.group(0))

    def ifdef_action(self, m):
        macro = m.group(2)
        return self.adict(kind="#ifdef",
                          attrs=self.adict(macro=macro),
                          matched=m.group(0))

    def ifndef_action(self, m):
        macro = m.group(2)
        return self.adict(kind="#ifndef",
                          attrs=self.adict(macro=macro),
                          matched=m.group(0))

    def if_def_action(self, m):
        macro = m.group(3)
        return self.adict(kind="#ifdef",
                          attrs=self.adict(macro=macro),
                          matched=m.group(0))

    def if_ndef_action(self, m):
        macro = m.group(3)
        return self.adict(kind="#ifndef",
                          attrs=self.adict(macro=macro),
                          matched=m.group(0))

    def if_action(self, m):
        return self.adict(kind="#if",
                          attrs=self.adict(condition=m.group(2)),
                          matched=m.group(0))

    def elif_action(self, m):
        return self.adict(kind="#elif",
                          attrs=self.adict(condition=m.group(2)),
                          matched=m.group(0))

    def else_action(self, m):
        return self.adict(kind="#else",
                          attrs=self.adict(),
                          matched=m.group(0))

    def endif_action(self, m):
        return self.adict(kind="#endif",
                          attrs=self.adict(),
                          matched=m.group(0))

    def error_action(self, m): # NOK
        return self.adict(kind="#error",
                          attrs=self.adict(),
                          matched=m.group(0))

    def pragma_action(self, m): # NOK
        return self.adict(kind="#pragma",
                          attrs=self.adict(),
                          matched=m.group(0))

    def line_action(self, m):
        return self.adict(kind="#line",
                          attrs=self.adict(number=int(m.group(2)),
                                           filename=m.group(5)),
                          matched=m.group(0))

    def null_action(self, m):
        return self.adict(kind="#null",
                          attrs=self.adict(),
                          matched=m.group(0))

    def substitute(self, text, scope):
        for macro, subst in scope.items():
            if subst is not None:
                pattern  = self.re.compile(self.subst_pattern.format(macro=macro))
                text, nsubs = pattern.subn(lambda m: m.group(1) + subst + m.group(3), text)
        return text

    patterns = (
        (re.compile(include_pattern), include_action),
        (re.compile(define_pattern0), define_action0),
        (re.compile(define_pattern),  define_action),
        (re.compile(undef_pattern),   undef_action),
        (re.compile(ifdef_pattern),   ifdef_action),
        (re.compile(ifndef_pattern),  ifndef_action),
        (re.compile(if_def_pattern),  if_def_action),
        (re.compile(if_ndef_pattern), if_ndef_action),
        (re.compile(if_pattern),      if_action),
        (re.compile(elif_pattern),    elif_action),
        (re.compile(else_pattern),    else_action),
        (re.compile(endif_pattern),   endif_action),
        (re.compile(error_pattern),   error_action),
        (re.compile(pragma_pattern),  pragma_action),
        (re.compile(line_pattern),    line_action),
        (re.compile(null_pattern),    null_action),
    )

    def preprocess(self, source, define_macros=(), undef_macros=()):
        self.define_macros = dict(define_macros)
        self.undef_macros  = set(undef_macros)
        source = self.comment_pattern.sub(self.comment_replacer, source)
        source_lines = (line for line in source.splitlines())
        lines  = []
        insert = [True]
        for line in source_lines:
            for pattern, action in self.patterns:
                match = pattern.match(line)
                if match:
                    node = action(self, match) 
                    #print("Node:", node.kind)
                    #print("  attributes  ->", node.attrs)
                    #print("  matched     ->", node.matched)
                    #if "replacement" in node and node.replacement is not None:
                    #    print("  replacement ->", node.replacement)
                    if node.kind == "#define0":
                        if insert[-1]:
                            self.define_macros[node.attrs.macro] = node.attrs.subst
                    elif node.kind == "#define":
                        if insert[-1]:
                            expr_str = str(self.eval_expr(node.attrs.subst, self.define_macros))
                            self.define_macros[node.attrs.macro] = ("("+expr_str+")"
                                                                    if expr_str else "")
                    elif node.kind == "#undef":
                        if insert[-1]:
                            self.define_macros.pop(node.attrs.macro, None)
                    elif node.kind == "#ifdef":
                        insert.append(insert[-1] and
                                      node.attrs.macro in self.define_macros)
                    elif node.kind == "#ifndef":
                        insert.append(insert[-1] and
                                      node.attrs.macro not in self.define_macros)
                    elif node.kind == "#if":
                        insert.append(insert[-1] and
                                      self.eval_expr(node.attrs.condition, self.define_macros))
                    elif node.kind == "#elif":
                        condition = (not insert.pop() and
                                     self.eval_expr(node.attrs.condition, self.define_macros))
                        insert.append(insert[-1] and condition)
                    elif node.kind == "#else":
                        condition = not insert.pop()
                        insert.append(insert[-1] and condition)
                    elif node.kind == "#endif":
                        insert.pop()

                    if (insert[-1] and
                        "replacement" in node and node.replacement is not None):
                        lines.append(node.replacement)
                    break
            else:
                if insert[-1]:
                    lines.append(self.substitute(line, self.define_macros))
        return "\n".join(lines)
