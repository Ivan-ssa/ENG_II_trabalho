from espaco import Espaco, lista_espacos
from morador import Morador, lista_moradores
from reserva import Reserva, lista_reserva
from funcion_reservas import carregar_dados, criar_reserva,salvar_reservas
from funcion_morador import adicionar_morador, deletar_morador


# Carregar dados do arquivo
carregar_dados()
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
            print("\nMoradores cadastrados:")
            for morador in lista_moradores:
                print(f"ID: {morador.id}, Nome: {morador.nome}")
        elif opcao == '4':
           
            print("\nReservas:")
            for reserva in lista_reserva:
                print(f"Morador ID: {reserva.morador_id}, ID:{reserva.espaco_id}|{reserva.descricao}|  Data: {reserva.data}")
        elif opcao == '5':
            deletar_morador()
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
