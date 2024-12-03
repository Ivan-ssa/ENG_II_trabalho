# Função para carregar dados dos arquivos JSON
import json
from datetime import datetime
from espaco import Espaco, lista_espacos
from morador import Morador,lista_moradores
from reserva import Reserva,lista_reserva


def buscar_morador_por_id(id_morador):
    if not Morador.validar_id(id_morador):
        print("ID inválido. O formato deve ser três números seguidos de uma letra maiúscula (exemplo: 101A).")
        return None

    for morador in lista_moradores:
        if morador.id == id_morador:
            return morador

    print("Morador não encontrado.")
    return None


def validar_nome(nome):
    if nome.strip() and nome.replace(" ", "").isalpha():  # Verifica se o nome não está vazio e contém apenas letras
        return True
    else:
        print("Nome inválido. O nome deve conter apenas letras e não pode estar vazio.")
        return False

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

def adicionar_morador():
    while True:
        nome = input("Digite o nome do morador: ").strip()
        if validar_nome(nome):
            break

    while True:
        apartamento = input("Digite o número do apartamento: ").strip()
        if validar_apartamento(apartamento):
            apartamento = int(apartamento)
            break

    while True:
        bloco = input("Digite a letra do bloco: ").strip().upper()
        if validar_bloco(bloco):
            break

    id_morador = f"{apartamento}{bloco}"
    if any(morador.id == id_morador for morador in lista_moradores):
        print(f"Já existe um morador com o ID {id_morador}.")
        return

    try:
        novo_morador = Morador(nome, apartamento, bloco)
        print(f"Morador {novo_morador.nome} adicionado com sucesso! ID: {novo_morador.id}")
    except ValueError as e:
        print(f"Erro: {e}")



def remover_reservas_por_morador(morador_id):
    global lista_reservas
    lista_reservas = [reserva for reserva in lista_reservas if reserva.morador_id != morador_id]
    Reserva.salvar_todas_reservas()
    print(f"Todas as reservas associadas ao morador ID {morador_id} foram removidas.")

def deletar_morador(morador_id):
    global lista_moradores
    morador_existe = any(morador.id == morador_id for morador in lista_moradores)
    if not morador_existe:
        print("Morador não encontrado. Não é possível deletar.")
        return

    lista_moradores = [morador for morador in lista_moradores if morador.id != morador_id]
    Morador.salvar_todos_moradores()  # Atualiza o arquivo de moradores
    remover_reservas_por_morador(morador_id)  # Remove reservas do morador
    print(f"Morador ID {morador_id} e suas reservas foram removidos com sucesso.")



def deletar_morador(morador_id):
    if not Morador.validar_id(morador_id):
        print("ID inválido. O formato deve ser três números seguidos de uma letra maiúscula (exemplo: 101A).")
        return

    global lista_moradores
    morador_existe = any(morador.id == morador_id for morador in lista_moradores)
    if not morador_existe:
        print("Morador não encontrado.")
        return

    lista_moradores = [morador for morador in lista_moradores if morador.id != morador_id]
    Morador.salvar_todos_moradores()
    remover_reservas_por_morador(morador_id)
    print(f"Morador com ID {morador_id} e suas reservas foram removidos com sucesso.")


# def deletar_morador_e_reservas():
#     morador_id = input("Digite o ID do morador que deseja deletar: ")
#     morador_existe = any(morador.id == morador_id for morador in lista_moradores)
    
#     if not morador_existe:
#         print("Morador não encontrado. Verifique o ID e tente novamente.")
#         return

#     # Remove o morador da lista
#     lista_moradores[:] = [morador for morador in lista_moradores if morador.id != morador_id]
#     Morador.salvar_todos_moradores()  # Salva a lista atualizada no arquivo JSON

#     # Remove as reservas associadas ao morador
#     lista_reservas[:] = [reserva for reserva in lista_reservas if reserva.morador_id != morador_id]
#     Reserva.salvar_todas_reservas()  # Salva a lista atualizada no arquivo JSON

#     print(f"Morador com ID {morador_id} e suas reservas foram deletados com sucesso.")




#def adicionar_morador():
#     """
#     Solicita os dados do morador e realiza as validações.
#     """
#     while True:
#         nome = input("Digite o nome do morador: ").strip()
#         if validar_nome(nome):
#             break

#     while True:
#         apartamento = input("Digite o número do apartamento: ").strip()
#         if validar_apartamento(apartamento):
#             apartamento = int(apartamento)  # Converte para inteiro após validação
#             break

#     while True:
#         bloco = input("Digite a letra do bloco: ").strip().upper()
#         if validar_bloco(bloco):
#             break

#     # Verifica duplicidade de apartamento e bloco
#     for morador in lista_moradores:
#         if morador.apartamento == apartamento and morador.bloco == bloco:
#             print(f"Já existe um morador cadastrado no apartamento {apartamento}, bloco {bloco} (Nome: {morador.nome}).")
#             opcao = input("Deseja sobrescrever o cadastro? (s/n): ").lower()
#             if opcao == 's':
#                 lista_moradores.remove(morador)  # Remove o cadastro antigo
#                 break  # Sai do loop para cadastrar o novo morador
#             else:
#                 print("Cadastro não realizado.")
#                 return  # Encerra a função sem adicionar o novo morador
    
#     # Cria e adiciona o novo morador
#     try:
#         novo_morador = Morador(nome, apartamento, bloco)
#         lista_moradores.append(novo_morador)
#         print(f"Morador {novo_morador.nome} adicionado com sucesso!")
#     except ValueError as e:
#         print(f"Erro ao adicionar morador: {e}")
