from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Livro, Autor, Editora
from .serializers import LivroSerializer, AutorSerializer, EditoraSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Endpoint de login que retorna os dados do usuário autenticado"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    login(request, user)
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_analista': user.groups.filter(name='Analistas de Cadastro').exists()
    }, status=status.HTTP_200_OK)


class IsAnalista(permissions.BasePermission):
    """Permissão customizada: apenas usuários do grupo 'Analistas de Cadastro' podem criar"""
    
    def has_permission(self, request, view):
        # Leitura disponível para qualquer um
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Criação apenas para membros do grupo 'Analistas de Cadastro'
        if request.method == 'POST':
            if request.user and request.user.is_authenticated:
                return request.user.groups.filter(name='Analistas de Cadastro').exists()
            return False
        
        # Outras ações (PUT, DELETE) são proibidas
        return False

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsAnalista]

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [permissions.AllowAny]

class EditoraViewSet(viewsets.ModelViewSet):
    queryset = Editora.objects.all()
    serializer_class = EditoraSerializer
    permission_classes = [permissions.AllowAny]