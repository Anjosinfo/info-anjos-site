from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Criação automática da tabela
def criar_tabela():
    with sqlite3.connect("clientes.db") as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT,
                endereco TEXT
            )
        """)
criar_tabela()

# --- ROTAS DE PÁGINAS ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html')

# --- API DE CLIENTES ---
@app.route('/api/clientes', methods=['POST'])
def salvar_cliente():
    dados = request.get_json()
    with sqlite3.connect("clientes.db") as con:
        cur = con.cursor()
        cur.execute("""
            INSERT INTO clientes (nome, email, telefone, endereco)
            VALUES (?, ?, ?, ?)
        """, (dados["nome"], dados["email"], dados["telefone"], dados["endereco"]))
        con.commit()
    return jsonify({"mensagem": "✅ Cliente cadastrado com sucesso!"})

@app.route('/api/clientes', methods=['GET'])
def listar_clientes():
    with sqlite3.connect("clientes.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes ORDER BY id DESC")
        clientes = [dict(row) for row in cur.fetchall()]
    return jsonify(clientes)

@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    with sqlite3.connect("clientes.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM clientes WHERE id = ?", (id,))
        con.commit()
    return jsonify({"mensagem": "Cliente excluído com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
