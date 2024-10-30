# Generated by Django 4.2.5 on 2024-06-04 01:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PontosTuristico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=50, verbose_name="nome")),
                ("longitude", models.CharField(max_length=50)),
                ("latitude", models.CharField(max_length=50)),
                ("estado", models.CharField(max_length=150)),
                (
                    "imagem",
                    models.ImageField(
                        upload_to="uploads/", verbose_name="Insira a foto"
                    ),
                ),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Rota",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=100, verbose_name="Nome da Rota")),
                ("descricao", models.TextField(verbose_name="Descrição da Rota")),
                (
                    "mapas_relacao",
                    models.ManyToManyField(
                        related_name="rotas",
                        to="mapas.pontosturistico",
                        verbose_name="Pontos Turísticos",
                    ),
                ),
            ],
        ),
    ]