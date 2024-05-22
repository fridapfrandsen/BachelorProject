from sympy import Matrix
from types import FunctionType

# Define the function to check if a value is zero modulo n
def iszero_mod_n(x, n):
    return x % n == 0

# Define the function to find a reasonable pivot
def _find_reasonable_pivot(col, iszerofunc, simpfunc, n):
    for i, val in enumerate(col):
        if not iszerofunc(val, n):  # Pass n as an argument to iszerofunc
            return i, val, True, []
    return None, None, False, []


# Define the function to simplify elements
def _simplify(x):
    return x

def _row_reduce_list_mod(mat, rows, cols, one, iszerofunc, simpfunc,
                         n, normalize_last=True, normalize=True, zero_above=True):
    """Row reduce a flat list representation of a matrix modulo n and return a tuple
    (rref_matrix, pivot_cols, swaps) where ``rref_matrix`` is a flat list,
    ``pivot_cols`` are the pivot columns and ``swaps`` are any row swaps that
    were used in the process of row reduction.

    Parameters
    ==========

    mat : list
        list of matrix elements, must be ``rows`` * ``cols`` in length

    rows, cols : integer
        number of rows and columns in flat list representation

    one : integer
        represents the value one, from ``Matrix.one``

    iszerofunc : determines if an entry can be used as a pivot

    simpfunc : used to simplify elements and test if they are
        zero if ``iszerofunc`` returns `None`

    n : integer
        modulus value for arithmetic operations

    normalize_last : indicates where all row reduction should
        happen in a fraction-free manner and then the rows are
        normalized (so that the pivots are 1), or whether
        rows should be normalized along the way (like the naive
        row reduction algorithm)

    normalize : whether pivot rows should be normalized so that
        the pivot value is 1

    zero_above : whether entries above the pivot should be zeroed.
        If ``zero_above=False``, an echelon matrix will be returned.
    """

    def get_col(i):
        return mat[i::cols]

    def row_swap(i, j):
        mat[i * cols:(i + 1) * cols], mat[j * cols:(j + 1) * cols] = \
            mat[j * cols:(j + 1) * cols], mat[i * cols:(i + 1) * cols]

    def cross_cancel(a, i, b, j):
        """Does the row op row[i] = a*row[i] - b*row[j] modulo n"""
        q = (j - i) * cols
        for p in range(i * cols, (i + 1) * cols):
            mat[p] = (a * mat[p] - b * mat[p + q]) % n

    piv_row, piv_col = 0, 0
    pivot_cols = []
    swaps = []

    # use a fraction free method to zero above and below each pivot
    while piv_col < cols and piv_row < rows:
        pivot_offset, pivot_val, \
        assumed_nonzero, newly_determined = _find_reasonable_pivot(
            get_col(piv_col)[piv_row:], iszerofunc, simpfunc, n)  # Pass n to _find_reasonable_pivot

        # _find_reasonable_pivot may have simplified some things
        # in the process.  Let's not let them go to waste
        for (offset, val) in newly_determined:
            offset += piv_row
            mat[offset * cols + piv_col] = val

        if pivot_offset is None:
            piv_col += 1
            continue

        pivot_cols.append(piv_col)
        if pivot_offset != 0:
            row_swap(piv_row, pivot_offset + piv_row)
            swaps.append((piv_row, pivot_offset + piv_row))

        # if we aren't normalizing last, we normalize
        # before we zero the other rows
        if not normalize_last:
            i, j = piv_row, piv_col
            mat[i * cols + j] = one
            for p in range(i * cols + j + 1, (i + 1) * cols):
                mat[p] = (mat[p] * pow(pivot_val, -1, n)) % n
            # after normalizing, the pivot value is 1
            pivot_val = one

        # zero above and below the pivot
        for row in range(rows):
            # don't zero our current row
            if row == piv_row:
                continue
            # don't zero above the pivot unless we're told.
            if not zero_above and row < piv_row:
                continue
            # if we're already a zero, don't do anything
            val = mat[row * cols + piv_col]
            if iszerofunc(val, n):  # Pass 'n' here
                continue

            cross_cancel(pivot_val, row, val, piv_row)
        piv_row += 1


    # normalize each row
    if normalize_last and normalize:
        for piv_i, piv_j in enumerate(pivot_cols):
            pivot_val = mat[piv_i * cols + piv_j]
            mat[piv_i * cols + piv_j] = one
            for p in range(piv_i * cols + piv_j + 1, (piv_i + 1) * cols):
                mat[p] = (mat[p] * pow(pivot_val, -1, n)) % n

    return mat, tuple(pivot_cols), tuple(swaps)


def _row_reduce_mod(M, iszerofunc, simpfunc, n, normalize_last=True,
                    normalize=True, zero_above=True):
    mat, pivot_cols, swaps = _row_reduce_list_mod(list(M), M.rows, M.cols, M.one,
                                                  iszerofunc, simpfunc, n,
                                                  normalize_last=normalize_last,
                                                  normalize=normalize, zero_above=zero_above)

    return M._new(M.rows, M.cols, mat), pivot_cols, swaps


def _rref_mod(M, iszerofunc=iszero_mod_n, simplify=False, pivots=True,
              normalize_last=True, n=2):
    simpfunc = simplify if isinstance(simplify, FunctionType) else _simplify

    mat, pivot_cols, _ = _row_reduce_mod(M, iszerofunc, simpfunc, n,
                                         normalize_last=normalize_last,
                                         normalize=True, zero_above=True)

    if pivots:
        mat = (mat, pivot_cols)

    return mat

# Define the example matrix
A = Matrix([[1, 1, 1, 1, 1, 0, 0, 0], [1, 3, 2, 6, 4, 3, 2, 6], [1, 2, 4, 1, 2, 3, 6, 5], [1, 6, 1, 6, 1, 1, 6, 1], [1, 4, 2, 1, 4, 0, 0, 0], [1, 5, 4, 6, 2, 1, 5, 4]])

# Define the modulus
n = 7

# Perform row reduction modulo n
rref_mod_result = _rref_mod(A, n=n)

# # Print the result
# print("Reduced Row Echelon Form (modulo {}):".format(n))
# print(rref_mod_result[0])
# print("Pivot columns:", rref_mod_result[1])
