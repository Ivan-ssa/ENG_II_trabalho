
import json
import os
from datetime import datetime

lista_reserva = []

class Reserva:
    proximo_id = 1

    def __init__(self, data, espaco_id, morador_id, descricao=None, id=None):
        global lista_reserva  # Acesso à lista global
        if id is None:
            self.id = Reserva.proximo_id
            Reserva.proximo_id += 1
        else:
            self.id = id
        
        self.espaco_id = espaco_id
        self.morador_id = morador_id
        self.data = data
        self.descricao = descricao
        lista_reserva.append(self)
        self.salvar_em_json_reserva()

    def reserva_existe_no_json(self, dados_reservas):
        """Verifica se a reserva já existe no arquivo JSON."""
        for reserva in dados_reservas.get("reservas", []):
            if (
                reserva["morador_id"] == self.morador_id and
                reserva["espaco_id"] == self.espaco_id and
                reserva["data_reserva"] == self.data
            ):
                return True
        return False

    @staticmethod
    def validar_data(data):
        try:
            return datetime.strptime(data, "%d-%m-%y").strftime("%d-%m-%y")
        except ValueError:
            raise ValueError("Data inválida! Use o formato DD-MM-AA.")

    def salvar_em_json_reserva(self):
        caminho_arquivo = 'json/reservas.json'

        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                try:
                    dados_reservas = json.load(file)
                except json.JSONDecodeError:
                    dados_reservas = {"reservas": [], "proximo_id": 1}
        else:
            dados_reservas = {"reservas": [], "proximo_id": 1}

        # Verificar se a reserva já existe no JSON
        if not self.reserva_existe_no_json(dados_reservas):
            reserva_dict = {
                "id": self.id,
                "morador_id": self.morador_id,
                "espaco_id": self.espaco_id,
                "data_reserva": self.data,
                "descricao": self.descricao
            }
            dados_reservas["reservas"].append(reserva_dict)

            # Atualizar o próximo ID
            dados_reservas["proximo_id"] = len(dados_reservas["reservas"]) + 1

            # Salvar no arquivo JSON
            with open(caminho_arquivo, 'w', encoding='utf-8') as file:
                json.dump(dados_reservas, file, indent=4, ensure_ascii=False)

def carregar_reservas():
    caminho_arquivo = 'json/reservas.json'

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            try:
                dados_reservas = json.load(file)

                for reserva in dados_reservas.get("reservas", []):
                    nova_reserva = Reserva(
                        reserva["data_reserva"], 
                        reserva["espaco_id"], 
                        reserva["morador_id"], 
                        reserva.get("descricao", None), 
                        reserva["id"]
                    )
                    
                    # Evitar duplicar na lista global
                    if not any(r.id == nova_reserva.id for r in lista_reserva):
                        lista_reserva.append(nova_reserva)
            except json.JSONDecodeError:
                print("Erro ao ler o arquivo JSON. O arquivo pode estar corrompido.")
    else:
        print("Arquivo de reservas não encontrado.")




# import json,os
# from datetime import datetime



# lista_reserva = []

# class Reserva:
#     proximo_id = 1

#     def __init__(self, data, espaco_id, morador_id, descricao=None, id=None):
#         global lista_reserva  # Acesso à lista global
#         if id is None:
#             self.id = Reserva.proximo_id
#             Reserva.proximo_id += 1
#         else:
#             self.id = id
        
#         self.espaco_id = espaco_id
#         self.morador_id = morador_id
#         self.data = data
#         self.descricao = descricao  # Adicionando o campo descricao
#         lista_reserva.append(self)
#         self.salvar_em_json_reserva()

#     # def __str__(self):
#     #     """Representação da reserva para exibição amigável."""
#     #     return f"ID: {self.id}, Espaço ID: {self.espaco_id}, Morador ID: {self.morador_id}, Data: {self.data}, Descrição: {self.descricao}"
#     def reserva_existe(self):
#         global lista_reservas
#         """Verifica se a reserva já existe na lista de reservas."""
#         for reserva in lista_reservas:
#             if (reserva.morador_id == self.morador_id and
#                 reserva.data == self.data and
#                 reserva.horario == self.horario and
#                 reserva.local == self.local):
#                 return True
#         return False
#     @staticmethod
#     def validar_data(data):
#         try:
#             return datetime.strptime(data, "%d-%m-%y").strftime("%d-%m-%y")
#         except ValueError:
#             raise ValueError("Data inválida! Use o formato DD-MM-AA.")

    
#     def salvar_em_json_reserva(self):
#         # Caminho para o arquivo JSON
#         caminho_arquivo = 'json/reservas.json'

#         # Verificar se o arquivo já existe
#         if os.path.exists(caminho_arquivo):
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 try:
#                     dados_reservas = json.load(file)
#                     if not isinstance(dados_reservas.get("reservas"), list):
#                         dados_reservas["reservas"] = []  # Corrige se não for uma lista
#                 except json.JSONDecodeError:
#                     dados_reservas = {"reservas": [], "proximo_id": 1}
#         else:
#             dados_reservas = {"reservas": [], "proximo_id": 1}

#         # Cria um dicionário com os dados da reserva
#         reserva_dict = {
#             "id": self.id,
#             "morador_id": self.morador_id,
#             "espaco_id": self.espaco_id,
#             "data_reserva": self.data,
#             "descricao": self.descricao
#         }

#         # Adiciona a nova reserva à lista de reservas
#         dados_reservas["reservas"].append(reserva_dict)

#         # Atualiza o próximo ID para o próximo item a ser adicionado
#         dados_reservas["proximo_id"] = len(dados_reservas["reservas"]) + 1

#         # Salva os dados atualizados no arquivo JSON
#         with open(caminho_arquivo, 'w', encoding='utf-8') as file:
#             json.dump(dados_reservas, file, indent=4, ensure_ascii=False)

#         #print("Reserva salva com sucesso no arquivo JSON!")

    

# def carregar_reservas():
#     caminho_arquivo = 'json/reservas.json'

#     if os.path.exists(caminho_arquivo):
#         with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#             try:
#                 reservas = json.load(file)

#                 for reserva in reservas:
#                     if isinstance(reserva, dict):
#                         # Cria um objeto Reserva para cada item carregado
#                         nova_reserva = Reserva(
#                             reserva['data'], 
#                             reserva['espaco_id'], 
#                             reserva['morador_id'], 
#                             reserva.get('descricao', None),  # Pegando o campo descricao (se existir)
#                             reserva.get('id', None)  # Pegando o id (caso o arquivo tenha id)
#                         )
                        
#                         # Verifica se a reserva já existe antes de adicionar
#                         if not nova_reserva.reserva_existe():
#                             lista_reserva.append(nova_reserva)
#             except json.JSONDecodeError:
#                 print("Erro ao ler o arquivo JSON. O arquivo pode estar corrompido.")
#     else:
#         print("Arquivo de reservas não encontrado.")