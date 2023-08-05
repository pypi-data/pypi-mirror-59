# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def addxtoy_int32_float32(np.ndarray[np.int32_t] py_x, np.ndarray[np.float32_t] py_y, np.uint32_t n):
    cdef np.int32_t* x = &py_x[0]
    cdef np.float32_t* y = &py_y[0]
    while n:
        n -= 1
        y[n] += x[n]
