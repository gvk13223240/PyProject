import streamlit as st
import sqlite3
import os
import sqlparse
import re
import pandas as pd
from utils import extract_schema, generate_mermaid_code, parse_sql_schema

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")
st.caption("Created by Garlapati Vamshi Krishna — [LinkedIn](https://www.linkedin.com/in/gvk-13vk)")

# Use in-memory DB that resets on page refresh
conn = sqlite3.connect(":memory:")

# Theme selector
theme = st.radio("Choose diagram theme", options=["Light", "Dark"], index=0)

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
    "🧠 Live SQL Editor", 
    "🛠️ Manual Mermaid Editor",
    "📋 Table Data Preview"
])

# -------- Tab 1: Upload SQLite or SQL --------
with tab1:
    uploaded_file = st.file_uploader("Upload a SQLite (.sqlite, .db) or SQL (.sql) file", type=["sqlite", "db", "sql"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".sql"):
                sql_text = uploaded_file.read().decode("utf-8")
                conn.executescript(sql_text)
                schema, foreign_keys = extract_schema(conn)
            else:
                db_path = "temp_uploaded.sqlite"
                with open(db_path, "wb") as f:
                    f.write(uploaded_file.read())
                db_conn = sqlite3.connect(db_path)
                schema, foreign_keys = extract_schema(db_conn)
                db_conn.close()

            mermaid_code = generate_mermaid_code(schema, foreign_keys)
            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")
            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

        except Exception as e:
            st.error(f"❌ Failed to process file: {e}")

# -------- Tab 2: Live SQL Editor (CREATE/INSERT/SELECT) --------
with tab2:
    st.write("Write SQL to CREATE tables, INSERT data, or RUN custom SELECT queries.")
    sql_input = st.text_area("📝 Enter SQL commands below", height=250)

    if st.button("▶️ Run SQL"):
        try:
            conn.executescript(sql_input)
            st.success("✅ SQL executed.")

            # Render ER diagram if structure changed
            schema, foreign_keys = extract_schema(conn)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)
            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

            # Try displaying SELECT results
            if re.search(r'\\bSELECT\\b', sql_input, re.IGNORECASE):
                try:
                    df = pd.read_sql_query(sql_input, conn)
                    st.subheader("📄 SQL Query Result")
                    st.dataframe(df)
                except Exception as e:
                    st.warning(f"⚠️ Query executed but failed to show result: {e}")
        except Exception as e:
            st.error(f"❌ Error executing SQL:\n\n{e}")

# -------- Tab 3: Manual Mermaid Editor --------
# -------- Tab 3: Manual Mermaid Editor --------
with tab3:
    default_mermaid = """erDiagram
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
    custom_code = st.text_area("✏️ Edit Mermaid code manually", value=default_mermaid, height=300)

    if st.button("🔄 Render Custom Mermaid"):
        render_mermaid_in_browser(custom_code, theme)

# -------- Tab 4: Table Data Preview --------
with tab4:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    if tables:
        table_selected = st.selectbox("📌 Choose a table to view data", tables)
        df = pd.read_sql_query(f"SELECT * FROM {table_selected} LIMIT 100", conn)
        st.dataframe(df)
    else:
        st.info("ℹ️ No tables available.")
