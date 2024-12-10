# Função para carregar dados dos arquivos JSON
import json
import os
from datetime import datetime
from espaco import Espaco, lista_espacos
from morador import lista_moradores,carregar_moradores
from reserva import Reserva, lista_reserva,carregar_reservas
from funcion_morador import buscar_morador_por_id

def carregar_dados():
    global lista_espacos,lista_moradores
    try:
        carregar_moradores()
        carregar_reservas()
        # Carregar espaços
        Espaco.inicializar_espacos()  # Inicializa os espaços a partir do JSON ou cria os padrões

    #     # Remove duplicações da lista de espaços
    #     espacos_unicos = {espaco.id: espaco for espaco in lista_espacos}  # Filtra duplicados pelo ID
    #     lista_espacos = list(espacos_unicos.values())  # Atualiza a lista global com os únicos

    # except FileNotFoundError:
    #     print("Arquivo de dados não encontrado, criando novo arquivo.")
    #     lista_moradores = []  # Se o arquivo não for encontrado, cria uma lista vazia
    #     lista_espacos = []  # Se o arquivo não for encontrado, cria uma lista vazia





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

# def validar_disponibilidade(espaco_id, data):
#     """Verifica se o espaço já está reservado na data fornecida."""
#     for reserva in lista_reserva:
#         if reserva.espaco_id == espaco_id and reserva.data == data:
#             raise ValueError("Espaço já reservado para essa data.")

def validar_disponibilidade(espaco_id, data):
    """Verifica se o espaço já está reservado na data fornecida."""
    for reserva in lista_reserva:
        if reserva.espaco_id == espaco_id and reserva.data == data:
            raise ValueError("Espaço já reservado para essa data.")
    return True

def validar_morador(morador_id):
    """Verifica se o morador existe na lista de moradores."""
    morador = next((m for m in lista_moradores if m.id == morador_id), None)
    if not morador:
        raise ValueError("Morador não encontrado.")
    return morador

def validar_espaco(espaco_id):
    """Verifica se o espaço existe na lista de espaços."""
    espaco = next((e for e in lista_espacos if e.id == espaco_id), None)
    if not espaco:
        raise ValueError("Espaço não encontrado.")
    return espaco

def validar_data(data_reserva):
    """Verifica se a data está no formato correto e é válida."""
    try:
        datetime.strptime(data_reserva, "%d-%m-%y")
        return data_reserva
    except ValueError:
        raise ValueError("Data inválida. Use o formato DD-MM-AA.")

def criar_reserva():
    try:
        # Recebe o ID do morador
        morador_id = str(input("Digite o ID do morador: ")).strip()
        if not morador_id:
            raise ValueError("O campo 'morador_id' é obrigatório!")

        # Valida o morador
        morador = validar_morador(morador_id)

        # Recebe e valida a data da reserva
        data_reserva = input("Digite a data da reserva (DD-MM-AAAA): ").strip()
        if not data_reserva:
            raise ValueError("O campo 'data' é obrigatório!")
        data_reserva = validar_data(data_reserva)

        # Exibe os espaços disponíveis
        print("\nEspaços disponíveis:")
        for espaco in lista_espacos:
            print(f"{espaco.id} - {espaco.nome}")

        # Solicita o ID do espaço ao usuário, valida e retorna o espaço
        espaco_id = input("Selecione o número do espaço que deseja reservar: ").strip()
        if not espaco_id:
            raise ValueError("O campo 'espaco_id' é obrigatório!")
        espaco = validar_espaco(int(espaco_id))
        if not espaco:
            raise ValueError("Espaço inválido!")

        # Verifica a disponibilidade do espaço
        validar_disponibilidade(int(espaco_id), data_reserva)

        # Solicita a descrição da reserva (opcional)
        descricao = input("Digite uma descrição para a reserva (opcional): ").strip().upper()
        if not descricao:
            raise ValueError("O campo 'descricao' é obrigatório!")

        # Cria a reserva
        nova_reserva = Reserva(
            morador_id=morador.id,
            data=data_reserva,
            espaco_id=espaco.id,
            descricao=descricao
        )

        # Retorna a nova reserva simulando um JSON
        print("Reserva criada com sucesso!")
        print(f"""
        "Reserva criada com sucesso!",            
    "morador_id": {nova_reserva.morador_id},
    "data": {nova_reserva.data},
    "espaco_id": {nova_reserva.espaco_id},
    "descricao": {nova_reserva.descricao}.            
        """)

    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro interno: {e}")

# def criar_reserva():
#     # Recebe o ID do morador
#     morador_id = str(input("Digite o ID do morador: "))

#     # Valida o morador
#     morador = validar_morador(morador_id)
#     if not morador:
#         print("Morador não encontrado!")
#         return

#     # Recebe e valida a data da reserva
#     data_reserva = input("Digite a data da reserva (DD-MM-AA): ")
#     try:
#         data_reserva = validar_data(data_reserva)  # Supondo que validar_data retorne a data formatada
#     except ValueError:
#         print("Data inválida!")
#         return

#     # Exibe os espaços disponíveis
#     print("\nEspaços disponíveis:")
#     for espaco in lista_espacos:
#         print(f"{espaco.id} - {espaco.nome}")

#     # Solicita o ID do espaço ao usuário, valida e retorna o espaço
#     espaco_id = int(input("Selecione o número do espaço que deseja reservar: "))
#     espaco = validar_espaco(espaco_id)
#     if not espaco:
#         print("Espaço inválido!")
#         return

#     # Solicita a descrição da reserva (opcional)
#     descricao = str(input("Digite uma descrição para a reserva (opcional): ")).upper()

