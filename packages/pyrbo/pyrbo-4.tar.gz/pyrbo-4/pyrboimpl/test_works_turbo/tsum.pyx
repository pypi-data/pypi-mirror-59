# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def tsum(np.uint32_t n, np.ndarray[np.float32_t] py_x, np.ndarray[np.float32_t] py_y, np.ndarray[np.float32_t] py_out):
    cdef np.float32_t* x = &py_x[0]
    cdef np.float32_t* y = &py_y[0]
    cdef np.float32_t* out = &py_out[0]
    cdef np.uint32_t i
    for i in range(n):
        out[i] = x[i] + y[i]
