from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from biblioteca.models import Autor

class AutorAPITest(APITestCase):
    def test_list_autores_api(self):
        Autor.objects.create(nome="Autor API")
        # Ajuste o nome da rota conforme seu api_urls.py (ex: autor-list)
        url = '/api/autores/' 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Autor API")