
from datetime import datetime
import json
from flask import Flask, jsonify, request
from funcion_morador import adicionar_morador,deletar_morador
from funcion_reservas import salvar_reservas,criar_reserva
from espaco import lista_espacos
from morador import lista_moradores
from reserva import Reserva, lista_reserva

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

def criar_reserva_apia(data_reserva, espaco_id, morador_id, descricao=""):
    # Verifica se o morador existe
    morador = next((m for m in lista_moradores if m.id == morador_id), None)
    if not morador:
        return {"erro": "Morador não encontrado"}

    # Verifica se o espaço existe
    espaco = next((e for e in lista_espacos if e.id == espaco_id), None)
    if not espaco:
        return {"erro": "Espaço não encontrado"}

    # Cria a reserva
    reserva = Reserva(
        data=data_reserva,
        espaco_id=espaco.id,
        morador_id=morador.id,
        descricao=descricao if descricao else None
    )

    # Salva a reserva no arquivo JSON
    salvar_reservas(reserva)

    return {
        "sucesso": True,
        "reserva": {
            "data": reserva.data,
            "espaco_id": reserva.espaco_id,
            "morador_id": reserva.morador_id,
            "descricao": reserva.descricao,
        }
    }
# Função para salvar dados antes de encerrar
def salvar_dados():
    with open('json/moradores.json', 'w', encoding='utf-8') as file:
        json.dump(lista_moradores, file, indent=3, ensure_ascii=False)
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(lista_reservas, file, indent=3, ensure_ascii=False)

# Rotas de CRUD
# metodos [ GET ] 
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



# metodos [ POST ]
# Rota para adicionar um novo morador
@app.route('/moradores', methods=['POST'])
def novo_morador():
    novo_morador = request.get_json()
    resposta = adicionar_morador(novo_morador, lista_moradores)
    if 'erro' in resposta:
        return jsonify(resposta), 400
    return jsonify(resposta), 201


@app.route("/reservas", methods=["POST"])
def criar_reserva_api():
    # Recebe o JSON enviado
    dados = request.json

    # Verifica se todos os campos obrigatórios estão presentes
    campos_obrigatorios = ["morador_id", "espaco_id", "data_reserva"]
    campos_faltando = [campo for campo in campos_obrigatorios if campo not in dados]

    if campos_faltando:
        # Se faltar algum campo, retorna uma mensagem de erro com os campos faltantes
        return jsonify({
            "erro": "Campos obrigatórios faltando",
            "campos_faltando": campos_faltando
        }), 400

    # Adiciona o dado na lista de reservas
    #lista_reservas.append(dados)
    
    # Salva a lista de reservas no arquivo JSON
    #salvar_reservas()

    # Retorna o mesmo JSON recebido
    return jsonify(dados), 201  # Retorna o JSON com código 201 para criação bem-sucedida



# Rota para atualizar uma reserva existente
@app.route('/reservas/<int:id>', methods=['PUT'])
def atualizar_reserva(id):
    dados_atualizados = request.get_json()
    reserva = next((res for res in lista_reservas if res['id'] == id), None)
    if reserva:
        reserva.update(dados_atualizados)
        return jsonify(reserva), 200
    return jsonify({'erro': 'Reserva não encontrada'}), 404

# Rota para deletar uma reserva
@app.route('/reservas/<int:id>', methods=['DELETE'])
def excluir_reserva(id):
    reserva = next((res for res in lista_reservas if res['id'] == id), None)
    if reserva:
        lista_reservas.remove(reserva)
        return jsonify(reserva), 200
    return jsonify({'erro': 'Reserva não encontrada'}), 404

# Rota para deletar um morador
@app.route('/moradores/<int:apartamento>/<bloco>', methods=['DELETE'])
def excluir_morador(apartamento, bloco):
    resposta = deletar_morador(apartamento, bloco, lista_moradores, lista_reservas)
    if 'erro' in resposta:
        return jsonify(resposta), 404
    return jsonify(resposta), 200

# Inicialização do aplicativo
if __name__ == '__main__':
    carregar_dados()  # Carrega os dados ao iniciar o servidor
    try:
        app.run(debug=True)
    finally:
        salvar_dados()  # Salva os dados ao encerrar o servidor


