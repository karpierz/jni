import ctypes
import sys

def as_ctypes_buf(obj):
    """
    Convert any buffer object (bytes, bytearray, memoryview, numpy, etc.)
    into a zero-copy ctypes buffer pointer.
    """
    mview = (obj if isinstance(obj, memoryview) else memoryview(obj)).cast("B")
    if mview.readonly:
        c_buf = (len(mview) * ctypes.c_char).from_buffer_copy(mview)
    else:
        c_buf = (len(mview) * ctypes.c_char).from_buffer(mview)
    return c_buf

v = b"12345"
x = as_ctypes_buf(v)
print(v, type(x), x[:])
x[2] = b"R"
print(v, type(x), x[:])
print()
v = bytearray(b"12345")
x = as_ctypes_buf(v)
print(v, type(x), x[:])
x[2] = b"R"
print(v, type(x), x[:])
print()
v = b"12345"
x = as_ctypes_buf(memoryview(v))
print(v, type(x), x[:])
x[2] = b"R"
print(v, type(x), x[:])
print()
v = bytearray(b"12345")
x = as_ctypes_buf(memoryview(v))
print(v, type(x), x[:])
x[2] = b"R"
print(v, type(x), x[:])
print()
