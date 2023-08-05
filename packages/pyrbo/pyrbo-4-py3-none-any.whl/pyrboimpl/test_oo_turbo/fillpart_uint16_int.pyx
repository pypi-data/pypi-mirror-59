# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fillpart_uint16_int(self, np.uint32_t i, np.uint32_t j, np.int_t v):
    cdef np.ndarray[np.uint16_t] py_self_u = self.u
    cdef np.uint16_t* self_u = &py_self_u[0]
    while i < j:
        self_u[i] = v
        i += 1
