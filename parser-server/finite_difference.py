"""
BASICS

Calculates the finite difference coefficients for a single variable
"""


from math import factorial
import numpy as np



# Number of coefficients needed
# m (int): Derivative
# n (int): Accuracy
def coefficient_number(m, n):
    return 2*((m+1)//2) -1 +n


# Finds the middle point of a list with a guaranteed odd number of elements
def oddcenter(L):
    return int(len(L)/2)

    
# Computes the actual coefficents
def finite_difference_coefficients(m, n, h):

    cn = coefficient_number(m, n)
    p = (cn - 1)//2

    m0 = np.zeros(cn)

    m0[m] = factorial(m)
    M = np.zeros((2*p+1, cn))

    for row in range(0, 2*p + 1):
        for col in range(0, 2*p+1):
            M[row][col] = (-p + col)**row

    return list((h**m)*np.linalg.solve(M, m0))


# Creates the u matrix for each derivative
# coefficients (arr) (float): Array of coefficients
# ts (int): Total size or resolution, so that the final matrix will be square and ts*ts dimensions
def partial_matrix(coefficients, ts):

    mc = oddcenter(coefficients)
    lc = len(coefficients)
    PM = np.zeros((ts, ts))
    center = coefficients[mc]

    for row in range(0, ts):

        PM[row][row] = center

        # Goes back and forth
        left_elements = min((lc-1)//2, row)
        right_elements = min((lc-1)//2, ts-row-1)

        for qq in range(1, left_elements+1):
            PM[row][row-qq] = coefficients[mc-qq]

        for hh in range(1, right_elements+1):
            PM[row][row+hh] = coefficients[mc+hh]    

    return PM
