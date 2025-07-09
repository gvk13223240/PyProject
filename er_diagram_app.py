# er_diagram_app.py
import streamlit as st
from utils import extract_schema, generate_mermaid_code, parse_sql_schema, preview_db_data
import tempfile
import uuid

st.set_page_config(page_title="📘 SQLite ER Diagram Generator", layout="wide")
st.title("\U0001F4D8 SQLite ER Diagram Generator")

st.markdown("""
> Built by **Garlapati Vamshi Krishna** 
> [LinkedIn](https://www.linkedin.com/in/gvk-13vk)
""")

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
upload_tab, sql_tab, manual_tab, data_tab = st.tabs([
    "📂 Upload File", "🧐 Live SQL Editor", "🛠️ Manual Mermaid", "📊 View Data"])

with upload_tab:
    uploaded_file = st.file_uploader("Upload SQLite (.sqlite/.db) or SQL (.sql) file", type=["sqlite", "db", "sql"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".sql"):
                sql_text = uploaded_file.read().decode("utf-8")
                schema, foreign_keys = parse_sql_schema(sql_text)
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    db_path = tmp_file.name
                schema, foreign_keys = extract_schema(db_path)

                if st.checkbox("Show Table Data"):
                    preview_db_data(db_path)

            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")
            st.subheader("📊 ER Diagram")
            render_mermaid_in_browser(mermaid_code, theme)
        except Exception as e:
            st.error(f"Error rendering diagram: {e}")

with sql_tab:
    sql_input = st.text_area("Paste CREATE TABLE statements:", height=300)
    if sql_input.strip():
        try:
            schema, foreign_keys = parse_sql_schema(sql_input)
            mermaid_code = generate_mermaid_code(schema, foreign_keys)

            st.subheader("📋 Mermaid Code")
            st.code(mermaid_code, language="mermaid")
            st.subheader("📊 Diagram")
            render_mermaid_in_browser(mermaid_code, theme)
        except Exception as e:
            st.error(f"SQL Parse Error: {e}")

with manual_tab:
    default_code = '''erDiagram
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
    CUSTOMER ||--o{ ORDER : customer_id'''

    custom_mermaid = st.text_area("Edit Mermaid code:", value=default_code, height=300)
    if st.button("Render Diagram"):
        render_mermaid_in_browser(custom_mermaid, theme)

with data_tab:
    st.info("Upload a SQLite file in the Upload tab to view table data.")
