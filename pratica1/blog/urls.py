from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello),
    path("eco/<str:textoUrl>", views.eco),
    path("info/", views.info)
]
