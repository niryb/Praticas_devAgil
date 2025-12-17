from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import LivroViewSet, AutorViewSet, EditoraViewSet, login_view

router = SimpleRouter()
router.register(r'livros', LivroViewSet)
router.register(r'autores', AutorViewSet)
router.register(r'editoras', EditoraViewSet)

app_name = 'api'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]