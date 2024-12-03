# Função para carregar dados dos arquivos JSON
import json
import os
from datetime import datetime
from espaco import Espaco, lista_espacos
from morador import Morador,lista_moradores
from reserva import Reserva, lista_reserva





def carregar_dados():
    global lista_espacos  # Declarar global antes de qualquer uso
    try:
        # Carregar moradores
        with open('json/moradores.json', 'r', encoding='utf-8') as file:
            moradores = json.load(file)
            if isinstance(moradores, list):  # Certifique-se de que é uma lista
                for morador in moradores:
                    if isinstance(morador, dict):  # Cada item deve ser um dicionário
                        Morador(**morador)

        # Carregar espaços
        Espaco.inicializar_espacos()  # Inicializa os espaços a partir do JSON ou cria os padrões

        # Remove duplicações da lista de espaços
        espacos_unicos = {espaco.id: espaco for espaco in lista_espacos}  # Filtra duplicados pelo ID
        lista_espacos = list(espacos_unicos.values())  # Atualiza a lista global com os únicos

# Carregar reservas
        if not os.path.exists('json/reservas.json'):
            print("Arquivo 'reservas.json' não encontrado. Criando arquivo com dados padrão.")
            os.makedirs('json', exist_ok=True)
            with open('json/reservas.json', 'w', encoding='utf-8') as file:
                dados_reservas = {
                    "reservas": [],
                    "proximo_id": 1
                }
                json.dump(dados_reservas, file, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        print("Arquivo não encontrado. Criando dados padrão.")
        carregar_reservas()  # Salva reservas padrão



def validar_disponibilidade(espaco_id, data):
    """Verifica se o espaço já está reservado na data fornecida."""
    for reserva in lista_reserva:
        if reserva.espaco_id == espaco_id and reserva.data == data:
            raise ValueError("Espaço já reservado para essa data.")

def criar_reserva():
    # Recebe o ID do morador
    morador_id = input("Digite o ID do morador: ")

    # Verifica se o morador existe
    morador = next((m for m in lista_moradores if m.id == morador_id), None)
    if not morador:
        print("Morador não encontrado!")
        return

    # Recebe a data da reserva
    data_reserva = input("Digite a data da reserva (DD-MM-AA): ")

    # Exibe espaços disponíveis
    print("\nEspaços disponíveis:")
    for espaco in lista_espacos:
        print(f"{espaco.id} - {espaco.nome}")

    # Recebe a escolha do espaço
    espaco_id = int(input("Selecione o número do espaço que deseja reservar: "))

    # Verifica se o espaço existe
    espaco = next((e for e in lista_espacos if e.id == espaco_id), None)
    if not espaco:
        print("Espaço não encontrado!")
        return

    # Recebe uma descrição opcional
    descricao = input("Digite uma descrição para a reserva (opcional): ")

    # Cria a reserva
    reserva = Reserva(
        data=data_reserva,
        espaco_id=espaco.id,
        morador_id=morador.id,
        descricao=descricao if descricao else None
    )

    # Salva a reserva no arquivo JSON
    salvar_reservas(reserva)
    print("\nReserva criada e salva com sucesso!")




def salvar_reservas(reserva):
    global lista_reserva  # Tornando a variável lista_reserva acessível aqui

    # Adiciona a nova reserva à lista de reservas
    lista_reserva.append(reserva)
    print("Reserva salva com sucesso!")

     # Cria um dicionário com os dados da reserva
    reserva_dict = {      
                
        "id": reserva.id,
        "morador_id": reserva.morador_id,  # ID do morador
        "espaco_id": reserva.espaco_id,    # ID do espaço
        "data_reserva": reserva.data,      # Data da reserva
        "descricao": reserva.descricao     # Descrição (se houver)
    }

    # Verifica se o arquivo de reservas já existe
    if os.path.exists('json/reservas.json'):
        # Se o arquivo existe, carrega os dados existentes
        with open('json/reservas.json', 'r', encoding='utf-8') as file:
            dados_reservas = json.load(file)
    else:
        # Se não existe, cria uma estrutura inicial para o arquivo JSON
        dados_reservas = {"reservas": [], "proximo_id": 1}

    # Adiciona a nova reserva à lista de reservas
    dados_reservas["reservas"].append(reserva_dict)

    # Atualiza o próximo ID para o próximo item a ser adicionado
    dados_reservas["proximo_id"] = len(dados_reservas["reservas"]) + 1

    # Salva os dados atualizados no arquivo JSON
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(dados_reservas, file, indent=4, ensure_ascii=False)

    print("Reserva salva com sucesso no arquivo JSON!")
    



def carregar_reservas():
    global lista_reserva  # Acessando a lista global de reservas
    try:
        # Verificando se o arquivo JSON existe
        if os.path.exists('json/reservas.json'):
            with open('json/reservas.json', 'r', encoding='utf-8') as file:
                dados_reservas = json.load(file)

            # Atualizando o próximo ID
            Reserva.proximo_id = dados_reservas.get("proximo_id", 1)

            # Reconstruindo as reservas a partir dos dados do JSON
            for reserva_dict in dados_reservas["reservas"]:
                # Criando um objeto Reserva a partir de cada dicionário
                reserva = Reserva(
                    data=reserva_dict["data_reserva"],
                    espaco_id=reserva_dict["espaco_id"],
                    morador_id=reserva_dict["morador_id"],
                    descricao=reserva_dict.get("descricao")
                )
    except FileNotFoundError:
        print("Arquivo de reservas não encontrado, criando novo arquivo.")
        # Se o arquivo não for encontrado, você pode optar por inicializar a lista de reservas
        lista_reserva = []




# def carregar_reservas():
#     try:
#         with open("reservas.json", "r") as arquivo:
#             dados = json.load(arquivo)
#             lista_reservas = dados.get("reservas", [])
#             proximo_id = dados.get("proximo_id", 1)
#             return lista_reservas, proximo_id
#     except FileNotFoundError:
#         # Se o arquivo não existir, retorna uma lista vazia e o ID inicial como 1
#         return [], 1

# def criar_reserva():
#     """Cria uma nova reserva e salva no arquivo."""
#     try:
#         morador_id = input("Digite o ID do morador: ")
#         data_reserva = input("Digite a data da reserva (DD-MM-AA): ")

#         # Verifica se o ID do morador é válido
#         morador_encontrado = any(morador.id == morador_id for morador in lista_moradores)
#         if not morador_encontrado:
#             print("ID do morador inválido!")
#             return

#         # Obtém os espaços disponíveis para a data
#         espacos_livres = listar_espacos_livres(data_reserva)

#         if not espacos_livres:
#             print("Não há espaços disponíveis para esta data.")
#             return

#         # Exibe os espaços livres
#         print("Espaços disponíveis:")
#         for idx, espaco in enumerate(espacos_livres, start=1):
#             print(f"{idx} - ID: {espaco.id} | Nome: {espaco.nome}")

#         # O usuário escolhe o espaço a ser reservado
#         espaco_selecionado = int(input("Selecione o número do espaço que deseja reservar: ")) - 1
#         if espaco_selecionado < 0 or espaco_selecionado >= len(espacos_livres):
#             print("Seleção inválida!")
#             return

#         # Obtém os dados do espaço selecionado
#         espaco = espacos_livres[espaco_selecionado]

#         # Verifica a disponibilidade do espaço para a data selecionada
#         validar_disponibilidade(espaco.id, data_reserva)

#         # Cria a nova reserva como um objeto da classe Reserva
#         reserva = Reserva(data_reserva, espaco.id, morador_id, espaco.nome)
            

#         # Atualiza o proximo_id
#         Reserva.proximo_id = reserva.id + 1

#         # Chama a função para salvar as reservas no arquivo JSON
#         salvar_reservas()

#         print(f"Reserva criada com sucesso: {reserva}")

#     except Exception as e:
#         print(f"Erro ao criar reserva: {e}")