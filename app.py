from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# Inicializa banco de dados
def init_db():
    conn = sqlite3.connect('clientes.db')
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
    
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)',
                   (nome, telefone, email))
    conn.commit()
    conn.close()
    return jsonify({"status":"sucesso","mensagem":f"Cliente {nome} cadastrado com sucesso!"})

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return jsonify(clientes)

if __name__ == '__main__':
    app.run(debug=True)
