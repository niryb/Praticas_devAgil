from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from .models import Autor, Editora, Livro
from .forms import AutorForm, EditoraForm, LivroForm, SignUpForm, SignInForm
from django.shortcuts import render
from django.core.exceptions import PermissionDenied


def base_view(request):
    return render(request, 'biblioteca/base.html')

def dashboard(request):
    return render(request, 'biblioteca/dashboard.html')

# Mapeia entidade → (modelo, form)
MAPEAMENTO = {
    'autor': (Autor, AutorForm),
    'editora': (Editora, EditoraForm),
    'livro': (Livro, LivroForm),
}

def listar_objetos(request, entidade):
    modelo, _ = MAPEAMENTO.get(entidade, (None, None))
    if not modelo:
        return render(request, 'biblioteca/erro.html', {'mensagem': f'Entidade "{entidade}" inválida.'})
    # É uma boa prática ordenar antes de paginar
    objetos_list = modelo.objects.all().order_by('id')
    page_obj = None
    is_paginated = False

    # Aplica paginação apenas para a entidade 'livro'
    if entidade == 'livro':
        paginator = Paginator(objetos_list, 10) # 10 livros por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context_objetos = page_obj # O template irá iterar sobre 'page_obj'
        is_paginated = True
    else:
        context_objetos = objetos_list # Entidades sem paginação
    
    return render(request, 'biblioteca/lista.html', {
        'objetos': context_objetos, 
        'entidade': entidade,
        'is_paginated': is_paginated, # Flag para o template
        'page_obj': page_obj # Objeto Paginator para os controles
    })

@login_required
def criar_objeto(request, entidade):
    _, Form = MAPEAMENTO.get(entidade, (None, None))
    if not Form:
        return render(request, 'biblioteca/erro.html', {'mensagem': f'Entidade "{entidade}" inválida.'})
    
    # --- VERIFICAÇÃO DE PERMISSÃO ---
    if entidade == 'livro' and not request.user.has_perm('biblioteca.add_livro'):
        raise PermissionDenied("Você não tem permissão para adicionar livros.")
    # --------------------------------

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar', entidade=entidade)
    else:
        form = Form()

    return render(request, 'biblioteca/form.html', {'form': form, 'entidade': entidade})

@login_required
def editar_objeto(request, entidade, pk):
    modelo, Form = MAPEAMENTO.get(entidade, (None, None))
    if not modelo:
        return render(request, 'biblioteca/erro.html', {'mensagem': f'Entidade "{entidade}" inválida.'})
    
    # --- VERIFICAÇÃO DE PERMISSÃO ---
    if entidade == 'livro' and not request.user.has_perm('biblioteca.change_livro'):
        raise PermissionDenied("Você não tem permissão para editar livros.")
    # --------------------------------
    
    obj = get_object_or_404(modelo, pk=pk)
    if request.method == 'POST':
        form = Form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('listar', entidade=entidade)
    else:
        form = Form(instance=obj)
    return render(request, 'biblioteca/form.html', {'form': form, 'entidade': entidade})


def deletar_objeto(request, entidade, pk):
    modelo, _ = MAPEAMENTO.get(entidade, (None, None))
    if not modelo:
        return render(request, 'biblioteca/erro.html', {'mensagem': f'Entidade "{entidade}" inválida.'})
    
    # --- VERIFICAÇÃO DE PERMISSÃO ---
    if entidade == 'livro' and not request.user.has_perm('biblioteca.delete_livro'):
        raise PermissionDenied("Você não tem permissão para excluir livros.")
    # --------------------------------

    obj = get_object_or_404(modelo, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('listar', entidade=entidade)
    return render(request, 'biblioteca/confirmar_exclusao.html', {'objeto': obj, 'entidade': entidade})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'biblioteca/sign_up.html', {'form': form})


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) #cria a sessão do usuário, define request.user para esse usuário. Cria cookie de sessão.
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = SignInForm()
    
    return render(request, 'biblioteca/sign_in.html', {'form':form})


def logout_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    logout(request)
    return redirect('signin')