document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formCadastro");
  if (!form) return; // só roda se o formulário existir

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const telefone = document.getElementById("telefone").value.trim();
    const endereco = document.getElementById("endereco") ? document.getElementById("endereco").value.trim() : "";

    if (!nome || !email) {
      alert("Por favor, preencha o nome e o e-mail!");
      return;
    }

    try {
      const resposta = await fetch("/api/clientes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, email, telefone, endereco }),
      });

      if (resposta.ok) {
        const data = await resposta.json();
        alert(data.mensagem || "Cliente cadastrado com sucesso!");
        form.reset();
      } else {
        const erro = await resposta.json();
        alert("Erro: " + (erro.erro || "Não foi possível cadastrar."));
      }
    } catch (error) {
      console.error("Erro ao conectar com o servidor:", error);
      alert("Erro de conexão com o servidor!");
    }
  });
});
