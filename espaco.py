import json

lista_espacos = []

class Espaco:
    _id_counter = 1  # Contador interno para gerar IDs únicos

    def __init__(self, tipo, nome=None, id=None):
        if id is not None:
            self.id = id  # Usa o ID fornecido, caso exista (para dados carregados)
            Espaco._id_counter = max(Espaco._id_counter, id + 1)  # Ajusta o contador
        else:
            self.id = Espaco._id_counter
            Espaco._id_counter += 1
        self.tipo = tipo
        self.nome = nome if nome else tipo
        lista_espacos.append(self)



    @staticmethod
    def inicializar_espacos():
        """Carrega os espaços a partir do JSON ou cria os padrões, garantindo que não haja duplicados."""
        try:
            with open('json/espacos.json', 'r', encoding='utf-8') as file:
                dados = json.load(file)
                ids_existentes = {espaco.id for espaco in lista_espacos}  # IDs já carregados
                
                # Processa espaços do JSON
                for espaco_dict in dados:
                    # Define o tipo fixo como "Churrasqueira"
                    tipo = espaco_dict.get("tipo", "Churrasqueira")
                    nome = espaco_dict.get("nome", f"Espaço de Churrasco {espaco_dict['id']}")
                    id_espaco = espaco_dict["id"]
                    
                    # Verificar se o ID já existe antes de criar o espaço
                    if id_espaco not in ids_existentes:
                        Espaco(tipo, nome, id_espaco)
        except FileNotFoundError:
            Espaco.criar_espacos_padrao()
            Espaco.salvar_em_json()

    # @staticmethod
    # def inicializar_espacos():
    #     """Carrega os espaços a partir do JSON ou cria os padrões, garantindo que não haja duplicados."""
    #     try:
    #         with open('json/espacos.json', 'r', encoding='utf-8') as file:
    #             dados = json.load(file)
    #             ids_existentes = {espaco.id for espaco in lista_espacos}  # IDs já carregados
                
    #             # Processa espaços do JSON
    #             espacos = []
    #             for espaco_dict in dados:
    #                 # Define o tipo fixo como "Churrasqueira"
    #                 tipo = "Churrasqueira"
    #                 nome = espaco_dict.get("nome", "Espaço de Churrasco")  # Nome pode ser ajustado
    #                 espaco = Espaco(tipo, nome, espaco_dict["id"])
                    
    #                 # Verificar se o ID já existe antes de adicionar
    #                 if espaco.id not in ids_existentes:
    #                     espacos.append(espaco)
                
    #             lista_espacos.extend(espacos)  # Atualiza a lista global
    #     except FileNotFoundError:
    #         Espaco.criar_espacos_padrao()
    #         Espaco.salvar_em_json()

    @staticmethod
    def criar_espacos_padrao():
        """Cria o salão de festas e cinco churrasqueiras."""
        Espaco("Salão de Festas", "Salão de Festas")  # Adiciona o salão de festas
        for i in range(1,6):  # Cria cinco churrasqueiras com tipo fixo
            Espaco("Churrasqueira", f"Espaço de Churrasco {i}")  # Define tipo e nome fixos

    @staticmethod
    def salvar_em_json():
        """Salva a lista de espaços no arquivo JSON."""
        with open('json/espacos.json', 'w', encoding='utf-8') as file:
            json.dump([espaco.__dict__ for espaco in lista_espacos], file, indent=3, ensure_ascii=False)

