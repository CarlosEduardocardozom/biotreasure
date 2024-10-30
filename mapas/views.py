from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from .models import PontosForm, PontosTuristico, RotasForm, Rota
from django.core.serializers import serialize

# Renderizar a página inicial dos mapas
def mapas(request):
    template = loader.get_template('mapas/index.html')
    return HttpResponse(template.render({}, request))

# Cadastrar Ponto Turístico
def cadastrarPonto(request):
    if request.method == 'POST':
        form = PontosForm(request.POST, request.FILES)
        if form.is_valid():
            ponto = form.save()  # Salva o ponto
            # Retorna o JSON do ponto cadastrado
            return JsonResponse({
                'id': ponto.id,
                'nome': ponto.nome,
                'latitude': ponto.latitude,
                'longitude': ponto.longitude,
                'imagem': ponto.imagem.url if ponto.imagem else None
            })
        else:
            return render(request, 'mapas/pontos/inserirPontos.html', {'form': form, 'ponto_criado': False})
    return render(request, 'mapas/pontos/inserirPontos.html', {'form': PontosForm()})

# Listar Pontos Turísticos
def listarPontos(request):
    pontos = PontosTuristico.objects.all()
    pontos_json = serialize('json', pontos, fields=('nome', 'latitude', 'longitude', 'imagem'))
    
    sucesso_editar = request.GET.get('sucesso_editar', False)
    sucesso_deletar = request.GET.get('sucesso_deletar', False)

    context = {
        'pontos': pontos,
        'sucesso_editar': sucesso_editar,
        'sucesso_deletar': sucesso_deletar
    }
    
    template = loader.get_template('mapas/pontos/listarPontos.html')
    return HttpResponse(template.render(context, request))

# View para retornar todos os pontos turísticos em JSON
def listarPontosJSON(request):
    pontos = PontosTuristico.objects.all().values('nome', 'latitude', 'longitude', 'imagem')
    pontos_list = list(pontos)  # Converte o queryset para uma lista
    return JsonResponse(pontos_list, safe=False)

# Editar Ponto Turístico
def editarPonto(request, id):
    ponto = get_object_or_404(PontosTuristico, id=id)
    if request.method == 'POST':
        form = PontosForm(request.POST, request.FILES, instance=ponto)
        if form.is_valid():
            form.save()
            url = reverse('listarPontos') + '?sucesso_editar=True'
            return HttpResponseRedirect(url)
    else:
        form = PontosForm(instance=ponto)
    
    template = loader.get_template('mapas/pontos/editarPontos.html')
    context = {
        'form': form,
        'ponto': ponto
    }
    return HttpResponse(template.render(context, request))

# Deletar Ponto Turístico
def deletarPonto(request, id):
    ponto = get_object_or_404(PontosTuristico, id=id)
    ponto.delete()
    url = reverse('listarPontos') + '?sucesso_deletar=True'
    return HttpResponseRedirect(url)

# Cadastrar Rotas
def cadastrarRotas(request):
    if request.method == 'POST':
        form = RotasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cadastrarRotas')
    template = loader.get_template('mapas/rotas/inserirRotas.html')
    context = {'form': RotasForm()}
    return HttpResponse(template.render(context, request))

# Listar Rotas
def listarRotas(request):
    rotas = Rota.objects.all()
    
    sucesso_editar = request.GET.get('sucesso_editar', False)
    sucesso_deletar = request.GET.get('sucesso_deletar', False)

    context = {
        'rotas': rotas,
        'sucesso_editar': sucesso_editar,
        'sucesso_deletar': sucesso_deletar
    }
    
    template = loader.get_template('mapas/rotas/listarRotas.html')
    return HttpResponse(template.render(context, request))

# Editar Rota
def editarRota(request, id):
    rota = get_object_or_404(Rota, id=id)
    if request.method == 'POST':
        form = RotasForm(request.POST, request.FILES, instance=rota)
        if form.is_valid():
            form.save()     
            url = reverse('listarRotas') + '?sucesso_editar=True'
            return HttpResponseRedirect(url)
    else:
        form = RotasForm(instance=rota)
    
    template = loader.get_template('mapas/rotas/editarRota.html')
    context = {
        'form': form,
        'rota': rota
    }
    return HttpResponse(template.render(context, request))

# Deletar Rota
def deletarRota(request, id):
    rota = get_object_or_404(Rota, id=id)
    rota.delete()
    url = reverse('listarRotas') + '?sucesso_deletar=True'
    return HttpResponseRedirect(url)
