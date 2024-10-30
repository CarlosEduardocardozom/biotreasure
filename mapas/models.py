from django.db import models
from django.forms import ModelForm, ModelMultipleChoiceField
from django import forms

# Modelo para Pontos Turisticos
class PontosTuristico(models.Model):
    nome = models.CharField(max_length=50, verbose_name="nome")
    longitude = models.CharField(max_length=50, name="longitude")
    latitude = models.CharField(max_length=50, name="latitude")
    estado = models.CharField(max_length=150, name="estado")
    imagem = models.ImageField(upload_to="uploads/", verbose_name="Insira a foto")
    
    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']

# Formulário para Pontos Turisticos
class PontosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['longitude'].widget.attrs.update({'class': 'form-control'})
        self.fields['latitude'].widget.attrs.update({'class': 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = PontosTuristico
        fields = ['nome', 'longitude', 'latitude', 'imagem']

# Modelo para Rota
class Rota(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Rota")
    descricao = models.TextField(verbose_name="Descrição da Rota")
    mapas_relacao = models.ManyToManyField(PontosTuristico, related_name='rotas', verbose_name="Pontos Turísticos")

# Formulário para Rota
class RotasForm(ModelForm):
    mapas_relacao = ModelMultipleChoiceField(
        queryset=PontosTuristico.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Pontos Turísticos"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-control'})



    class Meta:
        model = Rota
        fields = ['nome', 'descricao', 'mapas_relacao']
