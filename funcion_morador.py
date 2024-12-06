# Função para carregar dados dos arquivos JSON


import json,os

from morador import Morador,lista_moradores
from reserva import Reserva


def buscar_morador_por_id(id_morador):
    if not Morador.validar_id(id_morador):
        print("ID inválido. O formato deve ser três números seguidos de uma letra maiúscula (exemplo: 101A).")
        return None

    for morador in lista_moradores:
        if morador.id == id_morador:
            return morador

    print("Morador não encontrado.")
    return None

def listar_moradores():
    print("Moradores cadastrados:")
    if lista_moradores:
        for morador in lista_moradores:
            #print(f"Tipo de dado de 'morador': {type(morador)}")
            #print(f"Tipo de dado de 'morador.id': {type(morador.id)}")
            print(f"ID: {morador.id}, Nome: {morador.nome}")
    else:
        print("Nenhum morador cadastrado.")


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
    nome = input("Nome do Morador: ")
    apartamento = input("Número do Apartamento: ")
    bloco = input("Bloco do Morador: ")
    
    # Gerar o ID do morador
    id_morador = str(apartamento) + bloco

    # Verificar se o morador já existe na lista
    if any(m.id == id_morador for m in lista_moradores):
        print(f"Este morador com ID {id_morador} já está cadastrado.")
    else:
        novo_morador = Morador(nome, apartamento, bloco)
        lista_moradores.append(novo_morador)
        print(f"Morador {nome} adicionado com sucesso!")


def atualizar_morador_no_arquivo(morador_id, novos_dados):
    caminho_arquivo = 'json/moradores.json'
    
    # Procurar o morador na lista de memória
    morador_encontrado = None
    for morador in lista_moradores:
        # Gerar o ID do morador a partir do apartamento e bloco
        id_atual = f"{morador.apartamento}-{morador.bloco}"
        
        # Verificar se o ID gerado corresponde ao ID fornecido
        if id_atual == morador_id:
            morador.nome = novos_dados['nome']
            morador.apartamento = novos_dados['apartamento']
            morador.bloco = novos_dados['bloco']
            morador_encontrado = morador
            #print(f"Morador encontrado: {morador.nome}, {morador.apartamento}-{morador.bloco}")
            break
    
    if morador_encontrado is None:
        return f"Morador com ID {morador_id} não encontrado."

    # Atualizar o arquivo JSON
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            try:
                moradores_existentes = json.load(file)
                #print(f"Moradores carregados do arquivo: {moradores_existentes}")
            except json.JSONDecodeError:
                moradores_existentes = []  # Arquivo vazio ou corrompido
    else:
        moradores_existentes = []

    # Atualizar o morador no arquivo JSON
    for morador in moradores_existentes:
        if morador['apartamento'] == morador_encontrado.apartamento and morador['bloco'] == morador_encontrado.bloco:
            morador['nome'] = morador_encontrado.nome
            #print(f"Morador {morador_encontrado.nome} atualizado no JSON.")
            break
    else:
        # Se o morador não for encontrado no arquivo JSON, adiciona como novo
        moradores_existentes.append({
            'nome': morador_encontrado.nome,
            'apartamento': morador_encontrado.apartamento,
            'bloco': morador_encontrado.bloco
        })
        #print(f"Morador {morador_encontrado.nome} adicionado ao JSON.")

    # Salvar novamente no arquivo JSON
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        json.dump(moradores_existentes, file, indent=3, ensure_ascii=False)
        print(f"Arquivo JSON atualizado: {moradores_existentes}")

    return f"Morador {morador_encontrado.nome} atualizado com sucesso."

def deletar_reservas_por_morador(morador_id):
    try:
        # Carrega o arquivo JSON
        with open('json/reservas.json', 'r') as arquivo:
            dados = json.load(arquivo)

        # Verifique o conteúdo de 'dados' para garantir que seja uma lista de reservas
        #print(dados)  # Remova após a depuração

        # Filtra as reservas que NÃO pertencem ao morador
        novas_reservas = [reserva for reserva in dados if reserva['morador_id'] != morador_id]

        # Atualiza o conteúdo do JSON com as novas reservas
        with open('json/reservas.json', 'w') as arquivo:
            json.dump(novas_reservas, arquivo, indent=4)

        #print(f"Reservas do morador com ID {morador_id} foram deletadas com sucesso.")
        return {"reservas_removidas": len(dados) - len(novas_reservas)}  # Retorna a quantidade de reservas removidas
    except FileNotFoundError:
        #print("Erro: O arquivo reservas.json não foi encontrado.")
        return {"erro": "Arquivo não encontrado"}
    except json.JSONDecodeError:
        #print("Erro: O conteúdo do arquivo reservas.json não é válido.")
        return {"erro": "Erro ao processar o arquivo JSON"}

#