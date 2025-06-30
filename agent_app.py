import streamlit as st
import numpy as np
from tutor_agent import get_math_answer

st.set_page_config("📘 Math Tutor Bot", layout="centered")
st.title("📘 Math Tutor App")

# Sidebar topic selection
topic = st.sidebar.selectbox("Choose a topic:", [
    "General Math Tutor",
    "Matrix Operations"
])

st.markdown("Ask a question based on the selected topic.")

# 🔷 PART 1: GENERAL MATH SOLVER
if topic == "General Math Tutor":
    st.subheader("📌 Enter your math question:")

    math_topic = st.selectbox("Choose a math area:", [
        "Arithmetic", "Algebra", "Geometry", "Trigonometry", "Calculus", "Linear Algebra", "Word Problems"
    ])
    question = st.text_area("Your Question:")

    if st.button("🧠 Solve It"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                result = get_math_answer(math_topic, question)
            st.success("✅ Here's your step-by-step solution:")
            st.markdown("### 🧮 Solution:")
            st.write(result)

# 🔷 PART 2: MATRIX OPERATIONS
elif topic == "Matrix Operations":
    st.subheader("🧮 Matrix Operations")

    operation = st.selectbox("Choose matrix operation:", [
        "Determinant", "Inverse", "Transpose", "Rank", "Trace", "Multiplication", "Eigenvalues & Eigenvectors"
    ])

    # Input Matrix A
    st.subheader("🔷 Matrix A")
    rows_a = st.number_input("Number of rows (Matrix A)", 1, 5, value=2, key="rows_a")
    cols_a = st.number_input("Number of columns (Matrix A)", 1, 5, value=2, key="cols_a")

    matrix_a = []
    for i in range(rows_a):
        row = []
        cols = st.columns(cols_a)
        for j in range(cols_a):
            val = cols[j].number_input(f"A[{i+1},{j+1}]", value=0.0, key=f"a_{i}_{j}")
            row.append(val)
        matrix_a.append(row)
    A = np.array(matrix_a)

    # Optional Matrix B
    if operation == "Multiplication":
        st.subheader("🔷 Matrix B")
        rows_b = cols_a
        cols_b = st.number_input("Number of columns (Matrix B)", 1, 5, value=2, key="cols_b")
        matrix_b = []
        for i in range(rows_b):
            row = []
            cols = st.columns(cols_b)
            for j in range(cols_b):
                val = cols[j].number_input(f"B[{i+1},{j+1}]", value=0.0, key=f"b_{i}_{j}")
                row.append(val)
            matrix_b.append(row)
        B = np.array(matrix_b)

    # Compute Button
    if st.button("🔍 Compute"):
        try:
            if operation == "Determinant":
                if rows_a != cols_a:
                    st.error("Matrix must be square for determinant.")
                else:
                    det = np.linalg.det(A)
                    st.success(f"✅ Determinant: {det:.4f}")

            elif operation == "Inverse":
                if rows_a != cols_a:
                    st.error("Matrix must be square for inverse.")
                else:
                    inv = np.linalg.inv(A)
                    st.success("✅ Inverse:")
                    st.write(inv)

            elif operation == "Transpose":
                st.success("✅ Transpose:")
                st.write(A.T)

            elif operation == "Rank":
                rank = np.linalg.matrix_rank(A)
                st.success(f"✅ Rank: {rank}")

            elif operation == "Trace":
                if rows_a != cols_a:
                    st.error("Matrix must be square for trace.")
                else:
                    tr = np.trace(A)
                    st.success(f"✅ Trace: {tr}")

            elif operation == "Multiplication":
                if A.shape[1] != B.shape[0]:
                    st.error("Matrix A's columns must match Matrix B's rows.")
                else:
                    result = np.dot(A, B)
                    st.success("✅ A × B:")
                    st.write(result)

            elif operation == "Eigenvalues & Eigenvectors":
                if rows_a != cols_a:
                    st.error("Matrix must be square for eigen decomposition.")
                else:
                    eigvals, eigvecs = np.linalg.eig(A)
                    st.success("✅ Eigenvalues:")
                    st.write(eigvals)
                    st.success("✅ Eigenvectors:")
                    st.write(eigvecs)

        except np.linalg.LinAlgError as e:
            st.error(f"❌ Matrix error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
