import json
#add app
from flask import Flask, jsonify, request
from morador import Morador, lista_moradores
from reserva import Reserva
from funcion_morador import validar_nome,validar_bloco,validar_apartamento,atualizar_morador_no_arquivo,deletar_reservas_por_morador
from funcion_reservas import carregar_dados, validar_data,validar_disponibilidade,validar_espaco,validar_morador
app = Flask(__name__)
# Função auxiliar para ler dados do arquivo JSON
carregar_dados()
    
# def ler_reservas():
#     with open('json/reservas.json', 'r', encoding='utf-8') as file:
#         return json.load(file)
def ler_reservas():
    try:
        with open('reservas.json', 'r') as f:
            reservas = json.load(f)  # Isso deve carregar o JSON e converter para um dicionário/lista
            return reservas.get('reservas', [])  # Certifique-se de retornar a lista de reservas, caso exista
    except FileNotFoundError:
        return []  # Se o arquivo não for encontrado, retorna uma lista vazia
    except json.JSONDecodeError:
        return []  # Se o JSON estiver mal formatado, retorna uma lista vazia
def ler_moradores():
    with open('json/moradores.json', 'r', encoding='utf-8') as file:
        return json.load(file)
def ler_espacos():
    with open('json/espacos.json', 'r', encoding='utf-8') as file:
        return json.load(file)

#########################################################################################################

# Função auxiliar para salvar dados no arquivo JSON
def salvar_reservas(reservas):
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(reservas, file, indent=3, ensure_ascii=False)


def salvar_moradores(moradores):
    with open('json/moradores.json', 'w', encoding='utf-8') as file:
        json.dump(moradores, file, indent=3, ensure_ascii=False)


################################################################
# Rota para listar reservas
@app.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = ler_reservas()
    return jsonify(reservas), 200
#####################################################################
# listar moradores
@app.route('/moradores', methods=['GET'])
def listar_moradores():
    moradores = ler_moradores()
    return jsonify(moradores), 200
######################################################################
#listar espaços
@app.route('/espacos', methods=['GET'])
def listar_espacos():
    espacos = ler_espacos()
    return jsonify(espacos), 200
##########################################################

###   RESERVAS  POST --------------------

