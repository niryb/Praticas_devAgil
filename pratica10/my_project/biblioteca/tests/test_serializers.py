from django.test import TestCase
from biblioteca.serializers import AutorSerializer

class SerializerTest(TestCase):
    def test_autor_serializer_validacao_customizada(self):
        # Você implementou que se o nome for '0' deve dar erro
        data = {'nome': '0'}
        serializer = AutorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['nome'][0], "Validação teste")

    def test_autor_serializer_valido(self):
        data = {'nome': 'J.K. Rowling'}
        serializer = AutorSerializer(data=data)
        self.assertTrue(serializer.is_valid())