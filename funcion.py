# Função para carregar dados dos arquivos JSON
import json
from espaco import Espaco, lista_espacos
from morador import Morador,lista_moradores
from reserva import Reserva,lista_reservas

def carregar_dados():
    try:
        with open('moradores.json', 'r', encoding='utf-8') as file:
            moradores = json.load(file)
            for morador in moradores:
                Morador(**morador)

        with open('espacos.json', 'r', encoding='utf-8') as file:
            espacos = json.load(file)
            for espaco in espacos:
                Espaco(**espaco)

        with open('reservas.json', 'r', encoding='utf-8') as file:
            reservas = json.load(file)
            for reserva in reservas:
                Reserva(**reserva)

    except FileNotFoundError:
        print("Um ou mais arquivos JSON não foram encontrados.")

# Função para listar espaços livres (não reservados)
def listar_espacos_livres():
    espacos_ocupados = {reserva.espaco_id for reserva in lista_reservas}
    print(f"Espacos ocupados: {espacos_ocupados}")
    espacos_livres = [espaco for espaco in lista_espacos if espaco.id not in espacos_ocupados]
    print(f"Espacos livres encontrados: {[espaco.tipo for espaco in espacos_livres]}")
    return espacos_livres

def adicionar_morador():
    nome_morador = input("Digite o nome do morador: ")
    
    # Certificando-se de que o número do apartamento seja uma string
    apartamento = input("Digite o número do apartamento: ")
    
    # Convertendo a letra do bloco para maiúscula
    bloco = input("Digite a letra do bloco: ").upper()
    
    # Criando uma nova instância do morador
    novo_morador = Morador(nome_morador, apartamento, bloco)
    print(f"Morador {novo_morador.nome} adicionado com sucesso! ID: {novo_morador.id}")

def fazer_reserva():
    morador_id = input("Digite o ID do morador que fará a reserva: ")
    data_reserva = input("Digite a data da reserva (YYYY-MM-DD): ")
    
    # Exibir espaços livres
    print("\nEspaços livres:")
    espacos_livres = listar_espacos_livres()  # Chame a função que lista os espaços livres
    
    if espacos_livres:
        espaco_id = input("Digite o ID do espaço que deseja reservar: ")
        
        # Verifica se o espaço está livre
        if espaco_id in {espaco.id for espaco in espacos_livres}:
            nova_reserva = Reserva(morador_id, espaco_id, data_reserva)
            lista_reservas.append(nova_reserva)
            print("Reserva realizada com sucesso!")
        else:
            print("Espaço ocupado ou ID inválido.")
    else:
        print("Não há espaços livres disponíveis.")

def validar_apartamento(apartamento):
    try:
        numero = int(apartamento)
        # Verifica se o número do apartamento está nos intervalos válidos
        if (100 <= numero <= 104) or (200 <= numero <= 204) or (300 <= numero <= 304) or (400 <= numero <= 404) or (500 <= numero <= 504):
            return True
        else:
            print("Número de apartamento inválido. O apartamento deve estar entre 100-104, 200-204, 300-304, 400-404 ou 500-504.")
            return False
    except ValueError:
        print("Número de apartamento deve ser um número inteiro.")
        return False

def validar_bloco(bloco):
    if bloco.upper() in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        return True
    else:
        print("Letra do bloco inválida. O bloco deve estar entre A e G.")
        return False

def validar_nome(nome):
    if nome.strip() and nome.replace(" ", "").isalpha():  # Verifica se o nome não está vazio e contém apenas letras
        return True
    else:
        print("Nome inválido. O nome deve conter apenas letras e não pode estar vazio.")
        return False

def adicionar_morador():
    nome_morador = input("Digite o nome do morador: ")
    while not validar_nome(nome_morador):
        nome_morador = input("Digite um nome válido: ")
    
    apartamento = input("Digite o número do apartamento: ")
    while not validar_apartamento(apartamento):
        apartamento = input("Digite um número de apartamento válido: ")
    
    bloco = input("Digite a letra do bloco: ").upper()
    while not validar_bloco(bloco):
        bloco = input("Digite uma letra de bloco válida (A-G): ").upper()
    
    novo_morador = Morador(nome_morador, apartamento, bloco)
    print(f"Morador {novo_morador.nome} adicionado com sucesso! ID: {novo_morador.id}")


