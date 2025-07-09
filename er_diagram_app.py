# Save as er_diagram_app.py
import streamlit as st
import sqlite3
import tempfile
import os
import pandas as pd
from utils import extract_schema, generate_mermaid_code, parse_sql_schema

st.set_page_config(page_title="📘 SQLite ER Diagram Generator by Garlapati Vamshi Krishna", layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>📘 SQLite ER Diagram Generator</h1>
    <p style='text-align: center;'>by <a href='https://www.linkedin.com/in/gvk-13vk' target='_blank'>Garlapati Vamshi Krishna</a></p>
""", unsafe_allow_html=True)

theme = st.radio("Choose diagram theme", options=["Light", "Dark"], index=0)

# Use in-memory SQLite DB
if 'conn' not in st.session_state:
    st.session_state.conn = sqlite3.connect(':memory:', check_same_thread=False)

def render_mermaid_in_browser(mermaid_code, selected_theme):
    js_theme = "default" if selected_theme == "Light" else "dark"
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
            theme: "{js_theme}"
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

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Upload File",
    "🧠 Live SQL + 🔍 Run SQL",
    "🛠️ Manual Mermaid Editor",
    "🔗 Table Data Preview"
])

# Upload File
with tab1:
    uploaded_file = st.file_uploader("Upload a SQLite (.sqlite, .db) or SQL (.sql) file", type=["sqlite", "db", "sql"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".sql"):
                sql_text = uploaded_file.read().decode("utf-8")
                cursor = st.session_state.conn.cursor()
                cursor.executescript(sql_text)
            else:
                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file.write(uploaded_file.read())
                tmp_file.close()
                file_conn = sqlite3.connect(tmp_file.name)
                st.session_state.conn = file_conn

            schema, foreign_keys = extract_schema(st.session_state.conn)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")

            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

        except Exception as e:
            st.error(f"❌ Failed to render diagram.\n\n{e}")

# Live SQL + Run SQL
with tab2:
    sql_text = st.text_area("📝 Enter your CREATE/INSERT/SELECT SQL statements below", height=300)
    if st.button("▶️ Execute SQL"):
        try:
            cursor = st.session_state.conn.cursor()
            cursor.executescript(sql_text)
            st.success("✅ SQL executed successfully.")

            schema, foreign_keys = extract_schema(st.session_state.conn)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")

            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)
        except Exception as e:
            st.error(f"❌ Error executing SQL:\n\n{e}")

# Manual Mermaid
with tab3:
    default_code = """erDiagram
    CUSTOMER {
        INTEGER id
        NVARCHAR name
        NVARCHAR email
    }
    ORDER {
        INTEGER id
        INTEGER customer_id
        DATETIME date
    }
    CUSTOMER ||--o{ ORDER : customer_id
    """
    custom_mermaid = st.text_area("✏️ Edit Mermaid code directly", value=default_code, height=300)
    if st.button("🔄 Render Custom Diagram"):
        render_mermaid_in_browser(custom_mermaid, theme)

# Table Data Preview
with tab4:
    try:
        cursor = st.session_state.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        if not tables:
            st.info("No tables found.")
        else:
            for table in tables:
                st.markdown(f"### 📦 {table}")
                df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 100", st.session_state.conn)
                st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Error loading tables: {e}")
