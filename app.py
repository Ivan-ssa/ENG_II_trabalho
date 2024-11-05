import json

from flask import Flask, jsonify, request
from sistema import MoradorController, ReservaController

app = Flask(__name__)


# morador_controller = MoradorController()
# reserva_controller = ReservaController()

# Função auxiliar para ler dados do arquivo JSON
def ler_reservas():
    with open('json/reservas.json', 'r', encoding='utf-8') as file:
        return json.load(file)

# Função auxiliar para salvar dados no arquivo JSON
def salvar_reservas(reservas):
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(reservas, file, indent=3, ensure_ascii=False)

# Rota para listar reservas
@app.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = ler_reservas()
    return jsonify(reservas), 200

# Rota para adicionar uma nova reserva
@app.route('/reservas', methods=['POST'])
def adicionar_reserva():
    nova_reserva = request.get_json()
    reservas = ler_reservas()
    
    # Adiciona a nova reserva à lista
    reservas.append(nova_reserva)
    salvar_reservas(reservas)
    
    return jsonify(nova_reserva), 201

# Rota para deletar uma reserva
@app.route('/reservas/<int:id>', methods=['DELETE'])
def deletar_reserva(id):
    reservas = ler_reservas()
    reserva = next((res for res in reservas if res['id'] == id), None)
    
    if reserva:
        reservas.remove(reserva)
        salvar_reservas(reservas)
        return jsonify(reserva), 200
    else:
        return jsonify({'message': 'Reserva não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)



"""
py -m unittest discover -s test -p "test_*.py" --- testes
passos para os testes de CRUD 
pip install flask
python app.py inicinado o servidor



GET http://127.0.0.1:5000/reservas para listar as reservas.
POST http://127.0.0.1:5000/reservas com um corpo JSON para adicionar uma nova reserva

1. Criar uma Nova Reserva (POST)



POST /reservas
Content-Type: application/json

{
    "id": 2,
    "espaco_id": "churrasqueira",
    "morador_id": "456",
    "data": "02-01-23"
}

2. Listar Todas as Reservas (GET)
python
Copiar código

GET /reservas

3. Atualizar uma Reserva (PUT)
Para atualizar uma reserva existente, você precisa do ID da reserva e enviar as novas informações. Aqui está um exemplo:

URL: http://127.0.0.1:5000/reservas/<id>

Substitua <id> pelo ID da reserva que você deseja atualizar.

PUT /reservas/2


{
    "espaco_id": "churrasqueira",
    "morador_id": "456",
    "data": "03-01-23"
}

4. Deletar uma Reserva (DELETE)
Para deletar uma reserva existente, você precisa do ID da reserva. Aqui está um exemplo:



DELETE /reservas/2
Método: DELETE
URL: http://127.0.0.1:5000/reservas/<id> (substitua <id> pelo ID da reserva a ser deletada)

Testar as Rotas:

GET: http://127.0.0.1:5000/reservas
POST: http://127.0.0.1:5000/reservas com o corpo JSON.
PUT: http://127.0.0.1:5000/reservas/<id> com o corpo JSON atualizado.
DELETE: http://127.0.0.1:5000/reservas/<id>.
"""

#teste git

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Hello, Flask!'

# if __name__ == '__main__':
#     app.run(debug=True)
