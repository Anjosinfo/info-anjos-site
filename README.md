# cadastro_clientes.py

clientes = []

def exibir_menu():
    print("\n=== Sistema de Cadastro de Clientes ===")
    print("1 - Cadastrar novo cliente")
    print("2 - Listar clientes cadastrados")
    print("3 - Sair")

def cadastrar_cliente():
    print("\n--- Cadastro de Cliente ---")
    nome = input("Nome completo: ").strip()
    email = input("Email: ").strip()
    telefone = input("Telefone: ").strip()

    cliente = {
        "nome": nome,
        "email": email,
        "telefone": telefone
    }

    clientes.append(cliente)
    print(f"\n✅ Cliente '{nome}' cadastrado com sucesso!")

def listar_clientes():
    print("\n--- Lista de Clientes Cadastrados ---")
    if not clientes:
        print("Nenhum cliente cadastrado.")
    else:
        for i, cliente in enumerate(clientes, start=1):
            print(f"{i}. {cliente['nome']} - Email: {cliente['email']} - Telefone: {cliente['telefone']}")

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-3): ").strip()

        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            listar_clientes()
        elif opcao == '3':
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
