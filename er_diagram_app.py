import streamlit as st
import os
from utils import extract_schema, generate_mermaid_code, save_mermaid_file
import streamlit.components.v1 as components

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

uploaded_file = st.file_uploader("Upload a SQLite (.sqlite or .db) file", type=["sqlite", "db"])

def render_mermaid_in_browser(mermaid_code):
    mermaid_html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <div class="mermaid">
    {mermaid_code}
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true }});
    </script>
    """
    components.html(mermaid_html, height=800, scrolling=True)

if uploaded_file:
    db_path = "uploaded_db.sqlite"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        schema, foreign_keys = extract_schema(db_path)
        mermaid_code = generate_mermaid_code(schema, foreign_keys)

        st.subheader("📋 Mermaid Code")
        st.code(mermaid_code, language="mermaid")

        # Save .mmd file and provide download
        mmd_path = "diagrams/diagram.mmd"
        save_mermaid_file(mermaid_code, mmd_path)
        with open(mmd_path, "rb") as f:
            st.download_button("⬇️ Download Mermaid File", f, file_name="er_diagram.mmd")

        # Render Mermaid diagram using JS in browser
        st.subheader("📊 ER Diagram")
        render_mermaid_in_browser(mermaid_code)

    except Exception as e:
        st.error(f"❌ Failed to render diagram.\n\n{e}")
