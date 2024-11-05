import unittest
from morador import Morador, lista_moradores  # Certifique-se de importar a lista

class TestMorador(unittest.TestCase):

    def setUp(self):
        # Limpa a lista de moradores antes de cada teste
        lista_moradores.clear()

    def test_criar_morador(self):
        # Testa a criação de um morador com dados válidos
        morador = Morador("João da Silva", "101", "A")
        self.assertIn(morador, lista_moradores)  # Verifica se o morador foi adicionado à lista
        self.assertEqual(morador.nome, "João da Silva")
        self.assertEqual(morador.apartamento, "101")
        self.assertEqual(morador.bloco, "A")

    def test_nome_vazio(self):
        # Testa se um nome vazio levanta uma exceção
        with self.assertRaises(ValueError):
            Morador("", "101", "A")

    def test_apartamento_invalido(self):
        # Testa se o apartamento não pode ser vazio ou negativo
        with self.assertRaises(ValueError):
            Morador("Maria Oliveira", "-1", "B")  # Apartamento negativo
        with self.assertRaises(ValueError):
            Morador("Pedro Alves", "", "C")  # Apartamento vazio

    def test_bloco_invalido(self):
        # Testa se o bloco não pode ser vazio
        with self.assertRaises(ValueError):
            Morador("Flavio", "202", "")  # Bloco vazio

if __name__ == '__main__':
    unittest.main()

"""
coamndo do teste unitario

python -m unittest discover -s test -p "test_*.py"

"""