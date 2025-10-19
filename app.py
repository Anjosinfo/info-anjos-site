from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                       (nome, email, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
import os
