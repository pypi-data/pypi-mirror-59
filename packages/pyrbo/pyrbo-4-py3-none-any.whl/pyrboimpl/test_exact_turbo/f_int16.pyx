# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def f_int16(np.ndarray[np.int16_t] py_v):
    cdef np.int16_t* v = &py_v[0]
    pass
