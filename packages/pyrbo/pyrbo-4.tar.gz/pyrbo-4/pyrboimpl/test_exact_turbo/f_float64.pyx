# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def f_float64(np.ndarray[np.float64_t] py_v):
    cdef np.float64_t* v = &py_v[0]
    pass
