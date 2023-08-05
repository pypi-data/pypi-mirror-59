# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def turbotrue_float32(np.float32_t x, np.float32_t y):
    return x / y
