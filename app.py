from flask import Flask, request, jsonify
import psycopg2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conexão com PostgreSQL usando variável de ambiente DATABASE_URL
conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode='require')
cursor = conn.cursor()

# Criação da tabela clientes caso não exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(50),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

@app.route('/cadastrar-cliente', methods=['POST'])
def cadastrar_cliente():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    try:
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (%s,%s,%s) RETURNING id, nome, email, telefone, data_cadastro",
            (nome,email,telefone)
        )
        cliente = cursor.fetchone()
        conn.commit()
        return jsonify({"cliente":{
            "id":cliente[0],
            "nome":cliente[1],
            "email":cliente[2],
            "telefone":cliente[3],
            "data_cadastro":cliente[4].isoformat()
        }}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error":str(e)}),500

@app.route('/')
def index():
    return "API rodando!"

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
