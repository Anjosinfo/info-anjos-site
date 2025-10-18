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

# ROTA PRINCIPAL — precisa estar exatamente assim 👇
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# (demais rotas: cadastrar, listar_clientes...)
