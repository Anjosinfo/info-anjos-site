import os
import sqlite3
import subprocess
import sys

# --- CONFIGURAÇÕES ---
tipo_banco = "sqlite"          # "sqlite" ou "duckdb"
caminho_banco = "clientes.db"  # ou "clientes.duckdb"
arquivo_flask = "app.py"       # seu arquivo Flask

# --- FUNÇÃO PARA ZERAR CADASTRO ---
def zerar_cadastro():
    if tipo_banco.lower() == "sqlite":
        if not os.path.exists(caminho_banco):
            print(f"Arquivo {caminho_banco} não encontrado.")
            return
        con = sqlite3.connect(caminho_banco)
        cur = con.cursor()
        cur.execute("DELETE FROM clientes;")
        cur.execute("DELETE FROM sqlite_sequence WHERE name='clientes';")
        con.commit()
        con.close()
        print("Cadastro SQLite zerado com sucesso!")
    elif tipo_banco.lower() == "duckdb":
        import duckdb
        if not os.path.exists(caminho_banco):
            print(f"Arquivo {caminho_banco} não encontrado.")
            return
        con = duckdb.connect(caminho_banco)
        con.execute("DELETE FROM clientes;")
        con.close()
        print("Cadastro DuckDB zerado com sucesso!")
    else:
        print("Tipo de banco inválido! Use 'sqlite' ou 'duckdb'.")

# --- ZERAR CADASTRO ---
zerar_cadastro()

# --- RODAR FLASK ---
if not os.path.exists(arquivo_flask):
    print(f"Arquivo {arquivo_flask} não encontrado.")
    sys.exit(1)

# Usar pythonw.exe se quiser rodar invisível (sem terminal), ou python normal para ver logs
python_exe = sys.executable  # usa o mesmo Python que está rodando este script

print("Iniciando Flask...")
subprocess.Popen([python_exe, arquivo_flask])
print("Flask iniciado. Abra seu navegador em http://127.0.0.1:5000")
