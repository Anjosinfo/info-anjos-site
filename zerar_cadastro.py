import sqlite3
import duckdb
import os

tipo_banco = "sqlite"          # "sqlite" ou "duckdb"
caminho_banco = "clientes.db"  # ou "clientes.duckdb"

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
        if not os.path.exists(caminho_banco):
            print(f"Arquivo {caminho_banco} não encontrado.")
            return
        con = duckdb.connect(caminho_banco)
        con.execute("DELETE FROM clientes;")
        con.close()
        print("Cadastro DuckDB zerado com sucesso!")
    else:
        print("Tipo de banco inválido! Use 'sqlite' ou 'duckdb'.")

if __name__ == "__main__":
    resposta = input("Deseja realmente zerar o cadastro? (s/n): ")
    if resposta.lower() == "s":
        zerar_cadastro()
    else:
        print("Cadastro mantido.")
