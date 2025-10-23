import sqlite3
import duckdb

# Caminhos dos bancos
sqlite_db_path = 'clientes.db'        # Seu banco SQLite original
duckdb_db_path = 'clientes.duckdb'    # Banco DuckDB que será criado

# Conectar ao SQLite
sqlite_con = sqlite3.connect(sqlite_db_path)
sqlite_cur = sqlite_con.cursor()

# Conectar ao DuckDB
duck_con = duckdb.connect(duckdb_db_path)

# Obter lista de tabelas do SQLite
sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = [row[0] for row in sqlite_cur.fetchall()]

for tabela in tabelas:
    if tabela == 'sqlite_sequence':
        continue  # Ignorar tabela de autoincremento do SQLite

    print(f"Migrando tabela: {tabela}")

    # Obter informações das colunas e tipos
    sqlite_cur.execute(f"PRAGMA table_info({tabela});")
    colunas_info = sqlite_cur.fetchall()

    col_defs = []
    for col in colunas_info:
        nome_col = col[1]
        tipo_col = col[2].upper()

        # Ajuste de tipos para DuckDB
        if "INT" in tipo_col:
            tipo_col = "INTEGER"
        elif "CHAR" in tipo_col or "CLOB" in tipo_col or "TEXT" in tipo_col:
            tipo_col = "TEXT"
        elif "BLOB" in tipo_col:
            tipo_col = "BLOB"
        elif "REAL" in tipo_col or "FLOA" in tipo_col or "DOUB" in tipo_col:
            tipo_col = "REAL"
        else:
            tipo_col = "TEXT"  # fallback genérico

        col_defs.append(f"{nome_col} {tipo_col}")

    col_defs_sql = ", ".join(col_defs)

    # Criar tabela no DuckDB
    duck_con.execute(f"CREATE TABLE {tabela} ({col_defs_sql});")

    # Migrar dados
    sqlite_cur.execute(f"SELECT * FROM {tabela}")
    rows = sqlite_cur.fetchall()
    if rows:
        placeholders = ", ".join(["?"] * len(colunas_info))
        duck_con.executemany(
            f"INSERT INTO {tabela} VALUES ({placeholders})",
            rows
        )

print("Migração concluída com sucesso!")

# Fechar conexões
sqlite_con.close()
duck_con.close()
