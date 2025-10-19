from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Página inicial (lista os clientes)
@app.route('/')
def index():
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

# Página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)", (nome, email, telefone))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
