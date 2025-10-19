import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# ← Criação do app Flask (obrigatório antes das rotas)
app = Flask(__name__)

# --- Funções e rotas abaixo ---
def buscar_clientes():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

@app.route('/')
def index():
    clientes = buscar_clientes()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']

            conn = sqlite3.connect('clientes.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                (nome, email, telefone)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Ocorreu um erro: {e}"

    return render_template('cadastro.html')

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __
== '__main__':
    app.run(debug=True)
