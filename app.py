from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ===== CONFIGURAÇÃO DO BANCO =====
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'clientes.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

@app.route("/clientes")
def clientes():
    return render_template("clientes.html")

@app.route("/clientes/lista")
def lista_clientes():
    return render_template("lista_clientes.html")

# ===== API REST =====
@app.route("/api/clientes", methods=["GET"])
def obter_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@app.route("/api/clientes", methods=["POST"])
def adicionar_cliente():
    data = request.get_json()
    novo_cliente = Cliente(
        nome=data["nome"],
        email=data["email"],
        telefone=data.get("telefone"),
        endereco=data.get("endereco")
    )
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201

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
    app.run(debug=True)
