from django.urls import path,include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("", views.conta, name='main'),
    path("cadastrar", views.cadastrarUsuarios, name='cadastrarUsuarios'),
    path("listar", views.listar, name='listar'),
    path("perfil", views.perfil, name='perfil'),  # Rota para visualizar o perfil
    path("google-login/", views.google_login, name='google_login'),  # Rota para login com Google
    path("inserir/", views.inserir_usuario, name='inserir_usuario'),
    path('accounts/', include('allauth.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
