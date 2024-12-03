import json
import re
lista_moradores = []
class Morador:
    def __init__(self, nome, apartamento, bloco):
        # Validação do ID
        self.id = f"{apartamento}{bloco}"
        if not self.validar_id(self.id):
            raise ValueError("O ID do morador deve estar no formato: três números seguidos de uma letra maiúscula (exemplo: 101A).")

        self.nome = nome
        self.apartamento = apartamento
        self.bloco = bloco
        lista_moradores.append(self)
        self.salvar_em_json_morador()

    @staticmethod
    def validar_id(id_morador):
        """Valida se o ID do morador segue o formato 101A."""
        padrao = r"^\d{3}[A-Z]$"
        return bool(re.match(padrao, id_morador))

    def salvar_em_json_morador(self):
        moradores_sem_id = [
            {
                'nome': morador.nome,
                'apartamento': morador.apartamento,
                'bloco': morador.bloco
            }
            for morador in lista_moradores
        ]
        with open('json/moradores.json', 'w', encoding='utf-8') as file:
            json.dump(moradores_sem_id, file, indent=3, ensure_ascii=False)

    @classmethod
    def salvar_todos_moradores(cls):
        with open('json/moradores.json', 'w', encoding='utf-8') as file:
            json.dump(
                [{'nome': morador.nome, 'apartamento': morador.apartamento, 'bloco': morador.bloco} for morador in lista_moradores],
                file,
                indent=3,
                ensure_ascii=False
            )




















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