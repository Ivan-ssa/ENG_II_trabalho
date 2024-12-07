import json
#add app
from flask import Flask, jsonify, request
from morador import Morador, lista_moradores
from reserva import Reserva
from funcion_morador import validar_nome,validar_bloco,validar_apartamento,atualizar_morador_no_arquivo,deletar_morador_e_reservas,deletar_reservas_por_morador
from funcion_reservas import carregar_dados, validar_data,validar_disponibilidade,validar_espaco,validar_morador
app = Flask(__name__)
# Função auxiliar para ler dados do arquivo JSON
carregar_dados()
    
def ler_reservas():
    try:
        with open('json/reservas.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data["reservas"], data["proximo_id"]  # Retorna as reservas e o próximo ID
    except FileNotFoundError:
        return [], 1  # Se o arquivo não existir, retorna lista vazia e próximo ID como 1



# def ler_reservas():
#     try:
#         with open('reservas.json', 'r', encoding='utf-8') as f:
#             reservas = json.load(file)  # Isso deve carregar o JSON e converter para um dicionário/lista
#             return reservas.get('reservas', [])  # Certifique-se de retornar a lista de reservas, caso exista
#     except FileNotFoundError:
#         return []  # Se o arquivo não for encontrado, retorna uma lista vazia
#     except json.JSONDecodeError:
#         return []  # Se o JSON estiver mal formatado, retorna uma lista vazia
def ler_moradores():
    with open('json/moradores.json', 'r', encoding='utf-8') as file:
        moradores = json.load(file)  # Carrega diretamente a lista de moradores
        return moradores
def ler_espacos():
    with open('json/espacos.json', 'r', encoding='utf-8') as file:
        return json.load(file)

#########################################################################################################

# Função auxiliar para salvar dados no arquivo JSON
def salvar_reservas(reservas, proximo_id):
    # Estrutura do JSON com as reservas e o próximo ID
    data_to_save = {
        "reservas": reservas,
        "proximo_id": proximo_id  # Armazena o próximo ID disponível para uma nova reserva
    }

    # Salva no arquivo JSON
    with open('json/reservas.json', 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, indent=3, ensure_ascii=False)


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
        # Gerar o ID do morador
               
        # Verifica a disponibilidade
        validar_disponibilidade(espaco_id, data_reserva)

        # Valida a descrição
        descricao = dados.get("descricao")
        print(f"Descricao recebida: {descricao}")  # Adicionando um log para depuração
        if descricao is None or descricao.strip() == "":
            return jsonify({"erro": "O campo 'descricao' é obrigatório!"}), 400

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

        # Gera o ID do morador a partir do apartamento e bloco
        id_morador = f"{apartamento}{bloco}"

        # Lê a lista de moradores do arquivo
        moradores = ler_moradores()

        # Verifica se o morador já existe
        if any(morador["apartamento"] == apartamento and morador["bloco"] == bloco for morador in moradores):
            return jsonify({"erro": f"Morador com apartamento {apartamento} e bloco {bloco} já existe."}), 400

        # Cria o morador e adiciona na lista
        novo_morador = Morador(nome, apartamento, bloco)

        # Adiciona o novo morador à lista
        moradores.append({"nome": novo_morador.nome, "apartamento": novo_morador.apartamento, "bloco": novo_morador.bloco})

        # Salva os moradores atualizados no arquivo
        salvar_moradores(moradores)

        return jsonify({"mensagem": f"Morador {novo_morador.nome} adicionado com sucesso!", "id": novo_morador.id}), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao processar a solicitação."}), 500


# @app.route('/moradores', methods=['POST'])
# def adicionar_morador():
#     try:
#         dados = request.get_json()

#         # Valida os dados recebidos
#         nome = dados.get("nome")
#         apartamento = dados.get("apartamento")
#         bloco = dados.get("bloco")

#         # Validações usando as funções reaproveitadas
#         if not validar_nome(nome):
#             return jsonify({"erro": "Nome inválido. O nome deve conter apenas letras e não pode estar vazio."}), 400
#         if not validar_apartamento(apartamento):
#             return jsonify({"erro": "Número de apartamento inválido. Deve estar entre 100-104, 200-204, 300-304, 400-404 ou 500-504."}), 400
#         if not validar_bloco(bloco):
#             return jsonify({"erro": "Letra do bloco inválida. Deve ser entre A e G."}), 400

#         # Cria o morador e adiciona na lista
#         novo_morador = Morador(nome, apartamento, bloco)
#         return jsonify({"mensagem": f"Morador {novo_morador.nome} adicionado com sucesso!", "id": novo_morador.id}), 201

#     except ValueError as e:
#         return jsonify({"erro": str(e)}), 400
#     except Exception as e:
#         return jsonify({"erro": "Erro ao processar a solicitação."}), 500

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

################ PUT RESERVAS ########################
# Rota para adicionar reserva
# Rota para adicionar reserva
@app.route("/reservas/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    """Atualiza uma reserva existente."""
    try:
        reservas, proximo_id = ler_reservas()

        reserva_existente = next((res for res in reservas if res["id"] == id), None)
        if not reserva_existente:
            return jsonify({"erro": "Reserva não encontrada!"}), 404

        dados = request.get_json()

        # Validações de morador, espaço e data
        morador_id = dados.get("morador_id")
        if not morador_id:
            return jsonify({"erro": "O campo 'morador_id' é obrigatório!"}), 400
        morador = validar_morador(morador_id)

        data_reserva = dados.get("data")  # Use 'data' em vez de 'data_reserva'
        if not data_reserva:
            return jsonify({"erro": "O campo 'data_reserva' é obrigatório!"}), 400
        data_reserva = validar_data(data_reserva)

        espaco_id = dados.get("espaco_id")
        if not espaco_id:
            return jsonify({"erro": "O campo 'espaco_id' é obrigatório!"}), 400
        espaco = validar_espaco(espaco_id)

        # Validação de duplicação: Verifica se já existe uma reserva para o mesmo espaço e data
        reserva_existente_no_dia = next(
            (res for res in reservas if res["espaco_id"] == espaco_id and res["data_reserva"] == data_reserva),
            None
        )
        if reserva_existente_no_dia:
            return jsonify({"erro": "Este espaço já está reservado para a data informada!"}), 400

        descricao = dados.get("descricao")
        if not descricao:
            return jsonify({"erro": "O campo 'descricao' é obrigatório!"}), 400

        nova_reserva = Reserva(
            data=data_reserva,
            espaco_id=espaco_id,
            morador_id=morador.id,
            descricao=descricao
        )

        # Atualiza os campos se fornecido
        descricao = dados.get("descricao")
        if descricao is not None:
            reserva_existente["descricao"] = descricao

        morador_id = dados.get("morador_id")
        if morador_id:
            reserva_existente["morador_id"] = morador_id

        data = dados.get("data_reserva")  # Usando 'data_reserva'
        if data:
            reserva_existente["data_reserva"] = data

        espaco_id = dados.get("espaco_id")
        if espaco_id:
            reserva_existente["espaco_id"] = espaco_id

        salvar_reservas(reservas, proximo_id)

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


    # Atualizar o morador na lista e no arquivo
    mensagem = atualizar_morador_no_arquivo(morador_id, novos_dados)
    
    if "não encontrado" in mensagem:
        return jsonify({"erro": mensagem}), 404
    
    return jsonify({"mensagem": mensagem}), 200

#  @@@@@@@@@@@@@@@@@    delete morador   @@@@@@@@@@@@@@@@@@@@@@@@
# 

@app.route('/moradores/<int:apartamento>/<bloco>', methods=['DELETE'])
def deletar_morador(apartamento, bloco):
    morador_id = f"{apartamento}{bloco}"  # Gerar ID do morador
    resultado = deletar_morador_e_reservas(morador_id)
    status_code = 200 if "erro" not in resultado else 404
    return jsonify(resultado), status_code





#________________________________________________________________________________________
#  @@@@@@@@@@@@@@@@@    delete reserva   @@@@@@@@@@@@@@@@@@@@@@@@
@app.route("/reservas/<int:id>", methods=["DELETE"])
def deletar_reserva(id):
    """Deleta uma reserva existente."""
    try:
        reservas, proximo_id = ler_reservas()

        # Verifica se a reserva existe
        reserva_existente = next((res for res in reservas if res["id"] == id), None)
        if not reserva_existente:
            return jsonify({"erro": "Reserva não encontrada!"}), 404

        # Remove a reserva da lista
        reservas = [res for res in reservas if res["id"] != id]

        # Salva as reservas atualizadas no arquivo
        salvar_reservas(reservas, proximo_id)

        return jsonify({"mensagem": "Reserva deletada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro ao deletar a reserva", "detalhes": str(e)}), 500






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