### --------------------------
@app.route("/reservas", methods=["POST"])
def adicionar_reserva():
    """Recebe os dados e cria uma nova reserva."""
    try:
        # Obtém os dados da requisição
        dados = request.get_json()

        # Valida o morador
        morador_id = dados.get("morador_id")
        if not morador_id:
            return jsonify({"erro": "O campo 'morador_id' é obrigatório!"}), 400
        morador = validar_morador(morador_id)

        # Valida a data da reserva
        data_reserva = dados.get("data")
        if not data_reserva:
            return jsonify({"erro": "O campo 'data' é obrigatório!"}), 400
        data_reserva = validar_data(data_reserva)

        # Valida o espaço
        espaco_id = dados.get("espaco_id")
        if not espaco_id:
            return jsonify({"erro": "O campo 'espaco_id' é obrigatório!"}), 400
        espaco = validar_espaco(espaco_id)

        # Verifica a disponibilidade
        validar_disponibilidade(espaco_id, data_reserva)

        # Cria a reserva
        descricao = dados.get("descricao", "")
        nova_reserva = Reserva(
            morador_id=morador.id,
            data=data_reserva,
            espaco_id=espaco_id,
            descricao=descricao
        )

        # Retorna a nova reserva
        return jsonify({
            "mensagem": "Reserva criada com sucesso!",
            "reserva": nova_reserva.__dict__
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#@@@@ moradores POST

# Rota para adicionar morador
@app.route('/moradores', methods=['POST'])
def adicionar_morador():
    try:
        dados = request.get_json()

        # Valida os dados recebidos
        nome = dados.get("nome")
        apartamento = dados.get("apartamento")
        bloco = dados.get("bloco")

        # Validações usando as funções reaproveitadas
        if not validar_nome(nome):
            return jsonify({"erro": "Nome inválido. O nome deve conter apenas letras e não pode estar vazio."}), 400
        if not validar_apartamento(apartamento):
            return jsonify({"erro": "Número de apartamento inválido. Deve estar entre 100-104, 200-204, 300-304, 400-404 ou 500-504."}), 400
        if not validar_bloco(bloco):
            return jsonify({"erro": "Letra do bloco inválida. Deve ser entre A e G."}), 400

        # Cria o morador e adiciona na lista
        novo_morador = Morador(nome, apartamento, bloco)
        return jsonify({"mensagem": f"Morador {novo_morador.nome} adicionado com sucesso!", "id": novo_morador.id}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao processar a solicitação."}), 500

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

################ PUT RESERVAS ########################

@app.route("/reservas/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    """Atualiza uma reserva existente."""
    try:
        # Lê as reservas do arquivo JSON
        reservas = ler_reservas()

        # Procura a reserva pelo ID
        reserva_existente = next((res for res in reservas if res["id"] == id), None)
        if not reserva_existente:
            return jsonify({"erro": "Reserva não encontrada!"}), 404

        # Obtém os dados da requisição
        dados = request.get_json()

        # Valida o morador
        # morador_id = dados.get("morador_id")
        
        # if morador_id:  # Atualiza somente se informado
        #     print(morador_id,"########")
        #     validar_morador(morador_id)
        #     reserva_existente["morador_id"] = morador_id
        #     print(reserva_existente)

        
        # # Valida a data da reserva
        # data_reserva = dados.get("data")
        # if data_reserva:  # Atualiza somente se informado
        #     data_reserva = validar_data(data_reserva)
        #     reserva_existente["data"] = data_reserva

        # # Valida o espaço
        # espaco_id = dados.get("espaco_id")
        # if espaco_id:  # Atualiza somente se informado
        #     validar_espaco(espaco_id)
        #     validar_disponibilidade(espaco_id, reserva_existente["data"])
        #     reserva_existente["espaco_id"] = espaco_id
    
        # Atualiza a descrição
        descricao = dados.get("descricao")
        if descricao is not None:  # Atualiza somente se informado
            reserva_existente["descricao"] = descricao

        # Salva a lista de reservas atualizada
        salvar_reservas(reservas)

        # Retorna a reserva atualizada
        return jsonify({
            "mensagem": "Reserva atualizada com sucesso!",
            "reserva": reserva_existente
        }), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500




#__________________________________________________________________________________________-
# @@@@@@@@@@@@@@@@@     PUT moradores   @@@@@@@@@@@@@@@@@@@@@@@@@
@app.route('/moradores/<int:apartamento>/<bloco>', methods=['PUT'])
def atualizar_morador_endpoint(apartamento, bloco):
    novos_dados = request.json
    morador_id = f"{apartamento}-{bloco}"  # Gerar ID corretamente a partir de apartamento e bloco

    # Atualizar o morador na lista e no arquivo
    mensagem = atualizar_morador_no_arquivo(morador_id, novos_dados)
    
    if "não encontrado" in mensagem:
        return jsonify({"erro": mensagem}), 404
    
    return jsonify({"mensagem": mensagem}), 200

#  @@@@@@@@@@@@@@@@@    delete morador   @@@@@@@@@@@@@@@@@@@@@@@@
# 


@app.route('/moradores/<int:apartamento>/<bloco>', methods=['DELETE'])
def deletar_morador_e_reservas(apartamento, bloco):
    # Gerar o ID do morador
    morador_id = f"{apartamento}{bloco}"

    # Ler moradores do arquivo
    moradores = ler_moradores()
    morador = next((res for res in moradores if res['apartamento'] == str(apartamento) and res['bloco'] == bloco), None)

    if morador:
        # Remover o morador
        moradores.remove(morador)
        salvar_moradores(moradores)

        # Remover reservas associadas ao morador
        resultado_reservas = deletar_reservas_por_morador(morador_id)

        return jsonify({
            "message": "Morador e reservas deletados com sucesso.",
            "morador": morador,
            "reservas_removidas": resultado_reservas
        }), 200
    else:
        return jsonify({'message': 'Morador não encontrado'}), 404


#________________________________________________________________________________________

# # Rota para deletar uma reserva
# @app.route('/reservas/<int:id>', methods=['DELETE'])
# def deletar_reserva(id):
#     reservas = ler_reservas()
#     reserva = next((res for res in reservas if res['id'] == id), None)
    
#     if reserva:
#         reservas.remove(reserva)
#         salvar_reservas(reservas)
#         return jsonify(reserva), 200
#     else:
#         return jsonify({'message': 'Reserva não encontrada'}), 404


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
