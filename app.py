from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ===== CONFIGURAÇÃO DO BANCO =====
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'clientes.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ===== MODELO CLIENTE =====
class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ===== ROTAS =====
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")

        novo_cliente = Cliente(nome=nome, email=email, telefone=telefone, endereco=endereco)
        db.session.add(novo_cliente)
        db.session.commit()

        return render_template("cadastro.html", mensagem="Cliente cadastrado com sucesso!")
    return render_template("cadastro.html")

@app.route("/clientes")
def clientes_page():
    return render_template("clientes.html")

@app.route("/clientes/lista")
def lista_clientes_page():
    clientes = Cliente.query.all()
    return render_template("lista_clientes.html", clientes=clientes)

if __name__ == "__main__":
    app.run(debug=True)
