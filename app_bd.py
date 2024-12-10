from flask import Flask, jsonify, request
from bd_conect import executar_consulta, executar_comando
from funcion_morador import validar_nome, validar_bloco, validar_apartamento
from funcion_reservas import validar_data,validar_morador,validar_espaco
from datetime import datetime
app = Flask(__name__)

def validar_morador(morador_id):
    """Valida se o morador existe no banco de dados."""
    # Divide o morador_id em apartamento e bloco
    try:
        apartamento, bloco = morador_id[:-1], morador_id[-1]  # Exemplo: '101A' -> '101', 'A'
    except IndexError:
        raise ValueError("O ID do morador deve incluir o número do apartamento e o bloco (exemplo: '101A').")
    
    # Consulta no banco de dados
    consulta_morador = "SELECT * FROM moradores WHERE apartamento = %s AND bloco = %s;"
    morador = executar_consulta(consulta_morador, (apartamento, bloco))
    
    if not morador:
        raise ValueError(f"Morador com apartamento {apartamento} e bloco {bloco} não encontrado!")
    
    return morador[0]  # Retorna o primeiro resultado encontrado

# CRUD de Moradores============================================================
@app.route('/moradores', methods=['GET'])
def listar_moradores():
    moradores = executar_consulta("SELECT * FROM moradores;")
    return jsonify(moradores)


@app.route('/moradores', methods=['POST'])
def criar_morador():
    try:
        dados = request.get_json()

        # Valida os dados recebidos
        nome = dados.get("nome")
        apartamento = dados.get("apartamento")
        bloco = dados.get("bloco")

        # Validações usando funções reutilizáveis
        if not validar_nome(nome):
            return jsonify({"erro": "Nome inválido. O nome deve conter apenas letras e não pode estar vazio."}), 400
        if not validar_apartamento(apartamento):
            return jsonify({"erro": "Número de apartamento inválido. Deve estar entre 100-104, 200-204, 300-304, 400-404 ou 500-504."}), 400
        if not validar_bloco(bloco):
            return jsonify({"erro": "Letra do bloco inválida. Deve ser entre A e G."}), 400

        # Verifica se o morador já existe no banco de dados
        query_verificar = """
            SELECT * FROM moradores
            WHERE apartamento = %s AND bloco = %s;
        """
        params_verificar = (apartamento, bloco)
        morador_existente = executar_consulta(query_verificar, params_verificar)

        if morador_existente:
            return jsonify({"erro": f"Morador com apartamento {apartamento} e bloco {bloco} já existe."}), 400

        # Insere o novo morador no banco de dados
        query_inserir = """
            INSERT INTO moradores (nome, apartamento, bloco)
            VALUES (%s, %s, %s);
        """
        params_inserir = (nome, apartamento, bloco)
        linhas_afetadas = executar_comando(query_inserir, params_inserir)

        if linhas_afetadas > 0:
            return jsonify({"mensagem": f"Morador {nome} adicionado com sucesso!"}), 201
        else:
            return jsonify({"erro": "Erro ao inserir morador no banco de dados."}), 500

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao processar a solicitação.", "detalhes": str(e)}), 500


@app.route('/moradores/<apartamento>/<bloco>', methods=['PUT'])
def atualizar_morador(apartamento, bloco):
    try:
        dados = request.get_json()

        # Valida os dados recebidos
        novo_nome = dados.get("nome")

        # Validações
        if not validar_nome(novo_nome):
            return jsonify({"erro": "Nome inválido. O nome deve conter apenas letras e não pode estar vazio."}), 400
        if not validar_apartamento(apartamento):
            return jsonify({"erro": "Número de apartamento inválido. Deve estar entre 100-104, 200-204, 300-304, 400-404 ou 500-504."}), 400
        if not validar_bloco(bloco):
            return jsonify({"erro": "Letra do bloco inválida. Deve ser entre A e G."}), 400

        # Verifica se o morador existe no banco
        query_verificar = """
            SELECT * FROM moradores
            WHERE apartamento = %s AND bloco = %s;
        """
        params_verificar = (apartamento, bloco)
        morador_existente = executar_consulta(query_verificar, params_verificar)

        if not morador_existente:
            return jsonify({"erro": f"Morador com apartamento {apartamento} e bloco {bloco} não encontrado."}), 404

        # Atualiza os dados do morador
        query_atualizar = """
            UPDATE moradores
            SET nome = %s
            WHERE apartamento = %s AND bloco = %s;
        """
        params_atualizar = (novo_nome, apartamento, bloco)
        linhas_afetadas = executar_comando(query_atualizar, params_atualizar)

        if linhas_afetadas > 0:
            return jsonify({"mensagem": f"Morador com apartamento {apartamento} e bloco {bloco} atualizado com sucesso!"}), 200
        else:
            return jsonify({"erro": "Erro ao atualizar o morador no banco de dados."}), 500

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro ao processar a solicitação.", "detalhes": str(e)}), 500


