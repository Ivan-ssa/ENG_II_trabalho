import os,json

def listar_estrutura(caminho_base, ignorar=None, nivel=0):
    """
    Lista a estrutura de diretórios e arquivos de forma organizada.

    :param caminho_base: Diretório inicial.
    :param ignorar: Lista de nomes ou padrões a serem ignorados.
    :param nivel: Nível de recuo para exibir hierarquia.
    """
    if ignorar is None:
        ignorar = []

    try:
        # Itera sobre os itens no diretório atual
        itens = os.listdir(caminho_base)
        for item in itens:
            # Caminho completo do item
            caminho_completo = os.path.join(caminho_base, item)

            # Ignora itens indesejados
            if any(ignorar_item in caminho_completo for ignorar_item in ignorar):
                continue

            # Exibe o nome do item com indentação baseada no nível
            print("    " * nivel + f"├── {item}")

            # Caso seja um diretório, chama recursivamente
            if os.path.isdir(caminho_completo):
                listar_estrutura(caminho_completo, ignorar, nivel + 1)
    except PermissionError:
        # Ignora diretórios sem permissão
        print("    " * nivel + f"├── [SEM PERMISSÃO]")

# Configuração
caminho_base = "."  # Diretório inicial (atual)
ignorar = ["node_modules", "__tests__", ".git", ".DS_Store", "*.pyc", "*.pyo"]

# Execução
print("Estrutura do Projeto:")
listar_estrutura(caminho_base, ignorar)

