# Source - https://stackoverflow.com/a/75566371
# Posted by syockit
# Retrieved 2026-04-03, License - CC BY-SA 4.0

import numpy as np

def adjugate_matrix(A):
    """
    Calculate the adjugate of a matric A
    """

    return cofactor_matrix(A).T

def cofactor_matrix(A, mod=26):
    """
    Calculate the cofactor of a matrix A
    """
    
    sel_rows = np.ones(A.shape[0], dtype=bool)
    sel_columns = np.ones(A.shape[1], dtype=bool)
    CO = np.zeros_like(A)
    sgn_row = 1

    for row in range(A.shape[0]):
        # Unselect current row
        sel_rows[row] = False
        sgn_col = 1

        for col in range(A.shape[1]):
            # Unselect current column
            sel_columns[col] = False
            # Extract submatrix
            MATij = A[sel_rows][:,sel_columns]
            CO[row, col] = (sgn_row * sgn_col * round(np.linalg.det(MATij))) % mod
            # Reselect current column
            sel_columns[col] = True
            sgn_col = -sgn_col
        sel_rows[row] = True
        # Reselect current row
        sgn_row = -sgn_row

    return CO