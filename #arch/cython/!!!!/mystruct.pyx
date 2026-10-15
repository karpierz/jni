# mystruct.pyx

# distutils: language=c

from libc.string cimport strdup
from libc.stdlib cimport malloc, free

from mystruct_c cimport MyStruct as C_MyStruct


cdef class MyStruct:
    cdef C_MyStruct s

    def __cinit__(self, int x=0, double y=0.0, name=""):
        self.s.x = x
        self.s.y = y
        self.s.name = strdup(name.encode())

    def __dealloc__(self):
        if self.s.name != NULL:
            free(self.s.name)

    @property
    def x(self):
        return self.s.x

    @x.setter
    def x(self, value):
        self.s.x = value

    @property
    def y(self):
        return self.s.y

    @y.setter
    def y(self, value):
        self.s.y = value

    @property
    def name(self):
        return self.s.name.decode()

    @name.setter
    def name(self, value):
        free(self.s.name)
        self.s.name = strdup(value.encode())