@app.route('/moradores/<apartamento>/<bloco>', methods=['DELETE'])
def deletar_morador(apartamento, bloco):
    try:
        # Validações de entrada
        if not validar_apartamento(apartamento):
            return jsonify({"erro": "Número de apartamento inválido. Deve estar entre 100-104, 200-204, 300-304, 400-404 ou 500-504."}), 400
        if not validar_bloco(bloco):
            return jsonify({"erro": "Letra do bloco inválida. Deve ser entre A e G."}), 400

        # Verifica se o morador existe no banco
        query_verificar = """
            SELECT * FROM moradores
            WHERE apartamento = %s AND bloco = %s;
        """
        params_verificar = (apartamento, bloco)
        morador_existente = executar_consulta(query_verificar, params_verificar)

        if not morador_existente:
            return jsonify({"erro": f"Morador com apartamento {apartamento} e bloco {bloco} não encontrado."}), 404

        # Deleta o morador
        query_deletar = """
            DELETE FROM moradores
            WHERE apartamento = %s AND bloco = %s;
        """
        params_deletar = (apartamento, bloco)
        linhas_afetadas = executar_comando(query_deletar, params_deletar)

        if linhas_afetadas > 0:
            return jsonify({"mensagem": f"Morador com apartamento {apartamento} e bloco {bloco} deletado com sucesso!"}), 200
        else:
            return jsonify({"erro": "Erro ao deletar o morador no banco de dados."}), 500

    except Exception as e:
        return jsonify({"erro": "Erro ao processar a solicitação.", "detalhes": str(e)}), 500

# CRUD de Moradores=======================================================




