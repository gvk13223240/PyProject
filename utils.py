import sqlite3
import pandas as pd
import re

def extract_schema(db_path):
    """
    Extract tables, columns, and foreign keys from a SQLite DB file.
    Returns:
      schema: dict of {table_name: [(col_name, col_type), ...]}
      foreign_keys: list of (from_table, from_col, to_table, to_col)
    """
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
            # fk format: (id, seq, table, from, to, on_update, on_delete, match)
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
    """
    Generate Mermaid ER diagram code from schema and foreign keys.
    """
    lines = ["erDiagram"]
    for table, columns in schema.items():
        lines.append(f"    {table} {{")
        for name, dtype in columns:
            lines.append(f"        {map_sqlite_type(dtype)} {name}")
        lines.append("    }")

    for from_table, from_col, to_table, to_col in foreign_keys:
        # Mermaid syntax: PARENT ||--o{ CHILD : fk_column
        # from_table references to_table, so arrow from to_table -> from_table
        lines.append(f"    {to_table} ||--o{{ {from_table} : {from_col}")

    return "\n".join(lines)

def parse_sql_schema(sql_text):
    """
    Parse CREATE TABLE statements from SQL text.
    Returns:
      schema: dict of {table_name: [(col_name, col_type), ...]}
      foreign_keys: list of (from_table, from_col, to_table, to_col)
    """
    import sqlparse
    statements = sqlparse.split(sql_text)
    schema = {}
    foreign_keys = []

    for stmt in statements:
        stmt_clean = stmt.strip()
        if stmt_clean.upper().startswith("CREATE TABLE"):
            # extract table name and column block
            table_match = re.search(r'CREATE TABLE\s+["`]?(\w+)["`]?\s*\((.*?)\);?', stmt_clean, re.IGNORECASE | re.DOTALL)
            if table_match:
                table_name = table_match.group(1)
                column_block = table_match.group(2)

                columns = []
                for line in column_block.split(','):
                    col_def = line.strip()
                    if col_def.upper().startswith("FOREIGN KEY"):
                        fk_match = re.search(
                            r'FOREIGN KEY\s*\(["`]?(\w+)["`]?\)\s*REFERENCES\s+["`]?(\w+)["`]?\s*\(["`]?(\w+)["`]?\)', 
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

def preview_table_content(db_path, table_name, limit=10):
    """
    Return first N rows of a table as a pandas DataFrame.
    """
    conn = sqlite3.connect(db_path)
    try:
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
    except Exception:
        df = None
    finally:
        conn.close()
    return df

def infer_foreign_keys(schema, existing_fks):
    """
    Heuristic to guess foreign keys not explicitly declared:
    For each table, if it has columns named like other_table_id, and
    foreign key not already declared, add it.
    """
    guessed_fks = []
    tables = list(schema.keys())
    existing_fk_set = set(existing_fks)
    for table, columns in schema.items():
        col_names = [col[0] for col in columns]
        for col in col_names:
            if col.endswith("_id"):
                ref_table = col[:-3]  # Remove _id suffix
                if ref_table in tables:
                    candidate = (table, col, ref_table, "id")
                    if candidate not in existing_fk_set:
                        guessed_fks.append(candidate)
    return guessed_fks
