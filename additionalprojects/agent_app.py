import streamlit as st
import numpy as np
from tutor_agent import get_math_answer

st.set_page_config("📘 Math Tutor Bot", layout="centered")
st.title("📘 Math Tutor App")

math_topic = st.selectbox("Choose a math area:", [
    "Arithmetic", "Algebra", "Geometry", "Trigonometry", "Calculus", "Linear Algebra", "Word Problems", "Matrix Operations"
])

# General Tutor
if math_topic != "Matrix Operations":
    st.subheader("📌 Enter your question:")
    question = st.text_area("Your Question:")

    if st.button("🧠 Solve It"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Solving..."):
                result = get_math_answer(math_topic, question)
            st.success("✅ Here's your step-by-step solution:")
            st.markdown("### 🧮 Solution:")
            st.write(result)

# Matrix Operations Section
else:
    st.subheader("🧮 Matrix Operation Solver")

    operation = st.selectbox("Choose matrix operation:", [
        "Determinant", "Inverse", "Transpose", "Rank", "Trace", "Multiplication", "Eigenvalues & Eigenvectors"
    ])

    # Input for Matrix A
    st.markdown("### 🔹 Matrix A")
    rows_a = st.number_input("Rows (A)", 1, 5, 2)
    cols_a = st.number_input("Cols (A)", 1, 5, 2)

    matrix_a = []
    for i in range(rows_a):
        cols = st.columns(cols_a)
        row = [cols[j].number_input(f"A[{i+1},{j+1}]", value=0.0, key=f"a_{i}_{j}") for j in range(cols_a)]
        matrix_a.append(row)
    A = np.array(matrix_a)

    # Optional Matrix B for Multiplication
    if operation == "Multiplication":
        st.markdown("### 🔹 Matrix B")
        cols_b = st.number_input("Cols (B)", 1, 5, 2)
        matrix_b = []
        for i in range(cols_a):
            cols = st.columns(cols_b)
            row = [cols[j].number_input(f"B[{i+1},{j+1}]", value=0.0, key=f"b_{i}_{j}") for j in range(cols_b)]
            matrix_b.append(row)
        B = np.array(matrix_b)

    # Compute button
    if st.button("🔍 Compute Matrix Result"):
        try:
            if operation == "Determinant":
                if rows_a != cols_a:
                    st.error("Matrix must be square.")
                else:
                    st.success(f"Determinant: {np.linalg.det(A):.4f}")

            elif operation == "Inverse":
                if rows_a != cols_a:
                    st.error("Matrix must be square.")
                else:
                    st.write(np.linalg.inv(A))

            elif operation == "Transpose":
                st.write(A.T)

            elif operation == "Rank":
                st.success(f"Rank: {np.linalg.matrix_rank(A)}")

            elif operation == "Trace":
                if rows_a != cols_a:
                    st.error("Matrix must be square.")
                else:
                    st.success(f"Trace: {np.trace(A)}")

            elif operation == "Multiplication":
                if A.shape[1] != B.shape[0]:
                    st.error("Incompatible shapes for multiplication.")
                else:
                    st.write(np.dot(A, B))

            elif operation == "Eigenvalues & Eigenvectors":
                if rows_a != cols_a:
                    st.error("Matrix must be square.")
                else:
                    vals, vecs = np.linalg.eig(A)
                    st.write("Eigenvalues:", vals)
                    st.write("Eigenvectors:", vecs)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
