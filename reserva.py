import json
from datetime import datetime

lista_reservas = []

class Reserva:
    def __init__(self, espaco_id, morador_id, data):
        # Formata e valida a data no formato DD-MM-AA
        try:
            self.data = datetime.strptime(data, "%d-%m-%y").strftime("%d-%m-%y")
        except ValueError:
            raise ValueError("Data inválida! Use o formato DD-MM-AA.")
        
        self.espaco_id = espaco_id
        self.morador_id = morador_id
        
        # Adiciona a reserva à lista se o espaço estiver disponível na data
        if self.is_disponivel(espaco_id, self.data):
            lista_reservas.append(self)
            self.salvar_em_json()
        else:
            print("Espaço já reservado para essa data.")

    def is_disponivel(self, espaco_id, data):
        # Verifica se o espaço já está reservado para a data fornecida
        for reserva in lista_reservas:
            if reserva.espaco_id == espaco_id and reserva.data == data:
                return False
        return True

    def salvar_em_json(self):
        with open('json/reservas.json', 'w', encoding='utf-8') as file:
            json.dump([reserva.__dict__ for reserva in lista_reservas], file, indent=3, ensure_ascii=False)
