# cython: language_level=3

cimport numpy as np
import cython

DEF y = 6

@cython.boundscheck(False)
@cython.cdivision(True) # Don't check for divide-by-zero.
def turbotuple_int32_6(np.int32_t x):
    return x, y
