import os,json

# def listar_estrutura(caminho_base, ignorar=None, nivel=0):
#     """
#     Lista a estrutura de diretórios e arquivos de forma organizada.

#     :param caminho_base: Diretório inicial.
#     :param ignorar: Lista de nomes ou padrões a serem ignorados.
#     :param nivel: Nível de recuo para exibir hierarquia.
#     """
#     if ignorar is None:
#         ignorar = []

#     try:
#         # Itera sobre os itens no diretório atual
#         itens = os.listdir(caminho_base)
#         for item in itens:
#             # Caminho completo do item
#             caminho_completo = os.path.join(caminho_base, item)

#             # Ignora itens indesejados
#             if any(ignorar_item in caminho_completo for ignorar_item in ignorar):
#                 continue

#             # Exibe o nome do item com indentação baseada no nível
#             print("    " * nivel + f"├── {item}")

#             # Caso seja um diretório, chama recursivamente
#             if os.path.isdir(caminho_completo):
#                 listar_estrutura(caminho_completo, ignorar, nivel + 1)
#     except PermissionError:
#         # Ignora diretórios sem permissão
#         print("    " * nivel + f"├── [SEM PERMISSÃO]")

# # Configuração
# caminho_base = "."  # Diretório inicial (atual)
# ignorar = ["venv", "__pycache__", ".git", ".DS_Store", "*.pyc", "*.pyo"]

# # Execução
# print("Estrutura do Projeto:")
# listar_estrutura(caminho_base, ignorar)
import json

def deletar_reservas_por_morador(morador_id):
    """
    Remove todas as reservas associadas ao morador_id fornecido.
    
    Args:
        morador_id (str): ID do morador cujas reservas serão deletadas.
    
    Returns:
        dict: Informações sobre o resultado da operação.
    """
    try:
        # Carrega o arquivo JSON
        with open('json/reservas.json', 'r') as arquivo:
            dados = json.load(arquivo)

        # Verifica se a chave 'reservas' existe e é uma lista
        if not isinstance(dados.get('reservas'), list):
            return {"erro": "O arquivo JSON não contém uma lista de reservas válida"}

        reservas = dados['reservas']

        # Filtra as reservas que NÃO pertencem ao morador
        novas_reservas = [reserva for reserva in reservas if reserva.get('morador_id') != morador_id]

        # Atualiza o conteúdo do JSON com as novas reservas
        dados['reservas'] = novas_reservas

        with open('json/reservas.json', 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

        # Calcula a quantidade de reservas removidas
        reservas_removidas = len(reservas) - len(novas_reservas)
        return {
            "message": "Reservas deletadas com sucesso.",
            "reservas_removidas": reservas_removidas
        }
    except FileNotFoundError:
        return {"erro": "Arquivo reservas.json não encontrado"}
    except json.JSONDecodeError:
        return {"erro": "Erro ao processar o arquivo JSON"}


