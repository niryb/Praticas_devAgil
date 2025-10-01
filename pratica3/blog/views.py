from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import date

# Create your views here.
def hello(request):
    return HttpResponse("Bem-vindo ao meu blog!")

def eco(request, textoUrl):
    return HttpResponse(f"Você digitou: {textoUrl}")

def info(request):
    informacoes = { "disciplina": "RAD",
     "framework": "Django",
     "semestre": "2025.2"
    }
    return JsonResponse(informacoes)

def home(request):
    numero = 3
    is_logged_in = True
    idade = 30
    role = "admin"
    produtos = [
        {"nome": "Camiseta", "preco": 29.99},
        {"nome": "Calça Jeans", "preco": 79.90},
        {"nome": "Tênis", "preco": 150.00},
        {"nome": "Jaqueta", "preco": 120.50},
        {"nome": "Óculos de sol", "preco": 45.99}
    ]
    contexto = { "usuario": "Nirielly e Leticia",
     "disciplina": "Django",
     "data_atual": date.today(),
     "semestre": "2025.2",
     "is_logged_in":is_logged_in,
     "idade":idade,
     "role":role,
     "produtos":produtos,
     "numero":numero
    }
    return render(request, "home.html", contexto)

#view para a página de contato
def contato(request, telefone):
    contexto = {
        "telefone": telefone,
    }
    return render(request, "contato.html", contexto)

def inicial(request):
    contexto = {
        "usuario": "Nirielly e Leticia",
        "disciplina": "Django",
        "data_atual": date.today(),
        "semestre": "2025.2",
    }
    return render(request, "inicial.html", contexto)

def about(request):
    return render(request, "about.html")
