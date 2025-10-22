import sqlite3

# Conecta ao banco de dados existente
con = sqlite3.connect("clientes.db")
cur = con.cursor()

# Garante que a tabela de usuários existe
cur.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

# 🔐 Restaura o usuário e senha padrão
usuario = "admin"
senha = "1234"

# Remove o usuário antigo (se já existir)
cur.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))

# Adiciona novamente com a senha antiga
cur.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))

con.commit()
con.close()

print(f"✅ Usuário '{usuario}' restaurado com a senha padrão: {senha}")
