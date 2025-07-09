import streamlit as st
import sqlite3
import pandas as pd
from utils import extract_schema, generate_mermaid_code, parse_sql_schema

st.set_page_config(page_title="📘 SQLite ER Diagram Generator + Editor", layout="wide")
st.title("📘 SQLite ER Diagram Generator + Editor")

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

# -------- Tabs --------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Upload File",
    "🧠 Live SQL Editor",
    "🛠️ Manual Mermaid Editor",
    "✍️ Direct DB Editor",
    "👁️ Preview DB Structure & Content"
])

# Shared DB path variable
DB_PATH = "uploaded_db.sqlite"

# -------- Tab 1: Upload File --------
with tab1:
    uploaded_file = st.file_uploader("Upload a SQLite (.sqlite, .db) or SQL (.sql) file", type=["sqlite", "db", "sql"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".sql"):
                sql_text = uploaded_file.read().decode("utf-8")
                schema, foreign_keys = parse_sql_schema(sql_text)
                # Also save SQL to DB for editing later
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.executescript(sql_text)
                conn.commit()
                conn.close()
            else:
                with open(DB_PATH, "wb") as f:
                    f.write(uploaded_file.read())
                schema, foreign_keys = extract_schema(DB_PATH)

            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")

            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)

        except Exception as e:
            st.error(f"❌ Failed to render diagram.\n\n{e}")

# -------- Tab 2: Live SQL Editor --------
with tab2:
    sql_input = st.text_area("📝 Paste your CREATE TABLE SQL statements", height=300)
    if st.button("Run SQL"):
        if sql_input.strip():
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.executescript(sql_input)
                conn.commit()
                conn.close()

                schema, foreign_keys = extract_schema(DB_PATH)
                mermaid_code = generate_mermaid_code(schema, foreign_keys)

                st.subheader("📋 Mermaid Code")
                st.code(mermaid_code, language="mermaid")

                st.subheader("📊 ER Diagram from DB")
                render_mermaid_in_browser(mermaid_code, theme)
            except Exception as e:
                st.error(f"❌ SQL execution failed:\n{e}")

# -------- Tab 3: Manual Mermaid Editor --------
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

# -------- Tab 4: Direct DB Editor --------
with tab4:
    st.subheader("✍️ Add/Edit Tables and Foreign Keys")

    # Connect DB and get schema
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = []
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
    except:
        tables = []

    selected_table = st.selectbox("Select Table to Edit", options=["-- Create New Table --"] + tables)

    if selected_table == "-- Create New Table --":
        new_table_name = st.text_input("New Table Name")
        new_columns_text = st.text_area("Columns (one per line, e.g. `id INTEGER PRIMARY KEY`, `name TEXT`)", height=150)
        if st.button("Create Table"):
            if new_table_name.strip() and new_columns_text.strip():
                try:
                    sql_create = f"CREATE TABLE {new_table_name} (\n{new_columns_text}\n);"
                    cursor.execute(sql_create)
                    conn.commit()
                    st.success(f"Table `{new_table_name}` created!")
                except Exception as e:
                    st.error(f"Failed to create table:\n{e}")
            else:
                st.warning("Please enter a table name and columns.")
    else:
        # Show columns
        cursor.execute(f"PRAGMA table_info('{selected_table}')")
        cols = cursor.fetchall()
        df_cols = pd.DataFrame(cols, columns=["cid","name","type","notnull","dflt_value","pk"])
        st.write(f"Columns of `{selected_table}`:")
        st.dataframe(df_cols[["name", "type", "notnull", "dflt_value", "pk"]])

        # Add new column
        new_col_name = st.text_input("New Column Name")
        new_col_type = st.text_input("New Column Type (e.g. TEXT, INTEGER)")
        if st.button("Add Column"):
            if new_col_name.strip() and new_col_type.strip():
                try:
                    cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN {new_col_name} {new_col_type}")
                    conn.commit()
                    st.success(f"Column `{new_col_name}` added to `{selected_table}`!")
                except Exception as e:
                    st.error(f"Failed to add column:\n{e}")
            else:
                st.warning("Please provide column name and type.")

        # Show foreign keys
        cursor.execute(f"PRAGMA foreign_key_list('{selected_table}')")
        fks = cursor.fetchall()
        if fks:
            st.write(f"Foreign Keys in `{selected_table}`:")
            fk_df = pd.DataFrame(fks, columns=["id", "seq", "table", "from", "to", "on_update", "on_delete", "match"])
            st.dataframe(fk_df[["from", "table", "to"]])
        else:
            st.write(f"No foreign keys found in `{selected_table}`.")

    conn.close()

# -------- Tab 5: Preview DB Structure & Content --------
with tab5:
    st.subheader("👁️ Preview Database Structure and Table Contents")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
    except:
        tables = []

    selected_table_preview = st.selectbox("Select Table to Preview", options=tables)

    if selected_table_preview:
        cursor.execute(f"PRAGMA table_info('{selected_table_preview}')")
        cols = cursor.fetchall()
        st.write(f"Columns in `{selected_table_preview}`:")
        st.dataframe(pd.DataFrame(cols, columns=["cid", "name", "type", "notnull", "dflt_value", "pk"])[["name", "type"]])

        cursor.execute(f"SELECT * FROM {selected_table_preview} LIMIT 100")
        rows = cursor.fetchall()
        if rows:
            df_rows = pd.DataFrame(rows, columns=[col[0] for col in cursor.description])
            st.write(f"Sample data from `{selected_table_preview}` (up to 100 rows):")
            st.dataframe(df_rows)
        else:
            st.write(f"No data in `{selected_table_preview}`.")

    conn.close()
