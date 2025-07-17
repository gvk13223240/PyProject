import numpy as np
import streamlit as st

def matrix_addition(A, B):
    try:
        return np.add(A, B)
    except ValueError:
        return "Matrices must be of the same size for addition."

def matrix_multiplication(A, B):
    try:
        return np.dot(A, B)
    except ValueError:
        return "The number of columns in A must equal the number of rows in B."

def matrix_inversion(A):
    try:
        if np.linalg.det(A) == 0:
            return "Matrix is singular and cannot be inverted."
        return np.linalg.inv(A)
    except np.linalg.LinAlgError:
        return "Matrix inversion failed. Ensure the matrix is square and invertible."

def matrix_determinant(A):
    try:
        return np.linalg.det(A)
    except np.linalg.LinAlgError:
        return "Matrix must be square to calculate the determinant."

def matrix_trace(A):
    return np.trace(A)

def matrix_eigen(A):
    try:
        eigenvalues, eigenvectors = np.linalg.eig(A)
        return eigenvalues, eigenvectors
    except np.linalg.LinAlgError:
        return "Eigen decomposition failed."

def matrix_qr(A):
    try:
        Q, R = np.linalg.qr(A)
        return Q, R
    except np.linalg.LinAlgError:
        return "QR decomposition failed."

def matrix_cholesky(A):
    try:
        return np.linalg.cholesky(A)
    except np.linalg.LinAlgError:
        return "Matrix must be symmetric positive-definite for Cholesky decomposition."

def matrix_svd(A):
    try:
        U, S, Vt = np.linalg.svd(A)
        return U, S, Vt
    except np.linalg.LinAlgError:
        return "SVD failed."

def matrix_least_squares(A, B):
    try:
        solution, residuals, rank, s = np.linalg.lstsq(A, B, rcond=None)
        return solution, residuals
    except np.linalg.LinAlgError:
        return "Least squares solution failed."

st.title('Matrix Operations Calculator')
st.write("Created by - gvk13223240")

st.subheader("Enter Matrix A (space-separated, newline for rows)")
matrix_A_input = st.text_area("Matrix A", "1 2 3\n4 5 6\n7 8 9")

try:
    matrix_A = np.array([list(map(float, row.split())) for row in matrix_A_input.strip().split('\n')])
except ValueError:
    matrix_A = None
    st.error("Invalid Matrix A input.")

st.subheader("Enter Matrix B (space-separated, newline for rows)")
matrix_B_input = st.text_area("Matrix B", "9 8 7\n6 5 4\n3 2 1")

try:
    matrix_B = np.array([list(map(float, row.split())) for row in matrix_B_input.strip().split('\n')])
except ValueError:
    matrix_B = None
    st.error("Invalid Matrix B input.")

if matrix_A is not None:
    st.write("Matrix A:")
    st.write(matrix_A)

if matrix_B is not None:
    st.write("Matrix B:")
    st.write(matrix_B)

operation = st.selectbox(
    "Choose matrix operation",
    ["Addition", "Multiplication", "Inversion (A)", "Determinant (A)",
     "Trace (A)", "Eigenvalues and Eigenvectors (A)", "QR Decomposition (A)",
     "Cholesky Decomposition (A)", "SVD (A)", "Least Squares Solution (Ax = B)"]
)

if matrix_A is not None and (operation in ["Addition", "Multiplication", "Least Squares Solution (Ax = B)"] and matrix_B is None) == False:

    if operation == "Addition":
        if matrix_A.shape == matrix_B.shape:
            st.write("A + B:")
            st.write(matrix_addition(matrix_A, matrix_B))
        else:
            st.error("Addition requires A and B to be the same shape.")

    elif operation == "Multiplication":
        if matrix_A.shape[1] == matrix_B.shape[0]:
            st.write("A * B:")
            st.write(matrix_multiplication(matrix_A, matrix_B))
        else:
            st.error("A's columns must equal B's rows for multiplication.")

    elif operation == "Inversion (A)":
        st.write("Inverse of A:")
        st.write(matrix_inversion(matrix_A))

    elif operation == "Determinant (A)":
        st.write("Determinant of A:")
        st.write(matrix_determinant(matrix_A))

    elif operation == "Trace (A)":
        st.write("Trace of A:")
        st.write(matrix_trace(matrix_A))

    elif operation == "Eigenvalues and Eigenvectors (A)":
        result = matrix_eigen(matrix_A)
        if isinstance(result, tuple):
            eigenvalues, eigenvectors = result
            st.write("Eigenvalues of A:")
            st.write(eigenvalues)
            st.write("Eigenvectors of A:")
            st.write(eigenvectors)
        else:
            st.error(result)

    elif operation == "QR Decomposition (A)":
        result = matrix_qr(matrix_A)
        if isinstance(result, tuple):
            Q, R = result
            st.write("Q matrix:")
            st.write(Q)
            st.write("R matrix:")
            st.write(R)
        else:
            st.error(result)

    elif operation == "Cholesky Decomposition (A)":
        result = matrix_cholesky(matrix_A)
        if isinstance(result, str):
            st.error(result)
        else:
            st.write("Cholesky Decomposition (L):")
            st.write(result)

    elif operation == "SVD (A)":
        result = matrix_svd(matrix_A)
        if isinstance(result, tuple):
            U, S, Vt = result
            st.write("U matrix:")
            st.write(U)
            st.write("Singular values:")
            st.write(S)
            st.write("V Transposed matrix:")
            st.write(Vt)
        else:
            st.error(result)

    elif operation == "Least Squares Solution (Ax = B)":
        if matrix_A.shape[0] == matrix_B.shape[0]:
            result = matrix_least_squares(matrix_A, matrix_B)
            if isinstance(result, tuple):
                solution, residuals = result
                st.write("Solution x (minimizing ||Ax - B||):")
                st.write(solution)
                st.write("Residuals:")
                st.write(residuals)
            else:
                st.error(result)
        else:
            st.error("Rows of A must match rows of B for least squares.")
