from django.test import TestCase
from biblioteca.forms import AutorForm, SignUpForm
from django.contrib.auth import get_user_model

class FormsTest(TestCase):
    def test_autor_form_valido(self):
        form = AutorForm(data={'nome': 'Clarice Lispector'})
        self.assertTrue(form.is_valid())

    def test_signup_email_duplicado(self):
        User = get_user_model()
        User.objects.create_user(username='testuser', email='teste@email.com', password='password123')
        
        # Tenta criar formulário com o mesmo email
        form_data = {
            'username': 'novo_usuario',
            'email': 'teste@email.com',
            'password1': 'senha123',
            'password2': 'senha123'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'Este email já está em uso.')