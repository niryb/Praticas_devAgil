from django.test import TestCase
from django.urls import reverse
from biblioteca.models import Autor

class ViewsTest(TestCase):
    def test_acesso_dashboard(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_listar_autores_sucesso(self):
        Autor.objects.create(nome="Autor Exemplo")
        # A rota 'listar' recebe a entidade como parâmetro
        url = reverse('listar', kwargs={'entidade': 'autor'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Autor Exemplo")

    def test_entidade_invalida(self):
        url = reverse('listar', kwargs={'entidade': 'inexistente'})
        response = self.client.get(url)
        self.assertContains(response, 'Entidade "inexistente" inválida.')