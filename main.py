from espaco import lista_espacos
from morador import lista_moradores
from reserva import lista_reserva,Reserva
from funcion_reservas import carregar_dados, criar_reserva
from funcion_morador import adicionar_morador, listar_moradores

carregar_dados()






# carregar_dados()
# def validar_morador_test(morador_id):
#     """Verifica se o morador existe na lista de moradores."""
#     morador = next((m for m in lista_moradores if m.id == morador_id), None)
#     if not morador:
#         print("Morador não encontrado!")
#         return None  # Retorna None se não encontrar o morador
#     else:
#         return morador  # Retorna o objeto morador se encontrado

# # Teste manual
# morador_id = "101A"
# print(lista_moradores)
# # Valida o morador
# morador = validar_morador_test(morador_id)
# if morador is None:
#     print("Morador não encontrado parte 2!")  # Executa essa parte se o morador não for encontrado
# else:
#     print(f"Morador encontrado: {morador.id}, {morador.nome}")  # Caso o mor
# # validar_morador_test("101A")

# Verifique o conteúdo da lista de moradores





# Carregar dados do arquivo

# Criando uma reserva manual
# reserva_teste = Reserva(
#     data="12-12-2024",  # Data da reserva
#     espaco_id= 1,  # ID do espaço
#     morador_id= "101A",  # ID do morador
#     descricao="Evento de Natal"  # Descrição opcional
# )

# # Salvando a reserva no arquivo JSON
# salvar_reservas(reserva_teste)
# print("Lista de moradores no sistema:")  # Imprime uma mensagem no console
# for morador in lista_moradores:
#     print(morador)
 #Exemplo de como adicionar uma reserva
# nova_reserva = Reserva(espaco_id=1, morador_id="101A", data="12-12-34", descricao="Reserva de teste")
# lista_reserva.append(nova_reserva)

# # Chama a função para salvar as reservas no arquivo
# salvar_reservas()
# print(lista_moradores)
def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Adicionar Morador")
        print("2. Fazer Reserva")
        print("3. Listar Moradores")
        print("4. Listar Reservas")
        print("5. Deletar Morador e Reservas")
        print("6. Listar Espaços")
        print("7. Sair")            
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            adicionar_morador()
        elif opcao == '2':
            criar_reserva()
        elif opcao == '3':
            listar_moradores()
            # print("\nMoradores cadastrados:")
            # for morador in lista_moradores:
            #     print(f"ID: {morador.id}, Nome: {morador.nome}")
        elif opcao == '4':           
            print("\nReservas:")
            for reserva in lista_reserva:
                print(f"Morador ID: {reserva.morador_id}, ID:{reserva.espaco_id}|{reserva.descricao}|  Data: {reserva.data}")
        elif opcao == '5':
            pass
            #deletar_morador()
        elif opcao == '6':
           
            print("\nEspaços:")
            for espaco in lista_espacos:
                print(f"{espaco.id},{espaco.tipo}|{espaco.nome}|")
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida, por favor escolha novamente.")

# Executa o menu






menu()
