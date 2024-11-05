from espaco import Espaco, lista_espacos
from morador import Morador, lista_moradores
from reserva import Reserva, lista_reservas
from funcion import carregar_dados,adicionar_morador,fazer_reserva



# Carregar dados do arquivo
carregar_dados()



def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Adicionar Morador")
        print("2. Fazer Reserva")
        print("3. Listar Moradores")
        print("4. Listar Reservas")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            adicionar_morador()
        elif opcao == '2':
            fazer_reserva()
        elif opcao == '3':
            print("\nMoradores cadastrados:")
            for morador in lista_moradores:
                print(f"ID: {morador.id}, Nome: {morador.nome}")
        elif opcao == '4':
            print("\nReservas:")
            for reserva in lista_reservas:
                print(f"Morador ID: {reserva.morador_id}, Espaço ID: {reserva.espaco_id}, Data: {reserva.data}")
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida, por favor escolha novamente.")

# Executa o menu
menu()
1