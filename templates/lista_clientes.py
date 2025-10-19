<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Lista de Clientes</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Lista de Clientes</h1>
    <a href="{{ url_for('cadastro') }}">Adicionar Novo Cliente</a>
    <table>
        <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Email</th>
            <th>Telefone</th>
            <th>Ações</th>
        </tr>
        {% for cliente in clientes %}
        <tr>
            <td>{{ cliente['id'] }}</td>
            <td>{{ cliente['nome'] }}</td>
            <td>{{ cliente['email'] }}</td>
            <td>{{ cliente['telefone'] }}</td>
            <td>
                <a href="{{ url_for('excluir', id=cliente['id']) }}">Excluir</a>
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
