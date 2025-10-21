document.getElementById('openCadastro').addEventListener('click', function() {
    window.location.href = 'cadastro.html';
});

// Handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formCadastro');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;
            const telefone = document.getElementById('telefone').value;
            
            // Log the data (replace this with your actual save logic)
            console.log('Dados do cliente:', { nome, email, telefone });
            
            // Show success message
            alert('Cliente cadastrado com sucesso!');
            
            // Clear the form
            form.reset();
        });
    }
});
