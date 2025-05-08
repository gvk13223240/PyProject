import numpy as np
import streamlit as st

# Matrix Operations
def matrix_addition(A, B):
    try:
        result = np.add(A, B)
        return result
    except ValueError:
        return "Matrices must be of the same size for addition."

def matrix_multiplication(A, B):
    try:
        result = np.dot(A, B)
        return result
    except ValueError:
        return "The number of columns in A must equal the number of rows in B."

def matrix_inversion(A):
    try:
        if np.linalg.det(A) == 0:
            return "Matrix is singular and cannot be inverted."
        result = np.linalg.inv(A)
        return result
    except np.linalg.LinAlgError:
        return "Matrix inversion failed. Make sure the matrix is square and invertible."

def matrix_determinant(A):
    try:
        result = np.linalg.det(A)
        return result
    except np.linalg.LinAlgError:
        return "Matrix must be square to calculate the determinant."


# Streamlit UI Setup
st.title('Matrix Operations Calculator')
st.write("Created by - gvk13223240")
# Matrix A Input
st.subheader("Enter Matrix A (Use spaces to separate elements in a row and new lines for rows)")

# Allow users to input matrix A as a grid in the form of a string
matrix_A_input = st.text_area("Matrix A", "1 2 3\n4 5 6\n7 8 9")

# Convert the input into a NumPy array (split by lines and spaces)
try:
    matrix_A = np.array([list(map(float, row.split())) for row in matrix_A_input.split('\n')])
except ValueError:
    matrix_A = None
    st.error("Invalid matrix input. Please ensure the matrix is entered correctly.")

# Matrix B Input
st.subheader("Enter Matrix B (Use spaces to separate elements in a row and new lines for rows)")

matrix_B_input = st.text_area("Matrix B", "9 8 7\n6 5 4\n3 2 1")

# Convert the input into a NumPy array
try:
    matrix_B = np.array([list(map(float, row.split())) for row in matrix_B_input.split('\n')])
except ValueError:
    matrix_B = None
    st.error("Invalid matrix input. Please ensure the matrix is entered correctly.")

# Check if matrices are entered correctly
if matrix_A is not None and matrix_B is not None:
    st.write("Matrix A:")
    st.write(matrix_A)

    st.write("Matrix B:")
    st.write(matrix_B)

    # Operations
    operation = st.selectbox("Choose matrix operation", ["Addition", "Multiplication", "Inversion (A)", "Determinant (A)"])

    # Perform the selected operation
    if operation == "Addition":
        if matrix_A.shape == matrix_B.shape:
            result = matrix_addition(matrix_A, matrix_B)
            st.write("Result of Matrix A + Matrix B:")
            st.write(result)
        else:
            st.write("Matrices must have the same size for addition.")

    elif operation == "Multiplication":
        if matrix_A.shape[1] == matrix_B.shape[0]:
            result = matrix_multiplication(matrix_A, matrix_B)
            st.write("Result of Matrix A * Matrix B:")
            st.write(result)
        else:
            st.write("The number of columns in A must equal the number of rows in B for multiplication.")

    elif operation == "Inversion (A)":
        result = matrix_inversion(matrix_A)
        st.write("Inverse of Matrix A:")
        st.write(result)

    elif operation == "Determinant (A)":
        result = matrix_determinant(matrix_A)
        st.write("Determinant of Matrix A:")
        st.write(result)
