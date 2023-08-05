# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def noinfer_int32(np.ndarray[np.int32_t] py_x, np.ndarray[np.int32_t] py_y):
    cdef np.int32_t* x = &py_x[0]
    cdef np.int32_t* y = &py_y[0]
    pass
