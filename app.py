from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ===== CONFIGURAÇÃO DO BANCO =====
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, "clientes.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "anjosinfo123"

db = SQLAlchemy(app)

# ===== MODELO =====
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

    def __repr__(self):
        return f"<Cliente {self.nome}>"

# ===== CRIAR BANCO =====
with app.app_context():
    db.create_all()

# ===== ROTAS =====
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")

        novo = Cliente(nome=nome, email=email, telefone=telefone, endereco=endereco)
        db.session.add(novo)
        db.session.commit()

        return redirect(url_for("clientes"))
    return render_template("cadastro.html")

@app.route("/clientes")
def clientes():
    lista = Cliente.query.all()
    return render_template("clientes.html", clientes=lista)

# ===== EXECUTAR =====
if __name__ == "__main__":
    app.run(debug=True)
