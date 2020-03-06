# Copyright (c) 2004-2020 Adam Karpierz
# Licensed under CC BY-NC-ND 4.0
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "jni"
__summary__      = "Python bridge for the JNI (ctypes/cffi/cython-based)"
__uri__          = "https://pypi.org/project/jni/"
__version_info__ = type("version_info", (), dict(serial=6,
                        major=1, minor=0, micro=0, releaselevel="beta"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc", post=".post")
                   [__version_info__.releaselevel], __version_info__.serial
                   if __version_info__.releaselevel != "final" else "")
__author__       = "Adam Karpierz"
__maintainer__   = "Adam Karpierz"
__email__        = "adam@karpierz.net"
__copyright__    = "Copyright (c) 2004-2020 {0}, All Rights Reserved".format(
                   __author__)
__license__      = "Creative Commons BY-NC-ND 4.0 License ; {0}" \
                   "; {0}, Licensed under proprietary License".format(
                   "https://creativecommons.org/licenses/by-nc-nd/4.0",
                   __copyright__)
