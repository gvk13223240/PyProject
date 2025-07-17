import streamlit as st
import sqlite3
import os
import pandas as pd
import sqlparse
import re
from utils import extract_schema, generate_mermaid_code, parse_sql_schema

# -------------------------
# 🌐 Page Configuration
# -------------------------
st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

st.markdown("""
<small style='float:right;'>Built by <a href='https://www.linkedin.com/in/gvk-13vk' target='_blank'>Garlapati Vamshi Krishna</a></small>
""", unsafe_allow_html=True)

# -------------------------
# 🎨 Theme Selection
# -------------------------
theme = st.radio("Choose diagram theme", options=["Light", "Dark"], horizontal=True)

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
    components.html(mermaid_html, height=900, scrolling=True)

# -------------------------
# 🔧 DB Initialization
# -------------------------
if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect(":memory:", check_same_thread=False)
conn = st.session_state.conn
cursor = conn.cursor()

# -------------------------
# 🧭 Tabs Layout
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Upload File", 
    "🧠 Live SQL Editor (Create/Insert/Select)", 
    "🛠️ Manual Mermaid Editor", 
    "🔍 Table Data Preview"
])

# -------------------------
# 📂 TAB 1: Upload .db/.sql
# -------------------------
with tab1:
    uploaded_file = st.file_uploader("Upload SQLite (.sqlite/.db) or SQL (.sql) file", type=["sqlite", "db", "sql"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".sql"):
                sql = uploaded_file.read().decode("utf-8")
                conn.executescript(sql)
            else:
                db_path = "temp_uploaded.sqlite"
                with open(db_path, "wb") as f:
                    f.write(uploaded_file.read())
                disk_conn = sqlite3.connect(db_path)
                for line in disk_conn.iterdump():
                    conn.execute(line)
                disk_conn.close()
                os.remove(db_path)

            schema, foreign_keys = extract_schema(conn)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")

            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# -------------------------
# 🧠 TAB 2: Live SQL Editor
# -------------------------
with tab2:
    st.write("💻 Write SQL to CREATE tables, INSERT data, or RUN SELECT queries.")
    user_sql = st.text_area("📝 SQL Editor", height=200)

    col1, col2 = st.columns([1, 1])
    with col1:
        run_btn = st.button("▶️ Run SQL")
    with col2:
        gen_btn = st.button("🪄 Generate ER Diagram")

    if run_btn:
        try:
            cursor.executescript(user_sql)
            conn.commit()
            st.success("✅ SQL executed.")
            if re.search(r"\bSELECT\b", user_sql, re.IGNORECASE):
                queries = [q.strip() for q in sqlparse.split(user_sql) if re.search(r"\bSELECT\b", q, re.IGNORECASE)]
                for i, q in enumerate(queries):
                    try:
                        df = pd.read_sql_query(q, conn)
                        st.subheader(f"📄 Result of SELECT #{i+1}")
                        st.dataframe(df, use_container_width=True)
                    except Exception as err:
                        st.warning(f"⚠️ Couldn't fetch SELECT #{i+1}: {err}")
        except Exception as e:
            st.error(f"❌ SQL Error:\n\n{e}")

    if gen_btn:
        try:
            schema, foreign_keys = extract_schema(conn)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)
            st.subheader("📋 Generated Mermaid Code")
            st.code(mermaid_code, language="mermaid")
            render_mermaid_in_browser(mermaid_code, theme)
        except Exception as e:
            st.error(f"❌ Diagram Error: {e}")

# -------------------------
# 🛠️ TAB 3: Mermaid Editor
# -------------------------
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
    mermaid_input = st.text_area("✏️ Mermaid Code Editor", value=default_mermaid, height=250)
    if st.button("🔄 Render Mermaid Diagram"):
        render_mermaid_in_browser(mermaid_input, theme)

# -------------------------
# 🔍 TAB 4: Table Data Preview
# -------------------------
with tab4:
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        if not tables:
            st.warning("⚠️ No tables found in current database.")
        else:
            for table in tables:
                with st.expander(f"📦 Table: `{table}`", expanded=False):
                    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                    st.dataframe(df, use_container_width=True)

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button(f"❌ Drop `{table}`", key=f"drop_{table}"):
                            cursor.execute(f"DROP TABLE IF EXISTS {table}")
                            conn.commit()
                            st.success(f"✅ Dropped table: {table}")
                            st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Error fetching tables: {e}")
