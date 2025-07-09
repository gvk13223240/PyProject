import streamlit as st
from utils import (
    extract_schema,
    generate_mermaid_code,
    parse_sql_schema,
    preview_db_tables,
    run_custom_query
)

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

# Personal branding
st.markdown("""
<div style='text-align: right; font-size: 13px; color: gray;'>
    Created by <b>Garlapati Vamshi Krishna</b> · 
    <a href="https://www.linkedin.com/in/gvk-13vk" target="_blank">LinkedIn</a>
</div>
""", unsafe_allow_html=True)

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

# ----------------------------
# 🧭 TABS
# ----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Upload File", 
    "🧠 Live SQL Editor", 
    "🛠️ Manual Mermaid Editor", 
    "🔗 Edit & Link Tables", 
    "👁️ Preview DB + Query"
])

# -------- TAB 1: File Upload --------
with tab1:
    uploaded_file = st.file_uploader("Upload a SQLite (.sqlite, .db) or SQL (.sql) file", type=["sqlite", "db", "sql"])
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
            render_mermaid_in_browser(mermaid_code, theme)

        except Exception as e:
            st.error(f"❌ Failed to render diagram.\n\n{e}")

# -------- TAB 2: Live SQL Editor --------
with tab2:
    sql_input = st.text_area("📝 Paste your CREATE TABLE SQL statements", height=300)
    if sql_input.strip():
        try:
            schema, foreign_keys = parse_sql_schema(sql_input)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)
            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")
            st.subheader("📊 ER Diagram from SQL")
            render_mermaid_in_browser(mermaid_code, theme)
        except Exception as e:
            st.error(f"❌ Failed to parse SQL.\n\n{e}")

# -------- TAB 3: Manual Mermaid Editor --------
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

# -------- TAB 4: Interactive Linking --------
with tab4:
    st.info("💡 Drag-and-drop ER editor coming soon. For now, use the Mermaid Editor tab to manually create links.")

# -------- TAB 5: Preview DB Tables & Query --------
with tab5:
    uploaded_db = st.file_uploader("Upload SQLite DB to Preview Tables", type=["db", "sqlite"], key="preview-tab")
    if uploaded_db:
        db_path = "temp_preview.sqlite"
        with open(db_path, "wb") as f:
            f.write(uploaded_db.read())

        table = st.selectbox("Select a table to view data", preview_db_tables(db_path))
        if table:
            st.dataframe(run_custom_query(db_path, f"SELECT * FROM {table} LIMIT 100"))

        st.markdown("### 🔍 Run Custom SQL Query")
        custom_query = st.text_area("Write SQL query", value="SELECT name FROM sqlite_master WHERE type='table';")
        if st.button("▶️ Run Query"):
            try:
                result = run_custom_query(db_path, custom_query)
                st.dataframe(result)
            except Exception as e:
                st.error(f"Error: {e}")
