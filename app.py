from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Lógica do formulário aqui
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        print(f"Cliente cadastrado: {nome}, {email}, {telefone}")
        return redirect(url_for('index'))
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
