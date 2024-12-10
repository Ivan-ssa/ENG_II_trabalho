from espaco import lista_espacos
from morador import lista_moradores
from reserva import lista_reserva,Reserva
from funcion_reservas import carregar_dados, criar_reserva
from funcion_morador import adicionar_morador, listar_moradores

carregar_dados()







def menu_1():
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
menu_1()
