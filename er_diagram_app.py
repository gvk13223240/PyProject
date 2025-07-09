import streamlit as st
import os, re, sqlite3, pandas as pd
from utils import extract_schema, generate_mermaid_code, parse_sql_schema
import sqlparse
from pathlib import Path

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

theme = st.radio("Choose diagram theme", ["Light", "Dark"], horizontal=True)

# 🧠 Mermaid Renderer
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
    <div id="mermaid-container" class="mermaid">{mermaid_code}</div>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: "{js_theme}" }});
        function downloadPNG() {{
            html2canvas(document.getElementById("mermaid-container")).then(canvas => {{
                const link = document.createElement('a');
                link.download = 'er_diagram.png';
                link.href = canvas.toDataURL();
                link.click();
            }});
        }}
        function downloadPDF() {{
            html2canvas(document.getElementById("mermaid-container")).then(canvas => {{
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
    st.components.v1.html(mermaid_html, height=1000, scrolling=True)

# -------------------------
# 🧠 Database Session Setup
# -------------------------
DB_DIR = Path("/mnt/data/temp_dbs")
DB_DIR.mkdir(parents=True, exist_ok=True)

if "db_name" not in st.session_state:
    st.session_state.db_name = None
    st.session_state.conn = None

db_files = sorted(DB_DIR.glob("*.sqlite"))
db_names = [f.name for f in db_files]

col1, col2 = st.columns([3, 2])
with col1:
    db_selection = st.selectbox("📁 Choose active database", options=["Create new database"] + db_names)

with col2:
    if st.button("🗑️ Delete Selected DB") and st.session_state.db_name:
        try:
            os.remove(DB_DIR / st.session_state.db_name)
            st.success("Database deleted.")
            st.session_state.db_name = None
            st.session_state.conn = None
            st.experimental_rerun()
        except:
            st.error("Failed to delete DB.")

if db_selection == "Create new database":
    new_name = st.text_input("Enter name for new database", value="mydb")
    if st.button("➕ Create"):
        db_path = DB_DIR / f"{new_name}.sqlite"
        if db_path.exists():
            st.warning("File already exists.")
        else:
            conn = sqlite3.connect(db_path)
            st.session_state.conn = conn
            st.session_state.db_name = db_path.name
            st.success(f"Created {db_path.name}")
            st.experimental_rerun()
else:
    if st.session_state.db_name != db_selection:
        st.session_state.conn = sqlite3.connect(DB_DIR / db_selection)
        st.session_state.db_name = db_selection

conn = st.session_state.conn

# -------------------------
# Tabs Layout
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📂 Upload File", "🧠 Live SQL Editor", "🛠️ Mermaid Editor", "📊 Data Preview"])

# 📂 Tab 1
with tab1:
    uploaded_file = st.file_uploader("Upload a SQLite (.db/.sqlite) or SQL (.sql)", type=["sqlite", "db", "sql"])
    if uploaded_file:
        if uploaded_file.name.endswith(".sql"):
            sql = uploaded_file.read().decode("utf-8")
            schema, foreign_keys = parse_sql_schema(sql)
        else:
            db_path = "uploaded_temp.sqlite"
            with open(db_path, "wb") as f:
                f.write(uploaded_file.read())
            schema, foreign_keys = extract_schema(db_path)

        code = generate_mermaid_code(schema, foreign_keys)
        st.code(code, language="mermaid")
        render_mermaid_in_browser(code, theme)

# 🧠 Tab 2
with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        sql_input = st.text_area("SQL (CREATE / INSERT / SELECT)", height=250)
    with col2:
        if st.button("▶️ Run SQL"):
            try:
                conn.executescript(sql_input)
                st.success("SQL executed.")
            except Exception as e:
                st.error(e)

        if st.button("📈 Generate ER Diagram"):
            schema, fks = extract_schema(conn)
            code = generate_mermaid_code(schema, fks)
            st.code(code, language="mermaid")
            render_mermaid_in_browser(code, theme)

    if sql_input and re.search(r"\bSELECT\b", sql_input, re.IGNORECASE):
        try:
            last_select = [q for q in sqlparse.split(sql_input) if "SELECT" in q.upper()]
            if last_select:
                df = pd.read_sql_query(last_select[-1], conn)
                st.dataframe(df)
        except Exception as e:
            st.warning(e)

# 🛠️ Tab 3
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
    mermaid_edit = st.text_area("Edit Mermaid", default_code, height=300)
    if st.button("🔄 Render Manual Diagram"):
        render_mermaid_in_browser(mermaid_edit, theme)

# 📊 Tab 4
with tab4:
    schema, _ = extract_schema(conn)
    for table in schema.keys():
        with st.expander(f"📦 {table}"):
            st.markdown(f"**Structure:** `{[c[0] for c in schema[table]]}`")
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            st.dataframe(df)

            if st.button(f"❌ Drop `{table}`"):
                try:
                    conn.execute(f"DROP TABLE {table}")
                    st.success(f"{table} deleted.")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(e)

# 📌 Footer
st.markdown("---")
st.markdown("Made by **Garlapati Vamshi Krishna** | [LinkedIn](https://www.linkedin.com/in/gvk-13vk)")

