import sqlite3
import duckdb
import os
import csv

# Defina o tipo de banco e caminho
# "sqlite" ou "duckdb"
tipo_banco = "duckdb"
caminho_banco = "clientes.duckdb"  # ou "clientes.db" se for SQLite

# Conectar ao banco
if tipo_banco.lower() == "sqlite":
    con = sqlite3.connect(caminho_banco)
    cursor = con.cursor()
    # Obter tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [t[0] for t in cursor.fetchall()]
else:  # DuckDB
    con = duckdb.connect(caminho_banco)
    tabelas = [t[0] for t in con.execute("SHOW TABLES").fetchall()]

print(f"Tabelas encontradas ({tipo_banco}):")
for t in tabelas:
    print("-", t)

# Função para exportar cada tabela para CSV
def exportar_csv(tabela, pasta_saida="export_csv"):
    os.makedirs(pasta_saida, exist_ok=True)
    arquivo_csv = os.path.join(pasta_saida, f"{tabela}.csv")

    if tipo_banco.lower() == "sqlite":
        cursor.execute(f"SELECT * FROM {tabela}")
        colunas = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
    else:
        rows = con.execute(f"SELECT * FROM {tabela}").fetchall()
        colunas = [desc[0] for desc in con.execute(f"DESCRIBE {tabela}").fetchall()]

    with open(arquivo_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colunas)
        writer.writerows(rows)
    print(f"Tabela {tabela} exportada para {arquivo_csv}")

# Exportar todas as tabelas
for t in tabelas:
    exportar_csv(t)

# Fechar conexão
con.close()
print("Exportação concluída com sucesso!")
