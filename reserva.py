
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
        self.descricao = descricao  # Adicionando o campo descricao

        lista_reserva.append(self)
    # def __str__(self):
    #     """Representação da reserva para exibição amigável."""
    #     return f"ID: {self.id}, Espaço ID: {self.espaco_id}, Morador ID: {self.morador_id}, Data: {self.data}, Descrição: {self.descricao}"

    @staticmethod
    def validar_data(data):
        try:
            return datetime.strptime(data, "%d-%m-%y").strftime("%d-%m-%y")
        except ValueError:
            raise ValueError("Data inválida! Use o formato DD-MM-AA.")
