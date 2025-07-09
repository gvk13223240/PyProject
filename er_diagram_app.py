import streamlit as st
import os
from utils import extract_schema, generate_mermaid_code

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

uploaded_file = st.file_uploader("Upload a SQLite (.sqlite or .db) file", type=["sqlite", "db"])

# Theme selection
theme = st.radio("🎨 Select Diagram Theme", ["default", "forest", "dark", "neutral"], horizontal=True)

def render_mermaid_in_browser(mermaid_code, theme="default"):
    mermaid_html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

    <button onclick="downloadPNG()" style="margin: 10px; padding: 8px; font-size: 16px;">⬇️ Download as PNG</button>
    <div id="mermaid-container" class="mermaid">
        {mermaid_code}
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: '{theme}'
        }});

        function downloadPNG() {{
            const container = document.getElementById("mermaid-container");
            html2canvas(container).then(canvas => {{
                const link = document.createElement('a');
                link.download = 'er_diagram.png';
                link.href = canvas.toDataURL();
                link.click();
            }});
        }}
    </script>
    """
    import streamlit.components.v1 as components
    components.html(mermaid_html, height=1000, scrolling=True)

if uploaded_file:
    db_path = "uploaded_db.sqlite"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        schema, foreign_keys = extract_schema(db_path)
        mermaid_code = generate_mermaid_code(schema, foreign_keys)

        st.subheader("📋 Mermaid Code")
        st.code(mermaid_code, language="mermaid")

        # Download .mmd file
        st.download_button("⬇️ Download Mermaid Code (.mmd)", mermaid_code, file_name="er_diagram.mmd")

        st.subheader("📊 ER Diagram")
        render_mermaid_in_browser(mermaid_code, theme)

    except Exception as e:
        st.error(f"❌ Failed to render diagram.\n\n{e}")
