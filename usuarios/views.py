from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import UsuariosForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from allauth.socialaccount.models import SocialAccount


# Create your views here.
def conta(request):
    template = loader.get_template('usuarios/conta.html')
    return HttpResponse(template.render({}, request))

def listar(request):
    template = loader.get_template('usuarios/listar.html')
    return HttpResponse(template.render({}, request))

def cadastrarUsuarios(request):
    if request.POST:
        form = UsuariosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('Salvo com sucesso!')
            return redirect('index')
        else:
            return redirect('cadastrarUsuarios')
    else:
        template = loader.get_template('usuarios/inserir_usuarios.html')
        context = {
            'form': UsuariosForm(),
        }
        return HttpResponse(template.render(context, request))
    
# Login com Google - configura via django-allauth
def google_login(request):
    # A lógica de login com o Google será gerenciada pelo `django-allauth`
    return redirect('account_login')  # Redireciona para a página de login configurada pelo `allauth`

# Visualização do perfil do usuário
@login_required
def perfil(request):
    # Recupera as informações do usuário logado
    user_data = {
        'nome': request.user.username,
        'email': request.user.email,
        'social_accounts': SocialAccount.objects.filter(user=request.user)
    }
    return render(request, 'usuarios/perfil.html', {'user_data': user_data})

def inserir_usuario(request):
    if request.method == 'POST':
        form = UsuariosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = UsuariosForm()
    return render(request, 'usuarios/inserir_usuarios.html', {'form': form})