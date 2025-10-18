from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# Inicializa banco de clientes
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

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro
@app.route('/cadastrar-cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        if not nome or not telefone or not email:
            flash("Preencha todos os campos!", "erro")
            return redirect(url_for('cadastrar_cliente'))
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, telefone, email) VALUES (?, ?, ?)', (nome, telefone, email))
        conn.commit()
        conn.close()
        flash(f"Cliente {nome} cadastrado com sucesso!", "sucesso")
        return redirect(url_for('cadastrar_cliente'))
    return render_template('cadastro.html')

# Rodar app
if __name__ == '__main__':
    app.run(debug=True)
