# import json
# from flask import jsonify
# from morador import Morador
# from reserva import Reserva

# # Função para carregar os moradores do arquivo JSON
# def carregar_moradores():
#     with open('moradores.json', 'r') as file:
#         data = json.load(file)
#     return data  # Retorna diretamente a lista de moradores

# # Função para salvar os moradores no arquivo JSON
# def salvar_moradores(moradores):
#     with open('moradores.json', 'w') as file:
#         json.dump(moradores, file, indent=4)

# # Função para gerar o id automaticamente
# def gerar_id(morador):
#     # Gera o id concatenando apartamento e bloco
#     return f"{morador['apartamento']}{morador['bloco']}"
# # Função de criação de morador
# def criar_morador(apartamento, bloco):
#     morador = {
#         'apartamento': apartamento,
#         'bloco': bloco
#     }
#     # Atribui o id gerado ao morador
#     morador['id'] = gerar_id(morador)
#     return morador
# # Função para buscar o morador pelo id
# def buscar_morador(id_morador):
#     moradores = carregar_moradores()  # Carrega os moradores
#     for morador in moradores:
#         if morador['id'] == id_morador:  # Busca pelo campo 'id'
#             return morador
#     return None

# # Função para remover reservas associadas ao morador
# def remover_reservas_por_morador(morador_id):
#     reservas = carregar_reservas()  # Função para carregar as reservas do JSON
#     reservas_filtradas = [reserva for reserva in reservas if reserva['morador_id'] != morador_id]
    
#     # Salvar as reservas filtradas de volta no JSON
#     salvar_reservas(reservas_filtradas)
#     print(f"Todas as reservas associadas ao morador ID {morador_id} foram removidas.")

# # Função para carregar as reservas do arquivo JSON
# def carregar_reservas():
#     with open('reservas.json', 'r') as file:
#         data = json.load(file)
#     return data['reservas']

# # Função para salvar as reservas no arquivo JSON
# def salvar_reservas(reservas):
#     with open('reservas.json', 'w') as file:
#         json.dump({"reservas": reservas}, file, indent=4)

# # Função principal para deletar o morador e suas reservas
# def deletar_morador(morador):
#     # Verifica se o morador tem um id
#     if 'id' in morador:
#         # Chama a função para remover as reservas
#         remover_reservas_por_morador(morador['id'])
#         # Remover o morador da lista ou banco de dados
#         morador_removido = True  # Exemplo de remoção
#         return morador_removido
#     else:
#         # Se não encontrar o id, gera um erro
#         return "Morador não encontrado!"

# # Função para adicionar um novo morador (exemplo)
# def adicionar_morador(nome, apartamento, bloco):
#     morador = {
#         "nome": nome,
#         "apartamento": apartamento,
#         "bloco": bloco,
#         "id": gerar_id({"apartamento": apartamento, "bloco": bloco})  # Gerando o id automaticamente
#     }
    
#     moradores = carregar_moradores()  # Carrega a lista de moradores
#     moradores.append(morador)  # Adiciona o novo morador
#     salvar_moradores(moradores)  # Salva os moradores de volta no arquivo
    
#     return jsonify({'message': 'Morador adicionado com sucesso!', 'morador': morador}), 201
# def remover_reservas_por_morador(morador_id):
#     global lista_reservas
#     lista_reservas = [reserva for reserva in lista_reservas if reserva.morador_id != morador_id]
#     Reserva.salvar_todas_reservas()
#     print(f"Todas as reservas associadas ao morador ID {morador_id} foram removidas.")

# def deletar_morador(morador_id):
#     global lista_moradores
#     morador_existe = any(morador.id == morador_id for morador in lista_moradores)
#     if not morador_existe:
#         print("Morador não encontrado. Não é possível deletar.")
#         return

#     lista_moradores = [morador for morador in lista_moradores if morador.id != morador_id]
#     Morador.salvar_todos_moradores()  # Atualiza o arquivo de moradores
#     remover_reservas_por_morador(morador_id)  # Remove reservas do morador
#     print(f"Morador ID {morador_id} e suas reservas foram removidos com sucesso.")

# def deletar_morador(morador_id):
#     if not Morador.validar_id(morador_id):
#         print("ID inválido. O formato deve ser três números seguidos de uma letra maiúscula (exemplo: 101A).")
#         return

#     global lista_moradores
#     morador_existe = any(morador.id == morador_id for morador in lista_moradores)
#     if not morador_existe:
#         print("Morador não encontrado.")
#         return

#     lista_moradores = [morador for morador in lista_moradores if morador.id != morador_id]
#     Morador.salvar_todos_moradores()
#     remover_reservas_por_morador(morador_id)
#     print(f"Morador com ID {morador_id} e suas reservas foram removidos com sucesso.")


# def atualizar_morador_no_arquivo(morador_id, novos_dados):
#     caminho_arquivo = 'json/moradores.json'
    
#     # Procurar o morador na lista de memória
#     morador_encontrado = None
#     for morador in lista_moradores:
#         # Gerar o ID do morador a partir do apartamento e bloco
#         id_atual = f"{morador.apartamento}-{morador.bloco}"
        
#         # Verificar se o ID gerado corresponde ao ID fornecido
#         if id_atual == morador_id:
#             morador.nome = novos_dados['nome']
#             morador.apartamento = novos_dados['apartamento']
#             morador.bloco = novos_dados['bloco']
#             morador_encontrado = morador
#             #print(f"Morador encontrado: {morador.nome}, {morador.apartamento}-{morador.bloco}")
#             break
    
#     if morador_encontrado is None:
#         return f"Morador com ID {morador_id} não encontrado."

#     # Atualizar o arquivo JSON
#     if os.path.exists(caminho_arquivo):
#         with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#             try:
#                 moradores_existentes = json.load(file)
#                 #print(f"Moradores carregados do arquivo: {moradores_existentes}")
#             except json.JSONDecodeError:
#                 moradores_existentes = []  # Arquivo vazio ou corrompido
#     else:
#         moradores_existentes = []

#     # Atualizar o morador no arquivo JSON
#     for morador in moradores_existentes:
#         if morador['apartamento'] == morador_encontrado.apartamento and morador['bloco'] == morador_encontrado.bloco:
#             morador['nome'] = morador_encontrado.nome
#             #print(f"Morador {morador_encontrado.nome} atualizado no JSON.")
#             break
#     else:
#         # Se o morador não for encontrado no arquivo JSON, adiciona como novo
#         moradores_existentes.append({
#             'nome': morador_encontrado.nome,
#             'apartamento': morador_encontrado.apartamento,
#             'bloco': morador_encontrado.bloco
#         })
#         #print(f"Morador {morador_encontrado.nome} adicionado ao JSON.")

#     # Salvar novamente no arquivo JSON
#     with open(caminho_arquivo, 'w', encoding='utf-8') as file:
#         json.dump(moradores_existentes, file, indent=3, ensure_ascii=False)
#         print(f"Arquivo JSON atualizado: {moradores_existentes}")

#     return f"Morador {morador_encontrado.nome} atualizado com sucesso."
