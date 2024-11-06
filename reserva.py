import json
from datetime import datetime

lista_reservas = []

class Reserva:
    # Variável de classe para rastrear o próximo ID de reserva
    proximo_id = 1

    def __init__(self, espaco_id, morador_id, data, id=None):
        # Se um ID não for fornecido, gera automaticamente
        if id is None:
            self.id = Reserva.proximo_id  # Atribui o ID atual
            Reserva.proximo_id += 1  # Incrementa o próximo ID para a próxima reserva
        else:
            self.id = id  # Usa o ID fornecido

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

    @classmethod
    def carregar_reservas(cls):
        try:
            with open('json/reservas.json', 'r', encoding='utf-8') as file:
                reservas_carregadas = json.load(file)
                for reserva_data in reservas_carregadas:
                    # Cria uma nova reserva a partir dos dados carregados, passando o ID
                    reserva = cls(
                        espaco_id=reserva_data['espaco_id'],
                        morador_id=reserva_data['morador_id'],
                        data=reserva_data['data'],
                        id=reserva_data['id']  # Passa o ID do JSON
                    )
        except FileNotFoundError:
            print("Arquivo de reservas não encontrado. Nenhuma reserva foi carregada.")
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON.")
