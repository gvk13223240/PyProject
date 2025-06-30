import streamlit as st
from tutor_agent import get_math_answer

st.set_page_config("📘 Math Tutor Bot", layout="centered")
st.title("📐 Math Tutor Bot")

st.markdown("Ask me any math question and I'll solve it step by step!")

topic = st.selectbox("Choose a math topic:", [
    "Arithmetic", "Algebra", "Geometry", "Trigonometry", "Calculus", "Word Problems"
])

question = st.text_area("📌 Enter your math question:")

if st.button("🧠 Solve It"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            result = get_math_answer(topic, question)
        
        if result.startswith("❌ Error:"):
            st.error(result)
        else:
            st.success("Here's your step-by-step solution:")
            st.markdown("### 🧮 Solution:")
            st.write(result)
