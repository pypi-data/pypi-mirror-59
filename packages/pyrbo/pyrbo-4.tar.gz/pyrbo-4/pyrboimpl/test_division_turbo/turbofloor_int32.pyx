# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def turbofloor_int32(np.int32_t x, np.int32_t y):
    return x // y
