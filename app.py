import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Função para conectar ao banco ---
def get_db_connection():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Página inicial: mostra a lista de clientes ---
@app.route('/')
def index():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

# --- Página de cadastro ---
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = get_db_connection()
        conn.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)',
                     (nome, email, telefone))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('cadastro.html')

# --- Rota para excluir um cliente ---
@app.route('/excluir/<int:id_cliente>')
def excluir(id_cliente):
    conn = get_db_connection()
    conn.execute('DELETE FROM clientes WHERE id = ?', (id_cliente,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
