from flask import Flask, request, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret123'

# Criar banco
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'clientes.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    if not nome or not telefone or not email:
        return jsonify({"status":"erro","mensagem":"Preencha todos os campos"}), 400
    db_path = os.path.join(os.path.dirname(__file__), 'clientes.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)', (nome, telefone, email))
    conn.commit()
    conn.close()
    return jsonify({"status":"sucesso","mensagem":f"Cliente {nome} cadastrado com sucesso!"})

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    db_path = os.path.join(os.path.dirname(__file__), 'clientes.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return jsonify(clientes)
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Permite rodar direto com "python app.py"
if __name__ == "__main__":
    app.run(debug=True)
