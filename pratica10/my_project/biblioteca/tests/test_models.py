from django.test import TestCase
from biblioteca.models import Autor, Editora, Livro
import datetime

class BibliotecaModelsTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nome="Machado de Assis")
        self.editora = Editora.objects.create(nome="Editora Teste")

    def test_criacao_autor(self):
        self.assertEqual(str(self.autor), "Machado de Assis")

    def test_criacao_livro(self):
        livro = Livro.objects.create(
            isbn="1234567890123",
            autor=self.autor,
            titulo="Dom Casmurro",
            publicacao=datetime.date.today(),
            preco=50.00,
            estoque=10,
            editora=self.editora
        )
        self.assertEqual(str(livro), "Dom Casmurro")
        self.assertEqual(livro.autor.nome, "Machado de Assis")