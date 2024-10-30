from django.urls import path
from .views import (
    mapas,
    cadastrarPonto,
    listarPontos,
    listarPontosJSON,
    cadastrarRotas,
    listarRotas,
    editarPonto,
    deletarPonto,
    editarRota,
    deletarRota
)

urlpatterns = [
    path('', mapas, name='mapas'),
    path('cadastrar-ponto/', cadastrarPonto, name='cadastrarPonto'),
    path('listar-pontos/', listarPontos, name='listarPontos'),
    path('listar-pontos-json/', listarPontosJSON, name='listarPontosJSON'),  # Nova URL
    path('cadastrar-rotas/', cadastrarRotas, name='cadastrarRotas'),
    path('listar-rotas/', listarRotas, name='listarRotas'),
    path('editar-ponto/<int:id>/', editarPonto, name='editarPonto'),
    path('deletar-ponto/<int:id>/', deletarPonto, name='deletarPonto'),
    path('editar-rota/<int:id>/', editarRota, name='editarRota'),
    path('deletar-rota/<int:id>/', deletarRota, name='deletarRota'),
]
