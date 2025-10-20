from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Redirecionar para domínio principal
@app.before_request
def redirecionar_para_dominio():
    dominio_principal = "anjosinfo.com.br"
    if dominio_principal not in request.host:
        return redirect(f"https://{dominio_principal}{request.path}", code=301)

# Config banco
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri or "sqlite:///clientes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo de tabela
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cliente = Cliente(
            nome=request.form["nome"],
            email=request.form["email"],
            telefone=request.form["telefone"]
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect("/clientes")
    return render_template("index.html")

@app.route("/clientes")
def clientes():
    todos = Cliente.query.all()
    return render_template("clientes.html", clientes=todos)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
