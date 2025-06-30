# app.py
import streamlit as st
from sympy import symbols, Eq, solve, sympify
from tutor_agent import get_math_answer

st.set_page_config("📘 Hybrid Math Tutor", layout="centered")
st.title("🧠 Hybrid Math Tutor App")

# Sidebar to choose mode
mode = st.sidebar.radio("Choose Mode:", ["📐 Solve System of Equations", "🤖 Ask General Math Question"])

if mode == "📐 Solve System of Equations":
    st.header("📐 Solve a 3x3 Linear System")
    st.markdown("Enter equations involving variables `x`, `y`, and `z`.")

    eq1_input = st.text_input("🔹 Equation 1", "x + y + z = 6")
    eq2_input = st.text_input("🔹 Equation 2", "2*x + 3*y + 5*z = 17")
    eq3_input = st.text_input("🔹 Equation 3", "4*x + 0*y + 5*z = 18")

    if st.button("🧮 Solve System"):
        try:
            x, y, z = symbols('x y z')
            eq1 = Eq(*map(sympify, eq1_input.split('=')))
            eq2 = Eq(*map(sympify, eq2_input.split('=')))
            eq3 = Eq(*map(sympify, eq3_input.split('=')))
            solution = solve([eq1, eq2, eq3], (x, y, z), dict=True)

            if solution:
                sol = solution[0]
                st.success("✅ Exact Solution:")
                st.write(f"x = {sol[x]}, y = {sol[y]}, z = {sol[z]}")
                st.markdown("### 🔢 Decimal Approximation:")
                st.write(f"x ≈ {float(sol[x]):.3f}, y ≈ {float(sol[y]):.3f}, z ≈ {float(sol[z]):.3f}")
            else:
                st.error("❌ No solution found.")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

else:
    st.header("🤖 Ask a General Math Question")
    topic = st.selectbox("Choose Topic:", [
        "Arithmetic", "Algebra", "Geometry", "Trigonometry", "Calculus", "Word Problems", "Linear Algebra"
    ])
    question = st.text_area("📌 Type your math question here:")

    if st.button("🧠 Get Solution"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer = get_math_answer(topic, question)
            st.success("✅ Solution:")
            st.write(answer)
