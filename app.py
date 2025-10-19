import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔹 Substitua aqui pela SUA URL copiada do Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://usuario:senha@host:porta/nomedobanco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 🔹 Modelo da tabela clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# 🔹 Cria as tabelas no banco do Render
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        novo_cliente = Cliente(nome=nome, telefone=telefone, email=email)
        db.session.add(novo_cliente)
        db.session.commit()

        return "Cliente cadastrado com sucesso!"
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
