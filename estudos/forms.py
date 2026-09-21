from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Conteudo


class ConteudoForm(forms.ModelForm):

    class Meta:

        model = Conteudo

        fields = (
            "titulo",
            "categoria",
            "conteudo",
        )

        widgets = {
            "conteudo": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5"
                },
                config_name="extends"
            )
        }

class CriarConteudoCategoriaForm(forms.ModelForm):

    class Meta:

        model = Conteudo

        fields = (
            "titulo",
            "conteudo",
        )

        widgets = {
            "conteudo": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5"
                },
                config_name="extends"
            )
        }