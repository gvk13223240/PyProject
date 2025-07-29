import streamlit as st
import os
import json

# === HARD-CODED LOGIN ===
USERNAME = "admin"
PASSWORD = "admin123"

# === FILE TO STORE SNIPPETS ===
DATA_FILE = "snippets.json"

# === LOAD EXISTING SNIPPETS ===
def load_snippets():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# === SAVE SNIPPETS ===
def save_snippets(snippets):
    with open(DATA_FILE, "w") as f:
        json.dump(snippets, f, indent=2)

# === MAIN APP ===
def main():
    st.title("🔐 Simple Code/Text Storage")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # === LOGIN SCREEN ===
    if not st.session_state.logged_in:
        with st.form("login"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if username == USERNAME and password == PASSWORD:
                    st.session_state.logged_in = True
                    st.success("Logged in!")
                else:
                    st.error("Invalid credentials.")
        return

    # === AFTER LOGIN ===
    snippets = load_snippets()

    st.subheader("Add New Snippet")
    new_text = st.text_area("Enter code or text")
    if st.button("Save"):
        if new_text.strip():
            snippets.append(new_text.strip())
            save_snippets(snippets)
            st.success("Saved!")
        else:
            st.warning("Nothing to save.")

    st.subheader("📄 Saved Snippets")
    if snippets:
        for i, s in enumerate(snippets[::-1], 1):
            st.code(s, language="python")  # You can change language as needed
    else:
        st.info("No snippets saved yet.")

if __name__ == "__main__":
    main()
