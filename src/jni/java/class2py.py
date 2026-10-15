# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

from __future__ import annotations

__all__ = ('class2py',)

from typing import TypeAlias
import sys
from os import PathLike
from pathlib import Path
import logging

StrPath: TypeAlias = str | PathLike[str]


def class2py(class_file: StrPath,
             target_dir: StrPath | None = None,
             *, header: str | None = None) -> Path:
    """Create a Python representation of a Java .class file."""
    from codecs import encode
    import io
    import re
    class_file = Path(str(class_file))
    py_file = class_file.with_suffix(".py")
    py_file = py_file.with_stem(py_file.stem.replace("$", "_"))
    if target_dir is not None:
        py_file = Path(str(target_dir))/py_file.name
    is_new_py = not py_file.exists()
    jcode_regex = re.compile(r"(?P<beg>(.*\n)*)[ \t]*__javacode__[ \t]*="
                             r"\s*(((.|\n)*?\((.|\n)*?\))|(None[ \t]*\n))"
                             r"(?P<end>(.|\n)*)")
    if header is None:
        header = """\
# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: CC-BY-NC-ND-4.0 OR LicenseRef-Proprietary
# Please refer to the accompanying LICENSE file.

"""
    footer = """
"""
    with (class_file.open("rb") as fi,
          py_file.open("a+t", newline="") as fo,
          io.StringIO() as tmp):
        fo.seek(0)
        content = fo.read()
        match = jcode_regex.match(content)
        beg = match.group("beg") if match else ""
        end = match.group("end") if match else ""
        print(header if is_new_py else beg, end="", file=tmp)
        if is_new_py: print("__jnimethods__ = (\n)\n", file=tmp)
        print("__javacode__ = bytearray(  # Generated automatically; DO NOT EDIT.", file=tmp)
        while True:
            row = fi.read(20)
            if not row:
                break
            line = "".join(r"\x%c%c" % (c1, c2)
                           for c1, c2 in zip(*[iter(encode(row, "hex"))] * 2))
            print(f'    b"{line}"', file=tmp)
        print(")", end="", file=tmp)
        print(footer if is_new_py else end, end="", file=tmp)
        if tmp.getvalue() != content:
            fo.seek(0)
            fo.truncate()
            fo.write(tmp.getvalue())
    return py_file


def main(argv: list[str] = sys.argv[1:]) -> int:
    """Generate a Python representation of a Java .class file."""
    from argparse import ArgumentParser
    app_name = __package__ or "class2py"
    parser = ArgumentParser(prog=f"python -m {app_name}", description=main.__doc__)
    parser.add_argument("class_file", help="Path to the Java .class file")
    parser.add_argument("target_dir", nargs="?",
                        help="Output directory for the generated Python files")
    parser.add_argument("--header", default=None,
                        help="Custom header for newly generated Python files")
    parser.add_argument("--log", type=str, default="warning",
                        choices=["critical", "error", "warning", "info", "debug"],
                        help="Provide logging level. "
                             "Example --log debug, default='warning'")
    args = parser.parse_args(argv)
    # logging config
    logging.basicConfig(format="[%(levelname)s]:%(message)s",
                        level=getattr(logging, args.log.upper()))

    class2py(args.class_file, args.target_dir, header=args.header)
    return 0


if __name__.rpartition(".")[-1] == "__main__":
    sys.exit(main())
