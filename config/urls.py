from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from estudos.views import (home, area_detail, categoria_detail, conteudo_detail, gerenciar, editar_area, editar_categoria, editar_conteudo, excluir_categoria, excluir_area, excluir_conteudo, buscar, criar_conteudo)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("gerenciar/", gerenciar, name="gerenciar"),
    path("buscar/", buscar, name="buscar"),
    path("categoria/<int:categoria_id>/criar-conteudo/", criar_conteudo, name="criar_conteudo"),
    path("<slug:area_slug>/", area_detail, name="area_detail"),
    path("<slug:area_slug>/<slug:categoria_slug>/", categoria_detail, name="categoria_detail"),
    path("<slug:area_slug>/<slug:categoria_slug>/<slug:conteudo_slug>/",conteudo_detail,name="conteudo_detail"),
    path("gerenciar/categoria/<int:categoria_id>/editar/",editar_categoria,name="editar_categoria"),
    path("gerenciar/area/<int:area_id>/editar/", editar_area, name="editar_area"),
    path("gerenciar/conteudo/<int:conteudo_id>/editar/", editar_conteudo, name="editar_conteudo"),
    path("gerenciar/categoria/<int:categoria_id>/excluir/", excluir_categoria, name="excluir_categoria"),
    path("gerenciar/area/<int:area_id>/excluir/", excluir_area, name="excluir_area"),
    path("gerenciar/conteudo/<int:conteudo_id>/excluir/", excluir_conteudo, name="excluir_conteudo"),
    
]

urlpatterns += [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)