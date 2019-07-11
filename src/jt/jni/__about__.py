# Copyright (c) 2004-2019 Adam Karpierz
# Licensed under proprietary License
# Please refer to the accompanying LICENSE file.

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "jtypes.jni"
__summary__      = "Python-Java JNI API bridge (ctypes/cffi/cython-based)"
__uri__          = "http://python.pl/jtypes.jni/"
__version_info__ = type("version_info", (), dict(serial=3,
                        major=1, minor=0, micro=0, releaselevel="beta"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc")[__version_info__.releaselevel],
                   "" if __version_info__.releaselevel == "final" else __version_info__.serial)
__author__       = "Adam Karpierz"
__maintainer__   = "Adam Karpierz"
__email__        = "adam@karpierz.net"
__copyright__    = "Copyright (c) 2004-2019 {0}, All Rights Reserved".format(
                   __author__)
__license__      = "{0}, Licensed under proprietary License".format(
                   __copyright__)
