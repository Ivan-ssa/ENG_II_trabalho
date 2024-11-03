import json
    
lista_moradores = []
class Morador:
    def __init__(self,nome, apartamento, bloco):
        self.id = f"{apartamento}{bloco}"
        self.nome = nome
        self.apartamento = apartamento
        self.bloco = bloco
        lista_moradores.append(self)
        self.salvar_em_json()

    def salvar_em_json(self):
        # Converte cada morador em um dicionário, mas sem o campo 'id'
        moradores_sem_id = [
            {
                'nome': morador.nome,
                'apartamento': morador.apartamento,
                'bloco': morador.bloco
            }
            for morador in lista_moradores
        ]
        
        # Salva no arquivo JSON
        with open('moradores.json', 'w', encoding='utf-8') as file:
            json.dump(moradores_sem_id, file, indent=3, ensure_ascii=False)