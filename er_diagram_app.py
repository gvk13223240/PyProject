import streamlit as st
import sqlite3
from utils import extract_schema, generate_mermaid_code, parse_sql_schema, preview_table_content, infer_foreign_keys

# ---------- Helper to write DB file from SQL ----------
def create_db_from_sql(sql_text, db_path="temp_live.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(sql_text)
    conn.commit()
    conn.close()
    return db_path

# ---------- Main Streamlit app ----------
st.set_page_config(page_title="📘 SQLite ER Diagram + Live SQL Explorer", layout="wide")
st.title("📘 SQLite ER Diagram + Live SQL Explorer")

# Theme choice
theme = st.radio("Choose diagram theme", options=["Light", "Dark"], index=0)

# State to keep DB path for live sql or uploaded file
if "db_path" not in st.session_state:
    st.session_state.db_path = None

# Toggle inferred FK detection
show_inferred = st.checkbox("🔍 Show inferred foreign keys", value=True)

# --- Tabs ---
tab_upload, tab_live_sql, tab_mermaid, tab_sql_runner = st.tabs(
    ["📂 Upload DB/SQL File", "🧠 Live SQL Editor", "🛠️ Mermaid Editor", "📝 Run SQL Query"]
)

# -------- Tab 1: Upload --------
with tab_upload:
    uploaded_file = st.file_uploader("Upload SQLite (.sqlite, .db) or SQL (.sql) file", type=["sqlite", "db", "sql"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".sql"):
                sql_text = uploaded_file.read().decode("utf-8")
                db_path = create_db_from_sql(sql_text)
            else:
                db_path = f"uploaded_{uploaded_file.name}"
                with open(db_path, "wb") as f:
                    f.write(uploaded_file.read())
            st.session_state.db_path = db_path

            schema, foreign_keys = extract_schema(db_path)
            if show_inferred:
                foreign_keys += infer_foreign_keys(schema, foreign_keys)

            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")

            st.subheader("📊 ER Diagram")
            render_mermaid(mermaid_code, theme)

            st.subheader("📂 Tables & Sample Data")
            for table in schema.keys():
                st.write(f"**Table: {table}**")
                data = preview_table_content(db_path, table)
                if data:
                    st.dataframe(data)
                else:
                    st.write("No rows found.")
        except Exception as e:
            st.error(f"❌ Failed to process file: {e}")

# -------- Tab 2: Live SQL Editor --------
with tab_live_sql:
    sql_input = st.text_area("📝 Enter CREATE TABLE SQL statements", height=300, key="live_sql")
    if st.button("▶️ Build DB & Visualize", key="build_live"):
        try:
            if sql_input.strip():
                db_path = create_db_from_sql(sql_input)
                st.session_state.db_path = db_path

                schema, foreign_keys = extract_schema(db_path)
                if show_inferred:
                    foreign_keys += infer_foreign_keys(schema, foreign_keys)

                mermaid_code = generate_mermaid_code(schema, foreign_keys)

                st.subheader("📋 Mermaid Code")
                st.code(mermaid_code, language="mermaid")

                st.subheader("📊 ER Diagram")
                render_mermaid(mermaid_code, theme)

                st.subheader("📂 Tables & Sample Data")
                for table in schema.keys():
                    st.write(f"**Table: {table}**")
                    data = preview_table_content(db_path, table)
                    if data:
                        st.dataframe(data)
                    else:
                        st.write("No rows found.")
            else:
                st.warning("Please enter some CREATE TABLE SQL statements.")
        except Exception as e:
            st.error(f"❌ Error building DB: {e}")

# -------- Tab 3: Mermaid Editor --------
with tab_mermaid:
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
    custom_mermaid = st.text_area("✏️ Edit Mermaid code", value=default_code, height=300, key="mermaid_edit")

    if st.button("🔄 Render Mermaid Diagram", key="render_mermaid"):
        render_mermaid(custom_mermaid, theme)

# -------- Tab 4: SQL Runner --------
with tab_sql_runner:
    if st.session_state.db_path is None:
        st.warning("Upload or build a database first to run queries.")
    else:
        query = st.text_area("Write any SQL query here (e.g. SELECT * FROM table)", height=200)
        if st.button("▶️ Run SQL Query"):
            try:
                conn = sqlite3.connect(st.session_state.db_path)
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                conn.commit()
                conn.close()

                if rows:
                    st.dataframe([dict(zip(columns, row)) for row in rows])
                else:
                    st.write("No results to display.")
            except Exception as e:
                st.error(f"❌ Query failed: {e}")

# -------- Mermaid rendering helper --------
def render_mermaid(mermaid_code, selected_theme):
    js_theme = "default" if selected_theme == "Light" else "dark"
    mermaid_html = f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <div class="mermaid" id="mermaid-container">
    {mermaid_code}
    </div>
    <script>
    mermaid.initialize({{startOnLoad:true, theme:"{js_theme}"}});
    </script>
    """
    import streamlit.components.v1 as components
    components.html(mermaid_html, height=700, scrolling=True)
