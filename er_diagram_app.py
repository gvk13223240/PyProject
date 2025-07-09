import streamlit as st
import sqlite3
import pandas as pd
from utils import extract_schema, generate_mermaid_code, parse_sql_schema

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("📘 SQLite ER Diagram Generator")

# Your personal branding
st.sidebar.markdown(
    """
    <div style="font-size:14px; margin-bottom:20px;">
        Created by <b>Garlapati Vamshi Krishna</b><br/>
        <a href="https://www.linkedin.com/in/gvk-13vk" target="_blank">LinkedIn Profile</a>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a SQLite (.sqlite, .db) or SQL (.sql) file", 
    type=["sqlite", "db", "sql"]
)

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

mode = st.sidebar.radio("Select mode", ["Visualize ER Diagram", "Edit Relationships", "Preview Data"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".sql"):
            sql_text = uploaded_file.read().decode("utf-8")
            schema, foreign_keys = parse_sql_schema(sql_text)
            conn = None
        else:
            db_path = "uploaded_db.sqlite"
            with open(db_path, "wb") as f:
                f.write(uploaded_file.read())
            schema, foreign_keys = extract_schema(db_path)
            conn = sqlite3.connect(db_path)

        # Use session state to keep track of FKs added manually
        if "foreign_keys" not in st.session_state:
            st.session_state.foreign_keys = foreign_keys.copy()
        else:
            # Reset on new upload (optional)
            if st.session_state.get("last_uploaded") != uploaded_file.name:
                st.session_state.foreign_keys = foreign_keys.copy()
        st.session_state.last_uploaded = uploaded_file.name

        if mode == "Visualize ER Diagram":
            mermaid_code = generate_mermaid_code(schema, st.session_state.foreign_keys)
            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")
            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

        elif mode == "Edit Relationships":
            st.subheader("✏️ Add/Edit Foreign Key Relationships")

            tables = list(schema.keys())
            from_table = st.selectbox("From Table (child table)", tables)
            from_col = st.selectbox("From Column", [col for col, _ in schema[from_table]])
            to_table = st.selectbox("To Table (parent table)", tables)
            to_col = st.selectbox("To Column", [col for col, _ in schema[to_table]])

            if st.button("Add Relationship"):
                # Avoid duplicates
                new_fk = (from_table, from_col, to_table, to_col)
                if new_fk not in st.session_state.foreign_keys:
                    st.session_state.foreign_keys.append(new_fk)
                    st.success(f"Added FK: {from_table}.{from_col} → {to_table}.{to_col}")
                else:
                    st.warning("This foreign key relationship already exists.")

            mermaid_code = generate_mermaid_code(schema, st.session_state.foreign_keys)
            st.subheader("Updated ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

        elif mode == "Preview Data":
            st.subheader("📚 Database Structure & Sample Data")
            for table in schema:
                st.write(f"### Table: {table}")
                cols = [f"{col} ({dtype})" for col, dtype in schema[table]]
                st.write("Columns:", ", ".join(cols))
                if conn:
                    try:
                        df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
                        st.dataframe(df)
                    except Exception as e:
                        st.write(f"Could not load data: {e}")
                else:
                    st.write("No data preview available for SQL file upload.")

    except Exception as e:
        st.error(f"❌ Failed to process file.\n\n{e}")
else:
    st.info("Please upload a SQLite or SQL file to begin.")
