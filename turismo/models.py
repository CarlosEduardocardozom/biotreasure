from django.db import models
from django.forms import ModelForm

class Animais(models.Model):
    ESTADO_CHOICES = (
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins")
    )

    nomeCientifico = models.CharField(max_length=50, verbose_name='nomeCientifico')
    nomeComum = models.CharField(max_length=50, verbose_name='nomeComum')
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, blank=False, verbose_name='Estado')
    fotoAnimal = models.ImageField(upload_to="uploads/", verbose_name="Insira sua foto") 

    def __str__(self):
        return self.nomeCientifico
    class Meta:
        ordering=['nomeCientifico']

class pontoConcentracao(models.Model):
    longitude = models.CharField(max_length=50, verbose_name='Longitude')
    latitude = models.CharField(max_length=50, verbose_name='Latitude')
    
    def __str__(self):
        return self.longitude
    class Meta:
        ordering=['longitude']

class AnimaisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['nomeCientifico'].widget.attrs.update({'class': 'form-control'})
        self.fields['nomeComum'].widget.attrs.update({'class': 'form-control'})
        self.fields['estado'].widget.attrs.update({'class': 'form-control'})
        self.fields['fotoAnimal'].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Animais
        fields =['nomeCientifico', 'nomeComum', 'estado', 'fotoAnimal']

class Identificar(models.Model):
    imagemAnimal = models.ImageField(upload_to="uploads/", verbose_name="Faça upload da foto")

class IdentificarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['imagemAnimal'].widget.attrs.update({'class': 'form-control'})
    class Meta:
        model = Identificar
        fields =['imagemAnimal']
