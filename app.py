from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco PostgreSQL (Render usa DATABASE_URL)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo da tabela clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(50))
    data_cadastro = db.Column(db.DateTime, server_default=db.func.now())

# Cria as tabelas automaticamente se não existirem
with app.app_context():
    db.create_all()

@app.route("/cadastrar-cliente", methods=["POST"])
def cadastrar_cliente():
    data = request.get_json()
    try:
        cliente = Cliente(
            nome=data["nome"],
            email=data["email"],
            telefone=data.get("telefone")
        )
        db.session.add(cliente)
        db.session.commit()
        return jsonify({
            "cliente": {
                "id": cliente.id,
                "nome": cliente.nome,
                "email": cliente.email,
                "telefone": cliente.telefone,
                "data_cadastro": cliente.data_cadastro.isoformat() if cliente.data_cadastro else None
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "API da Anjo's Info rodando com sucesso!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
