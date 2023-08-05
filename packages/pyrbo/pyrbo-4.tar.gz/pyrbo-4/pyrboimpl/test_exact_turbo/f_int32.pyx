# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def f_int32(np.ndarray[np.int32_t] py_v):
    cdef np.int32_t* v = &py_v[0]
    pass
