from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

<<<<<<< HEAD
# ===== CONFIGURAÇÃO DO BANCO =====
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'clientes.db')}"
=======
# ===== CONFIGURAÇÃO DO BANCO POSTGRESQL =====
# Usa a variável de ambiente DATABASE_URL do Render
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
>>>>>>> 15ef49a845d8e31233f8b208b9d2f499653d68f7
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

<<<<<<< HEAD
# ===== MODELO =====
class Cliente(db.Model):
=======
# ===== MODELO CLIENTE =====
class Cliente(db.Model):
    __tablename__ = "clientes"
>>>>>>> 15ef49a845d8e31233f8b208b9d2f499653d68f7
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
<<<<<<< HEAD
            "endereco": self.endereco,
        }

# ===== CRIAR BANCO SE NÃO EXISTIR =====
with app.app_context():
    db.create_all()

# ===== ROTAS =====
=======
            "endereco": self.endereco
        }

# ===== CRIAR TABELAS SE NÃO EXISTIREM =====
with app.app_context():
    db.create_all()

# ===== ROTAS DO SITE =====
>>>>>>> 15ef49a845d8e31233f8b208b9d2f499653d68f7
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/clientes")
<<<<<<< HEAD
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
=======
def clientes_page():
    return render_template("clientes.html")

@app.route("/clientes/lista")
def lista_clientes_page():
    return render_template("lista_clientes.html")

# ===== API REST =====
@app.route("/api/clientes", methods=["GET"])
def obter_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@app.route("/api/clientes", methods=["POST"])
def adicionar_cliente():
    data = request.get_json()
    if not data.get("nome") or not data.get("email"):
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

>>>>>>> 15ef49a845d8e31233f8b208b9d2f499653d68f7
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
