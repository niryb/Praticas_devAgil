from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Autor, Editora, Livro

# ---- Formulário Autor ----
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do autor'
            })
        }


# ---- Formulário Editora ----
class EditoraForm(forms.ModelForm):
    class Meta:
        model = Editora
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da editora'
            })
        }


# ---- Formulário Livro ----
class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'isbn', 'titulo', 'autor', 'editora',
            'publicacao', 'preco', 'estoque'
        ]
        widgets = {
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 9781234567890'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do livro'
            }),
            'autor': forms.Select(attrs={'class': 'form-select'}),
            'editora': forms.Select(attrs={'class': 'form-select'}),
            'publicacao': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ex: 49.90'
            }),
            'estoque': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantidade em estoque'
            }),
        }

# ---- Formulário login ----
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'email@exemplo.com', 'class': 'input-text'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'input-text'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'input-text'}))
