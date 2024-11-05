import json


class Morador:
    def __init__(self, id, nome, apartamento, bloco):
        self.id = id
        self.nome = nome
        self.apartamento = apartamento
        self.bloco = bloco
        #self.email = email

class Reserva:
    def __init__(self, espaco_id, morador_id, data_reserva):
        self.espaco_id = espaco_id
        self.morador_id = morador_id
        self.data_reserva = data_reserva

class MoradorController:
    def __init__(self, arquivo='json/moradores.json'):
        self.arquivo = arquivo
        self.moradores = self.carregar_moradores()

    def carregar_moradores(self):
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                return [Morador(**data) for data in json.load(file)]
        except FileNotFoundError:
            return []
    
    def salvar_moradores(self):
        with open(self.arquivo, 'w', encoding='utf-8') as file:
            json.dump([vars(morador) for morador in self.moradores], file, ensure_ascii=False, indent=4)

    def listar(self):
        return self.moradores

    def adicionar(self, morador):
        self.moradores.append(morador)
        self.salvar_moradores()

    def atualizar(self, id, morador_atualizado):
        for i, morador in enumerate(self.moradores):
            if morador.id == id:
                self.moradores[i] = morador_atualizado
                self.salvar_moradores()
                return True
        return False

    def deletar(self, id):
        for i, morador in enumerate(self.moradores):
            if morador.id == id:
                del self.moradores[i]
                self.salvar_moradores()
                return True
        return False


class ReservaController:
    def __init__(self, arquivo='json/reservas.json'):
        self.arquivo = arquivo
        self.reservas = self.carregar_reservas()

    def carregar_reservas(self):
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                return [Reserva(**data) for data in json.load(file)]
        except FileNotFoundError:
            return []

    def salvar_reservas(self):
        with open(self.arquivo, 'w', encoding='utf-8') as file:
            json.dump([vars(reserva) for reserva in self.reservas], file, ensure_ascii=False, indent=4)

    def listar(self):
        return self.reservas

    def adicionar(self, reserva):
        self.reservas.append(reserva)
        self.salvar_reservas()

    def atualizar(self, id, reserva_atualizada):
        for i, reserva in enumerate(self.reservas):
            if reserva.espaco_id == id:
                self.reservas[i] = reserva_atualizada
                self.salvar_reservas()
                return True
        return False

    def deletar(self, id):
        for i, reserva in enumerate(self.reservas):
            if reserva.espaco_id == id:
                del self.reservas[i]
                self.salvar_reservas()
                return True
        return False  