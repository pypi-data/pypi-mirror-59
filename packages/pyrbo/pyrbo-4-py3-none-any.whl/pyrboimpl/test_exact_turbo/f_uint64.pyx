# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def f_uint64(np.ndarray[np.uint64_t] py_v):
    cdef np.uint64_t* v = &py_v[0]
    pass