# CRUD de Reservas---------------------------------------
@app.route('/reservas', methods=['GET'])
def listar_reservas():
    """Lista todas as reservas com a data formatada como dd-mm-AA."""
    reservas = executar_consulta("SELECT * FROM reservas;")
    
    # Formata os resultados
    reservas_formatadas = []
    for reserva in reservas:
        reserva_formatada = dict(reserva)  # Converte para dicionário se necessário
        if 'data_reserva' in reserva_formatada and reserva_formatada['data_reserva']:
            # Converte a data para o formato dd-mm-AA
            reserva_formatada['data_reserva'] = datetime.strptime(
                str(reserva_formatada['data_reserva']), "%Y-%m-%d"
            ).strftime("%d-%m-%y")
        reservas_formatadas.append(reserva_formatada)
    
    return jsonify(reservas_formatadas)

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

        # Verifica se o morador existe no banco de dados, buscando pelo formato correto do morador_id
        morador_query = "SELECT * FROM moradores WHERE CONCAT(apartamento, bloco) = %s"
        morador = executar_consulta(morador_query, (morador_id,))
        if not morador:
            return jsonify({"erro": "Morador não encontrado!"}), 404

        # Valida a data da reserva
        data_reserva = dados.get("data")
        if not data_reserva:
            return jsonify({"erro": "O campo 'data' é obrigatório!"}), 400
        # Supondo que você tenha uma função de validação de formato de data
        if not validar_data(data_reserva):
            return jsonify({"erro": "Data inválida!"}), 400

        # Valida o espaço
        espaco_id = dados.get("espaco_id")
        if not espaco_id:
            return jsonify({"erro": "O campo 'espaco_id' é obrigatório!"}), 400

        # Verifica se o espaço existe no banco de dados
        espaco_query = "SELECT * FROM espacos WHERE espaco_id = %s"
        espaco = executar_consulta(espaco_query, (espaco_id,))
        if not espaco:
            return jsonify({"erro": "Espaço não encontrado!"}), 404

        # Verifica se o espaço está disponível na data
        disponibilidade_query = """
            SELECT * FROM reservas 
            WHERE espaco_id = %s AND data_reserva = %s;
        """
        reservas_existentes = executar_consulta(disponibilidade_query, (espaco_id, data_reserva))
        if reservas_existentes:
            return jsonify({"erro": "O espaço já está reservado para a data informada."}), 400

        # Valida a descrição
        descricao = dados.get("descricao")
        if descricao is None or descricao.strip() == "":
            return jsonify({"erro": "O campo 'descricao' é obrigatório!"}), 400

        # Cria a reserva
        insert_reserva_query = """
            INSERT INTO reservas (espaco_id, data_reserva, descricao)
            VALUES (%s, %s, %s) RETURNING id_reservas;
        """
        params = (espaco_id, data_reserva, descricao)
        resultado = executar_comando(insert_reserva_query, params)

        # O retorno da função de execução do comando pode ser diretamente o ID gerado.
        reserva_id = resultado  # Ajustando para pegar diretamente o valor retornado
        if not reserva_id:
            return jsonify({"erro": "Falha ao criar reserva."}), 500

        # Retorna a nova reserva
        return jsonify({
            "mensagem": "Reserva criada com sucesso!",
            "reserva_id": reserva_id
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500


@app.route("/reservas/<int:reserva_id>", methods=["PUT"])
def atualizar_reserva(reserva_id):
    """Atualiza uma reserva existente."""
    try:
        # Verifica se a reserva existe
        consulta_reserva_query = "SELECT * FROM reservas WHERE id_reservas = %s"
        reserva_existente = executar_consulta(consulta_reserva_query, (reserva_id,))
        if not reserva_existente:
            return jsonify({"erro": "Reserva não encontrada!"}), 404

        # Obtém os dados da requisição
        dados = request.get_json()

        # Valida o morador
        morador_id = dados.get("morador_id")
        if not morador_id:
            return jsonify({"erro": "O campo 'morador_id' é obrigatório!"}), 400

        # Verifica se o morador existe no banco de dados
        morador_query = "SELECT * FROM moradores WHERE CONCAT(apartamento, bloco) = %s"
        morador = executar_consulta(morador_query, (morador_id,))
        if not morador:
            return jsonify({"erro": "Morador não encontrado!"}), 404

        # Valida a data da reserva
        data_reserva = dados.get("data")
        if not data_reserva:
            return jsonify({"erro": "O campo 'data' é obrigatório!"}), 400
        if not validar_data(data_reserva):
            return jsonify({"erro": "Data inválida!"}), 400

        # Valida o espaço
        espaco_id = dados.get("espaco_id")
        if not espaco_id:
            return jsonify({"erro": "O campo 'espaco_id' é obrigatório!"}), 400

        # Verifica se o espaço existe no banco de dados
        espaco_query = "SELECT * FROM espacos WHERE espaco_id = %s"
        espaco = executar_consulta(espaco_query, (espaco_id,))
        if not espaco:
            return jsonify({"erro": "Espaço não encontrado!"}), 404

        # Verifica se o espaço está disponível na data, ignorando a própria reserva
        disponibilidade_query = """
            SELECT * FROM reservas 
            WHERE espaco_id = %s AND data_reserva = %s AND id_reservas != %s;
        """
        reservas_existentes = executar_consulta(disponibilidade_query, (espaco_id, data_reserva, reserva_id))
        if reservas_existentes:
            return jsonify({"erro": "O espaço já está reservado para a data informada."}), 400

        # Valida a descrição
        descricao = dados.get("descricao")
        if descricao is None or descricao.strip() == "":
            return jsonify({"erro": "O campo 'descricao' é obrigatório!"}), 400

        # Atualiza a reserva no banco de dados
        update_reserva_query = """
            UPDATE reservas
            SET espaco_id = %s, data_reserva = %s, descricao = %s
            WHERE id_reservas = %s;
        """
        params = (espaco_id, data_reserva, descricao, reserva_id)
        linhas_afetadas = executar_comando(update_reserva_query, params)

        if linhas_afetadas == 0:
            return jsonify({"erro": "Nenhuma alteração realizada!"}), 400

        # Retorna os dados atualizados
        return jsonify({
            "mensagem": "Reserva atualizada com sucesso!",
            "reserva": {
                "id_reservas": reserva_id,
                "espaco_id": espaco_id,
                "data_reserva": data_reserva,
                "descricao": descricao
            }
        }), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500


@app.route('/reservas/<int:id_reserva>', methods=['DELETE'])
def deletar_reserva(id_reserva):
    """Deleta uma reserva existente após validação."""
    try:
        # Verifica se a reserva existe
        consulta_reserva = "SELECT * FROM reservas WHERE id_reservas = %s;"
        reserva_existente = executar_consulta(consulta_reserva, (id_reserva,))
        
        if not reserva_existente:
            return jsonify({"erro": "Reserva não encontrada!"}), 404

        # Deleta a reserva
        query = """
            DELETE FROM reservas
            WHERE id_reservas = %s;
        """
        params = (id_reserva,)
        linhas_afetadas = executar_comando(query, params)

        if linhas_afetadas == 0:
            return jsonify({"erro": "Erro ao deletar a reserva, nenhuma linha foi afetada."}), 500

        return jsonify({"mensagem": f"Reserva com ID {id_reserva} deletada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500


# CRUD de Reservas-------------------------------------------------


@app.route('/espacos', methods=['GET'])
def listar_espacos():
    """Lista todos os espaços cadastrados no banco de dados."""
    try:
        # Consulta para buscar todos os espaços
        query = "SELECT * FROM espacos;"
        espacos = executar_consulta(query)

        # Verifica se existem espaços cadastrados
        if not espacos:
            return jsonify({"mensagem": "Nenhum espaço encontrado."}), 404

        return jsonify(espacos), 200

    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor", "detalhes": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)
