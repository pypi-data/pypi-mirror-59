# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def multidim_float32(np.ndarray[np.float32_t, ndim=2] py_a):
    cdef np.float32_t* a = &py_a[0, 0]
    return a[0], a[1], a[2], a[3]
