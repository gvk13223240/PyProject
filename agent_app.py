import streamlit as st
from tutor_agent import get_math_answer

st.set_page_config(page_title="📘 Math Tutor Bot", layout="centered")
st.title("📐 Math Tutor Bot")
st.markdown("Ask me any math question and I'll solve it step-by-step!")

topics = [
    "Arithmetic", "Algebra", "Geometry", "Trigonometry",
    "Calculus", "Word Problems", "Linear Algebra"
]

# Default to "Linear Algebra" if matrix-like text is detected
def detect_topic_from_question(q):
    if "matrix" in q.lower() or "[" in q or "]" in q:
        return "Linear Algebra"
    return st.session_state.get("topic", topics[0])

# UI elements
topic = st.selectbox("Choose a math topic:", topics, key="topic")
question = st.text_area("📌 Enter your math question:")

if st.button("🧠 Solve It"):
    if not question.strip():
        st.warning("Please enter a math question.")
    else:
        detected_topic = detect_topic_from_question(question)
        with st.spinner(f"Solving with topic: {detected_topic}..."):
            result = get_math_answer(detected_topic, question)

        st.success("Here's your step-by-step solution:")
        st.markdown("### 🧮 Solution:")
        st.write(result)
