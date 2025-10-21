from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# ===== INSTÂNCIA DO FLASK =====
app = Flask(__name__)

# ===== CONFIGURAÇÃO DO BANCO =====
# Usa PostgreSQL no Render, SQLite localmente
if os.getenv("DATABASE_URL"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'clientes.db')}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ===== INICIALIZAÇÃO DO SQLALCHEMY =====
db = SQLAlchemy(app)

# ===== MODELO =====
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "endereco": self.endereco,
        }

# ===== CRIAR BANCO SE NÃO EXISTIR =====
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

        novo_cliente = Cliente(
            nome=nome,
            email=email,
            telefone=telefone,
            endereco=endereco
        )
        db.session.add(novo_cliente)
        db.session.commit()

        return render_template("cadastro.html", mensagem="Cliente cadastrado com sucesso!")

    return render_template("cadastro.html")

@app.route("/clientes")
def clientes():
    todos_clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=todos_clientes)

# ===== API REST =====
@app.route("/api/clientes", methods=["GET"])
def obter_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@app.route("/api/clientes/<int:id>", methods=["DELETE"])
def excluir_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado!"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente excluído com sucesso!"})

# ===== EXECUTAR SERVIDOR =====
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
