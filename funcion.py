# Função para carregar dados dos arquivos JSON
import json
from datetime import datetime
from espaco import Espaco, lista_espacos
from morador import Morador,lista_moradores
from reserva import Reserva,lista_reservas

def carregar_dados():
    try:
        with open('json/moradores.json', 'r', encoding='utf-8') as file:
            moradores = json.load(file)
            for morador in moradores:
                Morador(**morador)

        with open('json/espacos.json', 'r', encoding='utf-8') as file:
            espacos = json.load(file)
            for espaco in espacos:
                Espaco(**espaco)

        with open('json/reservas.json', 'r', encoding='utf-8') as file:
            reservas = json.load(file)
            for reserva in reservas:
                Reserva(**reserva)

    except FileNotFoundError:
        print("Um ou mais arquivos JSON não foram encontrados.")

# Função para listar espaços livres (não reservados)
def listar_espacos_livres(data_reserva):
    """Lista espaços livres para uma data específica."""
    espacos_ocupados_na_data = {reserva.espaco_id for reserva in lista_reservas if reserva.data == data_reserva}
    espacos_livres = [espaco for espaco in lista_espacos if espaco.id not in espacos_ocupados_na_data]
    
    print(f"Espaços livres para {data_reserva}:")
    for idx, espaco in enumerate(espacos_livres, 1):
        print(f"{idx}. {espaco.tipo} - ID: {espaco.id}")
    return espacos_livres


def fazer_reserva():
    morador_id = input("Digite o ID do morador que fará a reserva: ")
    
    # Solicita a data no formato DD-MM-AA
    data_reserva = input("Digite a data da reserva (DD-MM-AA): ")
    try:
        # Valida e formata a data para DD-MM-AA
        data_reserva = datetime.strptime(data_reserva, "%d-%m-%y").strftime("%d-%m-%y")
    except ValueError:
        print("Formato de data inválido! Use DD-MM-AA.")
        return

    # Lista os espaços livres para a data fornecida
    espacos_livres = listar_espacos_livres(data_reserva)

    if espacos_livres:
        # Permite que o usuário selecione o espaço
        espaco_selecionado = int(input("Selecione o número do espaço que deseja reservar: ")) - 1
        
        if 0 <= espaco_selecionado < len(espacos_livres):
            espaco_id = espacos_livres[espaco_selecionado].id
            
            # Cria uma nova reserva para o espaço selecionado
            nova_reserva = Reserva(espaco_id, morador_id, data_reserva)
            if nova_reserva in lista_reservas:
                print("Reserva realizada com sucesso!")
            else:
                print("Reserva não foi realizada. O espaço está ocupado.")
        else:
            print("Número inválido de espaço.")
    else:
        print("Não há espaços livres disponíveis para essa data.")


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