#     # Cria a reserva
#     reserva = Reserva(  
#         morador_id=morador.id,
#         data=data_reserva,
#         espaco_id=espaco.id,        
#         descricao=descricao if descricao else None
#     )

#     # A função `salvar_em_json_reserva` já garante que a reserva será salva no arquivo JSON
#     print("Reserva criada com sucesso!")








# def carregar_reservas():
#     try:
#         # Carrega as reservas do arquivo JSON
#         with open('json/reservas.json', 'r', encoding='utf-8') as arquivo:
#             dados = json.load(arquivo)  # Carrega o JSON inteiro

#         # Acessa a lista de reservas dentro do JSON
#         reservas = dados.get("reservas", [])  # Retorna [] se "reservas" não existir

#         # Define o próximo ID com base no maior ID ou no próximo_id do JSON
#         if reservas:
#             Reserva.proximo_id = max(reserva['id'] for reserva in reservas) + 1
#         else:
#             Reserva.proximo_id = dados.get("proximo_id", 1)  # Fallback para 1 se não houver reservas

#         return reservas
#     except FileNotFoundError:
#         print("Erro: O arquivo reservas.json não foi encontrado.")
#         return []
#     except json.JSONDecodeError:
#         print("Erro: O conteúdo do arquivo reservas.json não é válido.")
#         return []


# def criar_reserva():
#     # Recebe o ID do morador
#     morador_id = str(input("Digite o ID do morador: "))

#     # Valida o morador
#     morador = validar_morador(morador_id)
#     if not morador:
#         print("Morador não encontrado!")
#         return

#     # Recebe e valida a data da reserva
#     data_reserva = input("Digite a data da reserva (DD-MM-AA): ")
#     try:
#         data_reserva = validar_data(data_reserva)  # Supondo que validar_data retorne a data formatada
#     except ValueError:
#         print("Data inválida!")
#         return

#     # Exibe os espaços disponíveis
#     print("\nEspaços disponíveis:")
#     for espaco in lista_espacos:
#         print(f"{espaco.id} - {espaco.nome}")


#     # Recebe e valida a escolha do espaço
#     try:
#         espaco_id = int(input("Selecione o número do espaço que deseja reservar: "))
#         espaco = validar_espaco(espaco_id)
#         if not espaco:
#             print("Espaço inválido!")
#             return
#     except ValueError:
#         print("Seleção inválida! Por favor, insira um número.")
#         return

#     #Recebe uma descrição opcional
#     descricao = input("Digite uma descrição para a reserva (opcional): ")

#     # Cria a reserva
#     reserva = Reserva(
#         data=data_reserva,
#         espaco_id=espaco.id,
#         morador_id=morador.id,
#         descricao=descricao if descricao else None
#     )

#     # A função `salvar_em_json_reserva` já garante que a reserva será salva no arquivo JSON
#     print("Reserva criada com sucesso!")




# def criar_reserva():
#     # Recebe o ID do morador
#     morador_id = input("Digite o ID do morador: ")

#     # Verifica se o morador existe
#     morador = next((m for m in lista_moradores if m.id == morador_id), None)
#     if not morador:
#         print("Morador não encontrado!")
#         return

#     # Recebe a data da reserva
#     data_reserva = input("Digite a data da reserva (DD-MM-AA): ")

#     # Exibe espaços disponíveis
#     print("\nEspaços disponíveis:")
#     for espaco in lista_espacos:
#         print(f"{espaco.id} - {espaco.nome}")

#     # Recebe a escolha do espaço
#     espaco_id = int(input("Selecione o número do espaço que deseja reservar: "))

#     # Verifica se o espaço existe
#     espaco = next((e for e in lista_espacos if e.id == espaco_id), None)
#     if not espaco:
#         print("Espaço não encontrado!")
#         return

#     # Recebe uma descrição opcional
#     descricao = input("Digite uma descrição para a reserva (opcional): ")

#     # Cria a reserva
#     reserva = Reserva(
#         data=data_reserva,
#         espaco_id=espaco.id,
#         morador_id=morador.id,
#         descricao=descricao if descricao else None
#     )
    
#     salvar_reservas()
    




# def salvar_reservas(reserva):
#     global lista_reserva  # Tornando a variável lista_reserva acessível aqui

#     # Adiciona a nova reserva à lista de reservas
#     lista_reserva.append(reserva)
#     print("Reserva salva com sucesso!")

#      # Cria um dicionário com os dados da reserva
#     reserva_dict = {      
                
#         "id": reserva.id,
#         "morador_id": reserva.morador_id,  # ID do morador
#         "espaco_id": reserva.espaco_id,    # ID do espaço
#         "data_reserva": reserva.data,      # Data da reserva
#         "descricao": reserva.descricao     # Descrição (se houver)
#     }

#     # Verifica se o arquivo de reservas já existe
#     if os.path.exists('json/reservas.json'):
#         # Se o arquivo existe, carrega os dados existentes
#         with open('json/reservas.json', 'r', encoding='utf-8') as file:
#             dados_reservas = json.load(file)
#     else:
#         # Se não existe, cria uma estrutura inicial para o arquivo JSON
#         dados_reservas = {"reservas": [], "proximo_id": 1}

#     # Adiciona a nova reserva à lista de reservas
#     dados_reservas["reservas"].append(reserva_dict)

#     # Atualiza o próximo ID para o próximo item a ser adicionado
#     dados_reservas["proximo_id"] = len(dados_reservas["reservas"]) + 1

#     # Salva os dados atualizados no arquivo JSON
#     with open('json/reservas.json', 'w', encoding='utf-8') as file:
#         json.dump(dados_reservas, file, indent=4, ensure_ascii=False)

#     print("Reserva salva com sucesso no arquivo JSON!")
    








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