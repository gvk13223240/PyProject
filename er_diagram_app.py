import streamlit as st
import os
from utils import extract_schema, generate_mermaid_code, parse_sql_schema

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

uploaded_file = st.file_uploader(
    "Upload a SQLite (.sqlite, .db) or SQL (.sql) file", 
    type=["sqlite", "db", "sql"]
)

def render_mermaid_in_browser(mermaid_code):
    mermaid_html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

    <div style="margin-bottom: 1em;">
        <button onclick="downloadPNG()">⬇️ Download PNG</button>
        <button onclick="downloadPDF()">⬇️ Download PDF</button>
    </div>

    <div id="mermaid-container" class="mermaid">
        {mermaid_code}
    </div>

    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: document.body.classList.contains('light') ? 'default' : 'dark'
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

        function downloadPDF() {{
            const container = document.getElementById("mermaid-container");
            html2canvas(container).then(canvas => {{
                const {{ jsPDF }} = window.jspdf;
                const pdf = new jsPDF();
                const imgData = canvas.toDataURL('image/png');
                const imgProps = pdf.getImageProperties(imgData);
                const pdfWidth = pdf.internal.pageSize.getWidth();
                const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
                pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
                pdf.save('er_diagram.pdf');
            }});
        }}
    </script>
    """
    import streamlit.components.v1 as components
    components.html(mermaid_html, height=1000, scrolling=True)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".sql"):
            sql_text = uploaded_file.read().decode("utf-8")
            schema, foreign_keys = parse_sql_schema(sql_text)
        else:
            db_path = "uploaded_db.sqlite"
            with open(db_path, "wb") as f:
                f.write(uploaded_file.read())
            schema, foreign_keys = extract_schema(db_path)

        mermaid_code = generate_mermaid_code(schema, foreign_keys)

        st.subheader("📋 Mermaid Code")
        st.code(mermaid_code, language="mermaid")

        st.subheader("📊 ER Diagram")
        render_mermaid_in_browser(mermaid_code)

    except Exception as e:
        st.error(f"❌ Failed to render diagram.\n\n{e}")
