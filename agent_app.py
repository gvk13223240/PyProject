import streamlit as st
from sympy import symbols, Eq, solve, sympify

st.set_page_config("📘 Math Tutor with SymPy", layout="centered")
st.title("📐 Math Tutor: System Solver")

st.markdown("Enter a system of **three linear equations** in x, y, z.")

# Input fields for equations
eq1_input = st.text_input("🔹 Equation 1 (e.g., x + y + z = 6)", "x + y + z = 6")
eq2_input = st.text_input("🔹 Equation 2 (e.g., 2*x + 3*y + 5*z = 17)", "2*x + 3*y + 5*z = 17")
eq3_input = st.text_input("🔹 Equation 3 (e.g., 4*x + 0*y + 5*z = 18)", "4*x + 0*y + 5*z = 18")

if st.button("🧠 Solve System"):
    try:
        # Define symbols
        x, y, z = symbols('x y z')
        
        # Convert input strings to SymPy equations
        eq1 = Eq(*map(sympify, eq1_input.split('=')))
        eq2 = Eq(*map(sympify, eq2_input.split('=')))
        eq3 = Eq(*map(sympify, eq3_input.split('=')))

        # Solve the system
        solution = solve([eq1, eq2, eq3], (x, y, z), dict=True)
        
        if solution:
            sol = solution[0]
            st.success("✅ Exact Solution (fractions):")
            st.write(f"x = {sol[x]}, y = {sol[y]}, z = {sol[z]}")

            st.markdown("### 🔢 Decimal Approximation:")
            st.write(f"x ≈ {float(sol[x]):.3f}, y ≈ {float(sol[y]):.3f}, z ≈ {float(sol[z]):.3f}")

        else:
            st.error("❌ No solution found. The system might be inconsistent.")

    except Exception as e:
        st.error(f"⚠️ Error parsing equations: {e}")
