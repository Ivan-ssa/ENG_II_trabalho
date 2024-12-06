import json
import os
import re

lista_moradores = []

class Morador:
    def __init__(self, nome, apartamento, bloco):
        self.id = f"{apartamento}{bloco}"
        self.nome = nome
        self.apartamento = apartamento
        self.bloco = bloco

        # Adiciona o morador à lista se não existir
        if not self.morador_existe():
            lista_moradores.append(self)
            self.salvar_em_json_morador()  # Salva somente novos moradores
        else:
           print(f"Morador {self.id} já existe!")
    
    @staticmethod
    def validar_id(id_morador):
        """Valida se o ID do morador segue o formato 101A."""
        padrao = r"^\d{3}[A-Z]$"
        return bool(re.match(padrao, id_morador))

    def salvar_em_json_morador(self):
        caminho_arquivo = 'json/moradores.json'

        # Ler os moradores existentes no arquivo JSON
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                try:
                    moradores_existentes = json.load(file)
                except json.JSONDecodeError:
                    moradores_existentes = []  # Arquivo vazio ou corrompido
        else:
            moradores_existentes = []

        # Verificar se o morador já está no arquivo JSON
        for morador in moradores_existentes:
            if morador['apartamento'] == self.apartamento and morador['bloco'] == self.bloco:
                #print(f"Morador {self.id} já existe no arquivo JSON.")
                return

        # Adicionar o novo morador à lista
        novo_morador = {
            'nome': self.nome,
            'apartamento': self.apartamento,
            'bloco': self.bloco
        }
        moradores_existentes.append(novo_morador)

        # Salvar novamente no arquivo JSON
        with open(caminho_arquivo, 'w', encoding='utf-8') as file:
            json.dump(moradores_existentes, file, indent=3, ensure_ascii=False)

    def morador_existe(self):
        """Verifica se o morador já existe na lista de moradores."""
        for morador in lista_moradores:
            if morador.id == self.id:
                return True
        return False
def carregar_moradores():
    caminho_arquivo = 'json/moradores.json'

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            try:
                moradores = json.load(file)

                for morador in moradores:
                    if isinstance(morador, dict):
                        # Cria um objeto Morador para cada item carregado
                        novo_morador = Morador(morador['nome'], morador['apartamento'], morador['bloco'])
                        
                        # Verifica se o morador já existe
                        if not novo_morador.morador_existe():
                            lista_moradores.append(novo_morador)
            except json.JSONDecodeError:
                print("Erro ao ler o arquivo JSON. O arquivo pode estar corrompido.")
    else:
        print("Arquivo de moradores não encontrado.")







# def carregar_moradores():
#     caminho_arquivo = 'json/moradores.json'

#     if os.path.exists(caminho_arquivo):
#         with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#             try:
#                 moradores = json.load(file)
#                 # Carregar os moradores existentes no arquivo para a lista
#                 for morador in moradores:
#                     if isinstance(morador, dict):
#                         # Gerar o ID a partir do apartamento e bloco
#                         id_morador = str(morador['apartamento']) + morador['bloco']
                        
#                         # Verificar se o morador com o mesmo ID já existe na lista
#                         if not any(m.id == id_morador for m in lista_moradores):
#                             lista_moradores.append(Morador(morador['nome'], morador['apartamento'], morador['bloco']))
#             except json.JSONDecodeError:
#                 print("Erro ao ler o arquivo JSON. O arquivo pode estar corrompido.")
#     else:
#         print("Arquivo de moradores não encontrado.")





# import json
# import os
# import re

# lista_moradores = []

# class Morador:
#     def __init__(self, nome, apartamento, bloco):
#         self.id = f"{apartamento}{bloco}"
#         self.nome = nome
#         self.apartamento = apartamento
#         self.bloco = bloco

#         # Adiciona o morador à lista se não existir
#         if not self.morador_existe():
#             lista_moradores.append(self)
#             self.salvar_em_json_morador()  # Salva somente novos moradores
#         else:
#             print(f"Morador {self.id} já existe!")
    
#     @staticmethod
#     def validar_id(id_morador):
#         """Valida se o ID do morador segue o formato 101A."""
#         padrao = r"^\d{3}[A-Z]$"
#         return bool(re.match(padrao, id_morador))

#     def salvar_em_json_morador(self):
#         caminho_arquivo = 'json/moradores.json'

#         # Ler os moradores existentes no arquivo JSON
#         if os.path.exists(caminho_arquivo):
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 try:
#                     moradores_existentes = json.load(file)
#                 except json.JSONDecodeError:
#                     moradores_existentes = []  # Arquivo vazio ou corrompido
#         else:
#             moradores_existentes = []

#         # Adicionar o novo morador à lista
#         novo_morador = {
#             'nome': self.nome,
#             'apartamento': self.apartamento,
#             'bloco': self.bloco
#         }
#         moradores_existentes.append(novo_morador)

