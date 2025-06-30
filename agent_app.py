# app.py
import streamlit as st
from sympy import symbols, Eq, solve, sympify
from tutor_agent import get_math_answer

x, y, z = symbols('x y z')

def is_linear_system(lines):
    return (
        len(lines) == 3 and
        all('=' in line for line in lines) and
        all(any(var in line for var in ['x', 'y', 'z']) for line in lines)
    )

def solve_symbolic_system(lines):
    try:
        equations = [Eq(*map(sympify, line.split('='))) for line in lines]
        sol = solve(equations, (x, y, z), dict=True)
        if not sol:
            return "❌ No solution."
        s = sol[0]
        result = f"✅ Final Answer (exact): x = {s[x]}, y = {s[y]}, z = {s[z]}\n\n"
        result += f"Approx: x ≈ {float(s[x]):.3f}, y ≈ {float(s[y]):.3f}, z ≈ {float(s[z]):.3f}"
        return result
    except Exception as e:
        return f"⚠️ Could not parse system: {e}"

# UI
st.set_page_config("📘 Smart Math Tutor", layout="centered")
st.title("🧠 Smart Math Tutor")
st.write("#Created by - gvk13223240")
question = st.text_area("📌 Enter a math question:")

if st.button("🔍 Solve"):
    user_input = question.strip().split("\n")
    if is_linear_system(user_input):
        with st.spinner("Solving system using exact math..."):
            result = solve_symbolic_system(user_input)
    else:
        with st.spinner("Asking AI tutor..."):
            result = get_math_answer("General", question)

    st.markdown("### 🧮 Solution:")
    st.write(result)
