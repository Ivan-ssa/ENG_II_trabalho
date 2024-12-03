

from datetime import datetime
import json
from flask import Flask, jsonify, request
from funcion_reservas import adicionar_morador, fazer_reserva, deletar_morador  # Importando as funções criadas
from morador import lista_moradores
from reserva import lista_reservas,Reserva
from espaco import lista_espacos
app = Flask(__name__)



# Função para carregar dados na inicialização
def carregar_dados():
    global lista_moradores, lista_reservas, lista_espacos
    with open('json/moradores.json', 'r', encoding='utf-8') as file:
        lista_moradores = json.load(file)
    with open('json/reservas.json', 'r', encoding='utf-8') as file:
        lista_reservas = json.load(file)
    with open('json/espacos.json', 'r', encoding='utf-8') as file:
        lista_espacos = json.load(file)

# Função para salvar dados antes de encerrar
def salvar_dados():
    with open('json/moradores.json', 'w', encoding='utf-8') as file:
        json.dump(lista_moradores, file, indent=3, ensure_ascii=False)
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(lista_reservas, file, indent=3, ensure_ascii=False)

# Rotas de CRUD

# Rota para listar reservas
@app.route('/reservas', methods=['GET'])
def listar_reservas():
    return jsonify(lista_reservas), 200

# Rota para listar moradores
@app.route('/moradores', methods=['GET'])
def listar_moradores():
    return jsonify(lista_moradores), 200

# Rota para listar espaços
@app.route('/espacos', methods=['GET'])
def listar_espacos():
    return jsonify(lista_espacos), 200

# Rota para adicionar uma nova reserva

@app.route('/reservas', methods=['POST'])
def criar_reserva():
    try:
        # Obtém os dados do corpo da requisição (no formato JSON)
        dados = request.get_json()

        # Verifica se os dados necessários estão presentes
        if 'espaco_id' not in dados or 'morador_id' not in dados or 'data' not in dados:
            return jsonify({"erro": "Dados incompletos. Espaco_id, Morador_id e Data são necessários."}), 400

        espaco_id = dados['espaco_id']
        morador_id = dados['morador_id']
        data = dados['data']

        # Cria a reserva
        reserva = Reserva(espaco_id=espaco_id, morador_id=morador_id, data=data)
        
        # Retorna a resposta com os dados da reserva criada
        return jsonify({
            "id": reserva.id,
            "espaco_id": reserva.espaco_id,
            "morador_id": reserva.morador_id,
            "data": reserva.data
        }), 201  # Status 201 indica que a criação foi bem-sucedida

    except ValueError as e:
        # Se houver erro de validação na data
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        # Captura qualquer outro erro não esperado
        return jsonify({"erro": f"Ocorreu um erro: {str(e)}"}), 500



# Inicialização do aplicativo
if __name__ == '__main__':
    carregar_dados()  # Carrega os dados ao iniciar o servidor
    try:
        app.run(debug=True)
    finally:
        salvar_dados()  # Salva os dados ao encerrar o servidor

