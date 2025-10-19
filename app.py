from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 🔹 Substitua pela URL do PostgreSQL fornecida pelo Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://clientes_db_t9i1_user:74EgSpCFxpXBtjufFcrhG2LKYfgEv6it@dpg-d3qktql6ubrc7381v990-a/clientes_db_t9i1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 🔹 Modelo de cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# 🔹 Cria as tabelas automaticamente (apenas na primeira vez)
with app.app_context():
    db.create_all()

# 🔹 Rotas
@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        novo_cliente = Cliente(nome=nome, telefone=telefone, email=email)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/excluir/<int:id>')
def excluir(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('index'))

# 🔹 Executar app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
