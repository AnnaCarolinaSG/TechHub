from django.shortcuts import get_object_or_404, render, redirect
from .models import Area, Categoria, Conteudo
from django.db.models import Q
from .forms import ConteudoForm, CriarConteudoCategoriaForm


def home(request):
    areas = Area.objects.all()

    contexto = {
        "areas": areas,
    }

    return render(
        request,
        "estudos/index.html",
        contexto
    )


def area_detail(request, area_slug):
    area = get_object_or_404(Area, slug=area_slug)

    categorias = area.categorias.all()

    contexto = {
        "area": area,
        "categorias": categorias,
    }

    return render(
        request,
        "estudos/area_detail.html",
        contexto
    )

def categoria_detail(request, area_slug, categoria_slug):
    area = get_object_or_404(Area, slug=area_slug)

    categoria = get_object_or_404(
        area.categorias,
        slug=categoria_slug
    )

    conteudos = categoria.conteudos.all()

    contexto = {
        "area": area,
        "categoria": categoria,
        "conteudos": conteudos,
    }

    return render(
        request,
        "estudos/categoria_detail.html",
        contexto
    )

def conteudo_detail(request, area_slug, categoria_slug, conteudo_slug):
    area = get_object_or_404(
        Area,
        slug=area_slug
    )

    categoria = get_object_or_404(
        area.categorias,
        slug=categoria_slug
    )

    conteudo = get_object_or_404(
        categoria.conteudos,
        slug=conteudo_slug
    )

    contexto = {
        "area": area,
        "categoria": categoria,
        "conteudo": conteudo,
    }

    return render(
        request,
        "estudos/conteudo_detail.html",
        contexto
    )
def criar_conteudo(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    if request.method == "POST":

        form = CriarConteudoCategoriaForm(request.POST)

        if form.is_valid():

            conteudo = form.save(commit=False)

            conteudo.categoria = categoria
            conteudo.publicado = True

            conteudo.save()

            return redirect(
                "categoria_detail",
                area_slug=categoria.area.slug,
                categoria_slug=categoria.slug
            )

    else:

        form = CriarConteudoCategoriaForm()

    contexto = {
        "form": form,
        "categoria": categoria,
        "area": categoria.area,
    }

    return render(
        request,
        "estudos/criar_conteudo.html",
        contexto
    )

def gerenciar(request):

    form = ConteudoForm()

    if request.method == "POST":

        tipo = request.POST.get("tipo")

        if tipo == "area":

            nome = request.POST.get("nome")
            descricao = request.POST.get("descricao")
            icone = request.POST.get("icone")

            Area.objects.create(
                nome=nome,
                descricao=descricao,
                icone=icone
            )

        elif tipo == "categoria":

            nome = request.POST.get("nome")
            descricao = request.POST.get("descricao")
            area_id = request.POST.get("area")

            area = get_object_or_404(
                Area,
                id=area_id
            )

            Categoria.objects.create(
                nome=nome,
                descricao=descricao,
                area=area
            )

        elif tipo == "conteudo":

            form = ConteudoForm(request.POST)

            if form.is_valid():

                conteudo = form.save(commit=False)

                conteudo.publicado = True

                conteudo.save()

                form = ConteudoForm()

    areas = Area.objects.all()

    categorias = Categoria.objects.select_related(
        "area"
    ).all()

    conteudos = Conteudo.objects.select_related(
        "categoria",
        "categoria__area"
    ).all()

    contexto = {
        "areas": areas,
        "categorias": categorias,
        "conteudos": conteudos,
        "form": form,
    }

    return render(
        request,
        "estudos/gerenciar.html",
        contexto
    )

def editar_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    if request.method == "POST":

        categoria.nome = request.POST.get("nome")
        categoria.descricao = request.POST.get("descricao")

        categoria.save()

        return redirect(
            "area_detail",
            area_slug=categoria.area.slug
        )

    contexto = {
        "categoria": categoria
    }

    return render(
        request,
        "estudos/editar_categoria.html",
        contexto
    )

def editar_area(request, area_id):

    area = get_object_or_404(
        Area,
        id=area_id
    )

    if request.method == "POST":

        area.nome = request.POST.get("nome")
        area.descricao = request.POST.get("descricao")
        area.icone = request.POST.get("icone")

        area.save()

        return redirect("home")

    contexto = {
        "area": area
    }

    return render(
        request,
        "estudos/editar_area.html",
        contexto
    )

def editar_conteudo(request, conteudo_id):

    conteudo = get_object_or_404(
        Conteudo,
        id=conteudo_id
    )

    if request.method == "POST":

        form = ConteudoForm(
            request.POST,
            instance=conteudo
        )

        if form.is_valid():

            form.save()

            return redirect(
                "categoria_detail",
                area_slug=conteudo.categoria.area.slug,
                categoria_slug=conteudo.categoria.slug
            )

    else:

        form = ConteudoForm(
            instance=conteudo
        )

    contexto = {
        "conteudo": conteudo,
        "form": form,
    }

    return render(
        request,
        "estudos/editar_conteudo.html",
        contexto
    )

def excluir_categoria(request, categoria_id):

    categoria = get_object_or_404(
        Categoria,
        id=categoria_id
    )

    area_slug = categoria.area.slug

    if request.method == "POST":
        categoria.delete()

        return redirect(
            "area_detail",
            area_slug=area_slug
        )

    return redirect(
        "area_detail",
        area_slug=area_slug
    )

def excluir_area(request, area_id):

    area = get_object_or_404(
        Area,
        id=area_id
    )

    if request.method == "POST":

        area.delete()

        return redirect("home")

    return redirect("home")

def excluir_conteudo(request, conteudo_id):

    conteudo = get_object_or_404(
        Conteudo,
        id=conteudo_id
    )

    area_slug = conteudo.categoria.area.slug
    categoria_slug = conteudo.categoria.slug

    if request.method == "POST":

        conteudo.delete()

        return redirect(
            "categoria_detail",
            area_slug=area_slug,
            categoria_slug=categoria_slug
        )

    return redirect(
        "categoria_detail",
        area_slug=area_slug,
        categoria_slug=categoria_slug
    )

def buscar(request):

    termo = request.GET.get("q", "").strip()

    areas = Area.objects.none()
    categorias = Categoria.objects.none()
    conteudos = Conteudo.objects.none()

    if termo:

        areas = Area.objects.filter(
            Q(nome__icontains=termo) |
            Q(descricao__icontains=termo)
        )

        categorias = Categoria.objects.filter(
            Q(nome__icontains=termo) |
            Q(descricao__icontains=termo)
        ).select_related("area")

        conteudos = Conteudo.objects.filter(
            Q(titulo__icontains=termo) |
            Q(conteudo__icontains=termo)
        ).select_related(
            "categoria",
            "categoria__area"
        ).distinct()

    contexto = {
        "termo": termo,
        "areas": areas,
        "categorias": categorias,
        "conteudos": conteudos,
    }

    return render(
        request,
        "estudos/buscar.html",
        contexto
    )