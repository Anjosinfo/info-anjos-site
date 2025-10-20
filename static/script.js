const apiUrl = "/api/clientes";

async function carregarClientes() {
  const res = await fetch(apiUrl);
  const dados = await res.json();
  const tabela = document.querySelector("#tabelaClientes tbody");
  tabela.innerHTML = "";
  dados.forEach(c => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${c.id}</td>
      <td>${c.nome}</td>
      <td>${c.email}</td>
      <td>${c.telefone || ""}</td>
      <td>${c.endereco || ""}</td>
      <td>
        <button onclick="editar(${c.id}, '${c.nome}', '${c.email}', '${c.telefone || ""}', '${c.endereco || ""}')">Editar</button>
        <button onclick="deletar(${c.id})">Excluir</button>
      </td>`;
    tabela.appendChild(tr);
  });
}

document.getElementById("formCliente").addEventListener("submit", async e => {
  e.preventDefault();
  const id = document.getElementById("idCliente").value;
  const cliente = {
    nome: document.getElementById("nome").value,
    email: document.getElementById("email").value,
    telefone: document.getElementById("telefone").value,
    endereco: document.getElementById("endereco").value
  };

  const method = id ? "PUT" : "POST";
  const url = id ? `${apiUrl}/${id}` : apiUrl;

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cliente)
  });
  const data = await res.json();
  document.getElementById("mensagem").innerText = data.mensagem;
  document.getElementById("formCliente").reset();
  document.getElementById("idCliente").value = "";
  carregarClientes();
});

function editar(id, nome, email, telefone, endereco) {
  document.getElementById("idCliente").value = id;
  document.getElementById("nome").value = nome;
  document.getElementById("email").value = email;
  document.getElementById("telefone").value = telefone;
  document.getElementById("endereco").value = endereco;
}

async function deletar(id) {
  if (confirm("Excluir este cliente?")) {
    await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
    carregarClientes();
  }
}

carregarClientes();
