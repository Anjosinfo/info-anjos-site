import duckdb
import os

sqlite_path = r"C:\Users\Jessica Anjos\Documents\info-anjos-site\clientes.db"
duck_path = r"C:\Users\Jessica Anjos\Documents\info-anjos-site\teste_duck.db"

if not os.path.exists(sqlite_path):
    raise FileNotFoundError(f"❌ Banco SQLite não encontrado em: {sqlite_path}")

print("🔗 Conectando e anexando bancos...")
con = duckdb.connect(duck_path)
con.execute(f"ATTACH DATABASE '{sqlite_path}' AS sqlite_db (TYPE SQLITE)")

# 🔍 Verifica tabelas no SQLite
tabelas = [t[0] for t in con.execute("SHOW TABLES FROM sqlite_db").fetchall()]
print(f"📋 Tabelas detectadas: {tabelas}")

# 🔁 Copia cada tabela do SQLite para o DuckDB
for tabela in tabelas:
    if tabela == "sqlite_sequence":  # ignora tabela interna
        continue
    print(f"➡️  Copiando tabela: {tabela}")
    con.execute(f"CREATE OR REPLACE TABLE main.{tabela} AS SELECT * FROM sqlite_db.{tabela}")

con.close()
print(f"✅ Sincronização concluída! Banco DuckDB criado em:\n{duck_path}")
