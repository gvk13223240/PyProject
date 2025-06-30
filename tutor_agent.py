import re
from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import parse_expr

# Automatically inserts '*' for implicit multiplication like 2x → 2*x
def insert_implicit_multiplication(expr):
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)       # e.g. 2x → 2*x
    expr = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', expr) # e.g. xy → x*y
    return expr

# Solve system of equations
def get_math_answer(topic, question):
    if topic.lower() != "linear algebra":
        return "❌ Only 'Linear Algebra' topic is supported for symbolic solving."

    try:
        # Split input into lines and preprocess each equation
        lines = [line.strip() for line in question.strip().split('\n') if line.strip()]
        if not lines:
            return "❌ Error: No valid equations found."

        x, y, z = symbols('x y z')
        eqs = []
        for line in lines:
            line = insert_implicit_multiplication(line)
            left, right = line.split('=')
            eq = Eq(parse_expr(left.strip()), parse_expr(right.strip()))
            eqs.append(eq)

        sol = solve(eqs, (x, y, z), dict=True)
        if not sol:
            return "❌ No solution or infinite solutions."

        sol = sol[0]  # Only one solution expected
        exact = ', '.join([f"{var} = {sol[var]}" for var in (x, y, z)])
        approx = ', '.join([f"{var} ≈ {round(sol[var].evalf(), 4)}" for var in (x, y, z)])

        return f"""
### 🧠 Solved using SymPy:
**Exact Solution:**  
{exact}

**Decimal Approximation:**  
{approx}

✅ Final Answer.
"""

    except Exception as e:
        return f"❌ An error occurred: {e}"
