import sqlite3
import os
import subprocess

def extract_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all non-system tables
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
            foreign_keys.append((table, fk[3], fk[2], fk[4]))  # from_table, from_col, to_table, to_col

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

def save_mermaid_file(mermaid_code, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(mermaid_code)

def render_mermaid_to_svg(input_path, output_path, theme="default"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        "C:\\Users\\gvk13\\AppData\\Roaming\\npm\\mmdc.cmd",                      # Mermaid CLI command
        "-i", input_path,
        "-o", output_path,
        "--theme", theme             # Apply selected theme
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Mermaid CLI failed: {result.stderr.strip()}")

# C:\\Users\\gvk13\\AppData\\Roaming\\npm\\mmdc.cmd