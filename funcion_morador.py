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
    nome = str(input("Nome do Morador: ")).strip().upper()
    if not validar_nome(nome):
        return

    apartamento = str(input("Número do Apartamento: ")).strip().upper()
    if not validar_apartamento(apartamento):
        return

    bloco = str(input("Bloco do Morador: ")).strip().upper().upper()
    if not validar_bloco(bloco):
        return

    # Gerar o ID do morador
    id_morador = str(apartamento) + bloco

    # Verificar se o morador já existe na lista
    if any(m.id == id_morador for m in lista_moradores):
        print(f"Este Apartamento com ID {id_morador} já está cadastrado.")
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




import json

def deletar_reservas_por_morador(morador_id):
    """
    Remove todas as reservas associadas ao morador_id fornecido e retorna as reservas excluídas.
    
    Args:
        morador_id (str): ID do morador cujas reservas serão deletadas.
    
    Returns:
        dict: Informações sobre o resultado da operação, incluindo as reservas removidas.
    """
    try:
        # Carrega o arquivo JSON
        with open('json/reservas.json', 'r') as arquivo:
            dados = json.load(arquivo)

        # Verifica se a chave 'reservas' existe e é uma lista
        if not isinstance(dados.get('reservas'), list):
            return {"erro": "O arquivo JSON não contém uma lista de reservas válida"}

        reservas = dados['reservas']

        # Separa as reservas a serem removidas
        reservas_removidas = [reserva for reserva in reservas if reserva.get('morador_id') == morador_id]
        # Filtra as reservas que NÃO pertencem ao morador
        novas_reservas = [reserva for reserva in reservas if reserva.get('morador_id') != morador_id]

        # Atualiza o conteúdo do JSON com as novas reservas
        dados['reservas'] = novas_reservas

        with open('json/reservas.json', 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

        return {
            "message": "Reservas deletadas com sucesso.",
            "reservas_removidas": reservas_removidas
        }
    except FileNotFoundError:
        return {"erro": "Arquivo reservas.json não encontrado"}
    except json.JSONDecodeError:
        return {"erro": "Erro ao processar o arquivo JSON"}



def deletar_morador_e_reservas(morador_id, moradores_arquivo='json/moradores.json', reservas_arquivo='json/reservas.json'):
    """
    Remove o morador e todas as suas reservas associadas.
    
    Args:
        morador_id (str): ID do morador a ser deletado.
        moradores_arquivo (str): Caminho para o arquivo de moradores.
        reservas_arquivo (str): Caminho para o arquivo de reservas.
    
    Returns:
        dict: Informações sobre o resultado da operação.
    """
    # Deletar morador
    try:
        with open(moradores_arquivo, 'r') as arquivo:
            moradores = json.load(arquivo)

        morador = next((m for m in moradores if f"{m['apartamento']}{m['bloco']}" == morador_id), None)

        if not morador:
            return {"erro": "Morador não encontrado"}

        # Remove o morador da lista
        moradores.remove(morador)

        # Atualiza o arquivo
        with open(moradores_arquivo, 'w') as arquivo:
            json.dump(moradores, arquivo, indent=4)
    except FileNotFoundError:
        return {"erro": "Arquivo moradores.json não encontrado"}
    except json.JSONDecodeError:
        return {"erro": "Erro ao processar o arquivo JSON de moradores"}

    # Deletar reservas associadas
    resultado_reservas = deletar_reservas_por_morador(morador_id)

    # Combinar o resultado
    return {
        "message": "Morador e reservas deletados com sucesso.",
        "morador": morador,
        **resultado_reservas
    }