#         # Salvar novamente no arquivo JSON
#         with open(caminho_arquivo, 'w', encoding='utf-8') as file:
#             json.dump(moradores_existentes, file, indent=3, ensure_ascii=False)

#     def morador_existe(self):
#         """Verifica se o morador já existe na lista de moradores."""
#         for morador in lista_moradores:
#             if morador.id == self.id:
#                 return True
#         return False

# def carregar_moradores():
#     caminho_arquivo = 'json/moradores.json'

#     if os.path.exists(caminho_arquivo):
#         with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#             try:
#                 moradores = json.load(file)
#                 # Carregar os moradores existentes no arquivo para a lista
#                 for morador in moradores:
#                     if isinstance(morador, dict):
#                         Morador(morador['nome'], morador['apartamento'], morador['bloco'])  # Cria objetos de morador
#             except json.JSONDecodeError:
#                 print("Erro ao ler o arquivo JSON. O arquivo pode estar corrompido.")
#     else:
#         print("Arquivo de moradores não encontrado.")

# Chama a função de carregar moradores ao iniciar o programa







# import json,os,re

# lista_moradores = []
# class Morador:
#     def __init__(self, nome, apartamento, bloco):
#         # Validação do ID
#         self.id = f"{apartamento}{bloco}"
#         if not self.validar_id(self.id):
#             raise ValueError("O ID do morador deve estar no formato: três números seguidos de uma letra maiúscula (exemplo: 101A).")

#         self.nome = nome
#         self.apartamento = apartamento
#         self.bloco = bloco

#         # Verificar duplicação antes de adicionar
#         if not self.morador_existe():
#             lista_moradores.append(self)
#             self.salvar_em_json_morador()
#         else:
#             print(f"Morador {self.id} já existe!")

#     @staticmethod
#     def validar_id(id_morador):
#         """Valida se o ID do morador segue o formato 101A."""
#         padrao = r"^\d{3}[A-Z]$"
#         return bool(re.match(padrao, id_morador))

#     def salvar_em_json_morador(self):
#         caminho_arquivo = 'json/moradores.json'

#         # Ler os moradores existentes
#         if os.path.exists(caminho_arquivo):
#             with open(caminho_arquivo, 'r', encoding='utf-8') as file:
#                 try:
#                     moradores_existentes = json.load(file)
#                 except json.JSONDecodeError:
#                     moradores_existentes = []  # Arquivo vazio ou corrompido
#         else:
#             moradores_existentes = []

#         # Adicionar o novo morador à lista
#         novo_morador = {
#             'nome': self.nome,
#             'apartamento': self.apartamento,
#             'bloco': self.bloco
#         }
#         moradores_existentes.append(novo_morador)

#         # Salvar novamente no arquivo JSON
#         with open(caminho_arquivo, 'w', encoding='utf-8') as file:
#             json.dump(moradores_existentes, file, indent=3, ensure_ascii=False)

#     def morador_existe(self):
#         """Verifica se o morador já existe na lista de moradores."""
#         for morador in lista_moradores:
#             if morador.id == self.id:
#                 return True
#         return False
    # @classmethod
    # def salvar_todos_moradores(cls):
    #     with open('json/moradores.json', 'w', encoding='utf-8') as file:
    #         json.dump(
    #             [{'nome': morador.nome, 'apartamento': morador.apartamento, 'bloco': morador.bloco} for morador in lista_moradores],
    #             file,
    #             indent=3,
    #             ensure_ascii=False
    #         )




















# import json

# lista_moradores = []
# #---------------------------------------------------------

# class Morador:
#     def __init__(self, nome, apartamento, bloco):
         
        

#         self.id = f"{apartamento}{bloco}"
#         self.nome = nome
#         self.apartamento = apartamento
#         self.bloco = bloco
#         lista_moradores.append(self)
#         self.salvar_em_json_morador()

    

#     def salvar_em_json_morador(self):
#         # Converte cada morador em um dicionário, mas sem o campo 'id'
#         moradores_sem_id = [
#             {
#                 'nome': morador.nome,
#                 'apartamento': morador.apartamento,
#                 'bloco': morador.bloco
#             }
#             for morador in lista_moradores
#         ]
        
#         # Salva no arquivo JSON
#         with open('json\moradores.json', 'w', encoding='utf-8') as file:
#             json.dump(moradores_sem_id, file, indent=3, ensure_ascii=False)
#     @classmethod
#     def salvar_todos_moradores(cls):
#         with open('json/moradores.json', 'w', encoding='utf-8') as file:
#             json.dump(
#                     [{'nome': morador.nome, 'apartamento': morador.apartamento, 'bloco': morador.bloco} for morador in lista_moradores],
#                     file,
#                      indent=3,
#                      ensure_ascii=False
#                  )