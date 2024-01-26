# Copyright (c) 2011 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/license/zlib
#
# Strictly based on Thomas Heller's recipe.
# https://sourceforge.net/p/ctypes/mailman/message/22650014/

"""This module implements pointer arithmetic for ctypes pointers."""

__all__ = ('c_ptr_add', 'c_ptr_sub', 'c_ptr_iadd', 'c_ptr_isub')


def c_ptr_add(ptr, other):
    """
    Add an integer to a pointer instance.

    Returns a new pointer:

    >>> import ctypes
    >>> string_ptr = ctypes.c_char_p(b'foobar')
    >>> string_ptr.value
    b'foobar'
    >>> p2 = c_ptr_add(string_ptr, 3)
    >>> print(p2.value)
    b'bar'
    >>> string_ptr.value
    b'foobar'
    >>>
    """
    from ctypes import c_void_p, cast  # , sizeof
    try:
        offset = other.__index__()
    except AttributeError:
        raise TypeError("Can only add integer to pointer")
    void_p = cast(ptr, c_void_p)
    void_p.value += offset  # * sizeof(ptr._type_)
    return cast(void_p, type(ptr))


def c_ptr_sub(ptr, other):
    """
    Substract an integer or a pointer from a pointer.

    Returns a new pointer or an integer.

    >>> import ctypes
    >>> string_ptr = ctypes.c_char_p(b'foobar')
    >>> string_ptr.value
    b'foobar'
    >>> p2 = c_ptr_add(string_ptr, 3)
    >>> print(p2.value)
    b'bar'
    >>> string_ptr.value
    b'foobar'
    >>> print(c_ptr_sub(p2, string_ptr))
    3
    >>> print(c_ptr_sub(string_ptr, p2))
    -3
    >>>
    >>> p3 = c_ptr_sub(p2, 3)
    >>> p3.value
    b'foobar'
    >>>
    >>> c_ptr_sub(string_ptr, p3)
    0
    >>>
    """
    from ctypes import c_void_p, cast  # , sizeof
    if type(ptr) == type(other):
        return cast(ptr, c_void_p).value - cast(other, c_void_p).value
    else:
        try:
            offset = other.__index__()
        except AttributeError:
            raise TypeError("Can only substract pointer or integer from pointer")
        void_p = cast(ptr, c_void_p)
        void_p.value -= offset  # * sizeof(ptr._type_)
        return cast(void_p, type(ptr))


def c_ptr_iadd(ptr, other):
    """
    Add an integer to a pointer instance in place:

    >>> import ctypes
    >>> string_ptr = ctypes.c_char_p(b'foobar')
    >>> string_ptr.value
    b'foobar'
    >>> c_ptr_iadd(string_ptr, 3)
    >>> string_ptr.value
    b'bar'
    >>>
    """
    from ctypes import c_void_p, cast  # , sizeof
    from ctypes import pointer, POINTER
    try:
        offset = other.__index__()
    except AttributeError:
        raise TypeError("Can only add integer to pointer")
    void_pp = cast(pointer(ptr), POINTER(c_void_p))
    void_pp.contents.value += offset  # * sizeof(ptr._type_)


def c_ptr_isub(ptr, other):
    """
    Substract an integer or a pointer from a pointer.

    Returns a new pointer or an integer.

    >>> import ctypes
    >>> string_ptr = ctypes.c_char_p(b'foobar')
    >>> string_ptr.value
    b'foobar'
    >>> c_ptr_iadd(string_ptr, 4)
    >>> string_ptr.value
    b'ar'
    >>> c_ptr_isub(string_ptr, 2)
    >>> string_ptr.value
    b'obar'
    >>> c_ptr_isub(string_ptr, 1)
    >>> string_ptr.value
    b'oobar'
    >>> c_ptr_isub(string_ptr, 1)
    >>> string_ptr.value
    b'foobar'
    >>>
    """
    from ctypes import c_void_p, cast  # , sizeof
    from ctypes import pointer, POINTER
    try:
        offset = other.__index__()
    except AttributeError:
        raise TypeError("Can only substract integer from pointer")
    void_pp = cast(pointer(ptr), POINTER(c_void_p))
    void_pp.contents.value -= offset  # * sizeof(ptr._type_)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
