# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def fieldlocal(obj):
    cdef np.int_t obj_field = obj.field
    obj_field = 6
    if False:
        obj.field = obj_field
