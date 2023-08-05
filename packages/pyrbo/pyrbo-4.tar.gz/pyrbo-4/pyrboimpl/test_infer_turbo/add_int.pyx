# cython: language_level=3

cimport numpy as np
import cython


@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def add_int(np.int_t x, np.int_t y):
    return x + y
