# utils.py
import sqlite3
import sqlparse
import re
import streamlit as st

def extract_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]

    schema = {}
    foreign_keys = []

    for table in tables:
        cursor.execute(f"PRAGMA table_info('{table}')")
        cols = cursor.fetchall()
        schema[table] = [(col[1], col[2]) for col in cols]

        cursor.execute(f"PRAGMA foreign_key_list('{table}')")
        fks = cursor.fetchall()
        for fk in fks:
            foreign_keys.append((table, fk[3], fk[2], fk[4]))

    conn.close()
    return schema, foreign_keys

def map_sqlite_type(sqlite_type: str) -> str:
    t = sqlite_type.upper()
    if "INT" in t:
        return "INTEGER"
    elif "CHAR" in t or "TEXT" in t or "CLOB" in t:
        return "NVARCHAR"
    elif "REAL" in t or "FLOA" in t or "DOUB" in t:
        return "REAL"
    elif "NUMERIC" in t or "DECIMAL" in t:
        return "NUMERIC"
    elif "DATE" in t or "TIME" in t:
        return "DATETIME"
    else:
        return "NVARCHAR"

def generate_mermaid_code(schema, foreign_keys):
    lines = ["erDiagram"]
    for table, columns in schema.items():
        lines.append(f"    {table} {{")
        for name, dtype in columns:
            lines.append(f"        {map_sqlite_type(dtype)} {name}")
        lines.append("    }")

    for from_table, from_col, to_table, to_col in foreign_keys:
        lines.append(f"    {to_table} ||--o{{ {from_table} : {from_col}")

    return "\n".join(lines)

def parse_sql_schema(sql_text):
    statements = sqlparse.split(sql_text)
    schema = {}
    foreign_keys = []

    for stmt in statements:
        stmt_clean = stmt.strip()
        if stmt_clean.upper().startswith("CREATE TABLE"):
            table_match = re.search(r'CREATE TABLE\s+\"?(\w+)\"?\s*\((.*?)\);?', stmt_clean, re.IGNORECASE | re.DOTALL)
            if table_match:
                table_name = table_match.group(1)
                column_block = table_match.group(2)

                columns = []
                for line in column_block.split(','):
                    col_def = line.strip()
                    if col_def.upper().startswith("FOREIGN KEY"):
                        fk_match = re.search(
                            r'FOREIGN KEY\s*\((\w+)\)\s*REFERENCES\s+(\w+)\s*\((\w+)\)',
                            col_def, re.IGNORECASE
                        )
                        if fk_match:
                            from_col = fk_match.group(1)
                            to_table = fk_match.group(2)
                            to_col = fk_match.group(3)
                            foreign_keys.append((table_name, from_col, to_table, to_col))
                    elif col_def and not col_def.upper().startswith("PRIMARY KEY"):
                        col_parts = col_def.split()
                        if len(col_parts) >= 2:
                            columns.append((col_parts[0], col_parts[1]))
                schema[table_name] = columns
    return schema, foreign_keys

def preview_db_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    st.subheader("📊 Table Data Preview")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        st.markdown(f"**{table}**")
        try:
            df = cursor.execute(f"SELECT * FROM {table} LIMIT 100").fetchall()
            columns = [description[0] for description in cursor.description]
            import pandas as pd
            df = pd.DataFrame(df, columns=columns)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error loading data from {table}: {e}")
    conn.close()
