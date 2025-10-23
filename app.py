from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
import duckdb

app = Flask(__name__)
app.secret_key = "anjosinfo123"

DB_PATH = "clientes.db"
DUCK_PATH = "clientes_duck.db"

# ======== BANCO DE DADOS ========
def conectar():
    return sqlite3.connect(DB_PATH, timeout=10)

def criar_banco():
    novo_banco = not os.path.exists(DB_PATH)
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telefone TEXT,
            endereco TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
        """)
        cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
        conexao.commit()
        if novo_banco:
            print("✅ Banco SQLite criado com usuário admin/1234")

# ======== SINCRONIZAÇÃO AUTOMÁTICA COM DUCKDB ========
def sincronizar_sqlite_duck():
    if not os.path.exists(DB_PATH):
        print("⚠️ Banco SQLite não encontrado, criando...")
        criar_banco()

    print("🔗 Sincronizando SQLite → DuckDB...")
    con = duckdb.connect(DUCK_PATH)
    con.execute(f"ATTACH DATABASE '{DB_PATH}' AS sqlite_db (TYPE SQLITE)")

    tabelas = [t[0] for t in con.execute("SHOW TABLES FROM sqlite_db").fetchall()]
    print(f"📋 Tabelas detectadas: {tabelas}")

    for tabela in tabelas:
        if tabela == "sqlite_sequence":
            continue
        print(f"➡️  Copiando tabela: {tabela}")
        con.execute(f"CREATE OR REPLACE TABLE main.{tabela} AS SELECT * FROM sqlite_db.{tabela}")

    con.close()
    print(f"✅ Sincronização concluída! Banco DuckDB atualizado: {DUCK_PATH}")

# ======== PROTEÇÃO DE LOGIN ========
@app.before_request
def verificar_login():
    rotas_publicas = ['login', 'static']
    if request.endpoint not in rotas_publicas and not session.get('logado'):
        return redirect(url_for('login'))

# ======== ROTAS ========

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"].strip()
        senha = request.form["senha"].strip()
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
            user = cursor.fetchone()
            if user:
                session["logado"] = True
                session["usuario"] = usuario
                return redirect(url_for("home"))
            else:
                flash("❌ Usuário ou senha incorretos!", "danger")
                return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/clientes")
def listar_clientes():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
    return render_template("listar.html", clientes=clientes)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        endereco = request.form["endereco"].strip()
        try:
            with conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute("""
                    INSERT INTO clientes (nome, email, telefone, endereco)
                    VALUES (?, ?, ?, ?)
                """, (nome, email, telefone, endereco))
            flash("✅ Cliente cadastrado com sucesso!", "success")
            return redirect(url_for("listar_clientes"))
        except Exception as e:
            flash(f"❌ Erro ao cadastrar cliente: {e}", "danger")
            return redirect(url_for("cadastrar_cliente"))
    return render_template("cadastrar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id=?", (id,))
        cliente = cursor.fetchone()
    if not cliente:
        flash("❌ Cliente não encontrado!", "danger")
        return redirect(url_for("listar_clientes"))

    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        telefone = request.form["telefone"].strip()
        endereco = request.form["endereco"].strip()
        try:
            with conectar() as conexao:
                cursor = conexao.cursor()
                cursor.execute("""
                    UPDATE clientes
                    SET nome=?, email=?, telefone=?, endereco=?
                    WHERE id=?
                """, (nome, email, telefone, endereco, id))
            flash("✏️ Cliente atualizado com sucesso!", "info")
            return redirect(url_for("listar_clientes"))
        except Exception as e:
            flash(f"❌ Erro ao atualizar cliente: {e}", "danger")
            return redirect(url_for("editar_cliente", id=id))

    return render_template("editar.html", cliente=cliente)

@app.route("/excluir/<int:id>")
def excluir_cliente(id):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM clientes WHERE id=?", (id,))
        flash("🗑️ Cliente excluído com sucesso!", "warning")
    except Exception as e:
        flash(f"❌ Erro ao excluir cliente: {e}", "danger")
    return redirect(url_for("listar_clientes"))

@app.route("/logout")
def logout():
    session.clear()
    flash("✅ Você saiu da conta.", "success")
    return redirect(url_for("login"))

# ======== EXECUÇÃO ========
if __name__ == "__main__":
    criar_banco()
    sincronizar_sqlite_duck()
    app.run(debug=True)
