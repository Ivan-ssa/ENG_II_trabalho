import json

from flask import Flask, jsonify, request


app = Flask(__name__)


# Função auxiliar para ler dados do arquivo JSON
def ler_reservas():
    with open('json/reservas.json', 'r', encoding='utf-8') as file:
        return json.load(file)
def ler_moradores():
    with open('json/moradores.json', 'r', encoding='utf-8') as file:
        return json.load(file)
def ler_espacos():
    with open('json/espacos.json', 'r', encoding='utf-8') as file:
        return json.load(file)




# Função auxiliar para salvar dados no arquivo JSON
def salvar_reservas(reservas):
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(reservas, file, indent=3, ensure_ascii=False)

def salvar_moradores(moradores):
    with open('json/moradores.json', 'w', encoding='utf-8') as file:
        json.dump(moradores, file, indent=3, ensure_ascii=False)



# Rota para listar reservas
@app.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = ler_reservas()
    return jsonify(reservas), 200
# listar moradores
@app.route('/moradores', methods=['GET'])
def listar_moradores():
    moradores = ler_moradores()
    return jsonify(moradores), 200
#listar espaços
@app.route('/espacos', methods=['GET'])
def listar_espacos():
    espacos = ler_espacos()
    return jsonify(espacos), 200






# Rota para adicionar uma nova reserva
@app.route('/reservas', methods=['POST'])
def adicionar_reserva():
    nova_reserva = request.get_json()
    reservas = ler_reservas()
    
    # Adiciona a nova reserva à lista
    reservas.append(nova_reserva)
    salvar_reservas(reservas)
    
    return jsonify(nova_reserva), 201

@app.route('/moradores', methods=['POST'])
def adicionar_morador():
    novo_morador = request.get_json()
    morador = ler_moradores()
    
    # Adiciona a novo morador à lista
    morador.append(novo_morador)
    salvar_moradores(morador)
    
    return jsonify(novo_morador), 201




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

# deletar o morador.
@app.route('/moradores/<int:apartamento>/<bloco>', methods=['DELETE'])
def deletar_morador(apartamento, bloco):
    moradores = ler_moradores()
    morador = next((res for res in moradores if res['apartamento'] == str(apartamento) and res['bloco'] == bloco), None)
    
    if morador:
        moradores.remove(morador)
        salvar_moradores(moradores)
        return jsonify(morador), 200
    else:
        return jsonify({'message': 'Morador não encontrado'}), 404









if __name__ == '__main__':
    app.run(debug=True)


"""
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