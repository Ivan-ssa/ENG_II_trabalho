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
        """Verifica se o arquivo existe e inicializa os espaços se estiver vazio."""
        try:
            with open('json/espacos.json', 'r', encoding='utf-8') as file:
                espacos_salvos = json.load(file)
                tipos_existentes = {espaco["tipo"] for espaco in lista_espacos}
                for espaco in espacos_salvos:
                    if espaco["tipo"] not in tipos_existentes:
                        lista_espacos.append(Espaco(espaco["tipo"]))
        except FileNotFoundError:
            # Se o arquivo não existir, cria os espaços padrão
            Espaco.criar_espacos_padrao()
            Espaco.salvar_em_json()

    @staticmethod
    def criar_espacos_padrao():
        """Cria o salão de festas e cinco churrasqueiras."""
        Espaco("Salão de Festas")  # Adiciona o salão de festas
        for i in range(1, 6):  # Cria cinco churrasqueiras com nomes únicos
            Espaco(f"Churrasqueira {i}")

    @staticmethod
    def salvar_em_json():
        """Salva a lista de espaços no arquivo JSON."""
        with open('json/espacos.json', 'w', encoding='utf-8') as file:
            json.dump([espaco.__dict__ for espaco in lista_espacos], file, indent=3, ensure_ascii=False)

