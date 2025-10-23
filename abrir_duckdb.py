import duckdb

# Caminho do seu banco DuckDB
duckdb_path = 'clientes.duckdb'

# Conectar ao banco
con = duckdb.connect(duckdb_path)

# Listar todas as tabelas
tabelas = con.execute("SHOW TABLES").fetchall()
print("Tabelas no banco DuckDB:")
for t in tabelas:
    print("-", t[0])

# Fechar conexão
con.close()
