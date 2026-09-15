from django.contrib import admin
from .models import Categoria, Conteudo, Area

admin.site.register(Area)
admin.site.register(Categoria)
admin.site.register(Conteudo)