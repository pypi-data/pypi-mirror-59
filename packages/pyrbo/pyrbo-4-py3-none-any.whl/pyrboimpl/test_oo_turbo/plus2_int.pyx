# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def plus2_int(self, np.int_t y):
    cdef np.int_t self_x = self.x
    cdef np.int_t z
    z = self_x + y
    return z
