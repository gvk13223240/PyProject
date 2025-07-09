import streamlit as st
import os
from utils import extract_schema, generate_mermaid_code, save_mermaid_file, render_mermaid_to_svg

# Configure Streamlit page
st.set_page_config(page_title="📘 SQLite ER Diagram Generator")
st.title("📘 SQLite ER Diagram Generator")

# File upload
uploaded_file = st.file_uploader("Upload a SQLite (.sqlite or .db) file", type=["sqlite", "db"])

# Theme selection
theme = st.selectbox("🎨 Mermaid Diagram Theme", ["default", "dark", "forest", "neutral"])

if uploaded_file:
    db_path = "uploaded_db.sqlite"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        # Extract DB schema and generate Mermaid code
        schema, foreign_keys = extract_schema(db_path)
        mermaid_code = generate_mermaid_code(schema, foreign_keys)

        st.subheader("📋 Mermaid Code")
        st.code(mermaid_code, language="mermaid")

        # Save .mmd and render to SVG
        os.makedirs("diagrams", exist_ok=True)
        mmd_path = "diagrams/test.mmd"
        svg_path = "diagrams/test.svg"

        save_mermaid_file(mermaid_code, mmd_path)
        render_mermaid_to_svg(mmd_path, svg_path, theme=theme)

        # Read SVG content
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        st.subheader("📊 ER Diagram")
        st.markdown(svg_content, unsafe_allow_html=True)

        # Add download button
        st.download_button(
            label="⬇️ Download ER Diagram (SVG)",
            data=svg_content,
            file_name="er_diagram.svg",
            mime="image/svg+xml"
        )

    except Exception as e:
        st.error(f"❌ Failed to render diagram.\n\n{e}")
