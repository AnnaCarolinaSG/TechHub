from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Area(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=10, default="📚")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    descricao = models.TextField(blank=True)

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="categorias"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Conteudo(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    conteudo = CKEditor5Field("Conteúdo", config_name="extends")

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="conteudos"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    publicado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo