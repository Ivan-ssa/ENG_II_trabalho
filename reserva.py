
import json

lista_reservas = []

class Reserva:
    def __init__(self, espaco_id, morador_id, data):
        self.espaco_id = espaco_id
        self.morador_id = morador_id
        self.data = data
        lista_reservas.append(self)
        self.salvar_em_json()

    def salvar_em_json(self):
        with open('reservas.json', 'w', encoding='utf-8') as file:
            json.dump([reserva.__dict__ for reserva in lista_reservas], file, indent=3, ensure_ascii=False)

    