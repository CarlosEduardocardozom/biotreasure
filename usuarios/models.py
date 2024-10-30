from django.db import models
from django.forms import ModelForm 

# Create your models here.

class Usuarios(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    email = models.CharField(max_length=45, verbose_name="Email")
    senha = models.CharField(max_length=30, verbose_name="Senha")
    cpf = models.CharField(max_length=12, verbose_name="CPF")
    data_nascimento = models.DateField(max_length=8, verbose_name="Data de nascimento")
    fotoPerfil = models.ImageField(upload_to="uploads/", verbose_name="Insira sua foto")

    def __str__(self):
        return self.nome
    class Meta:
        ordering=['nome']

class UsuariosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['senha'].widget.attrs.update({'class': 'form-control'})
        self.fields['cpf'].widget.attrs.update({'class': 'form-control'})
        self.fields['data_nascimento'].widget.attrs.update({'class': 'form-control'})
        self.fields['fotoPerfil'].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Usuarios
        fields =['nome', 'email', 'senha', 'cpf', 'data_nascimento', 'fotoPerfil']

