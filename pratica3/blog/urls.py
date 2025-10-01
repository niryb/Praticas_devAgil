from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello),
    path("eco/<str:textoUrl>", views.eco),
    path("info/", views.info),
    path("home/", views.home),
    path('contato/<str:telefone>/', views.contato, name='contato'),
    path("inicial/", views.inicial, name='inicial'),
    path('about/', views.about, name='about'),  
    path('contato/<str:telefone>/', views.contato, name='contato'),
    path('', views.home, name='home')
]
