import datetime
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cuentas.models import Perfil
from experiencias.models import Categoria, Experiencia, Reserva
from experiencias.forms import CategoriaForm, ExperienciaForm

def obtener_perfil(user):
    perfil, _ = Perfil.objects.get_or_create(
        usuario=user,
        defaults={'rol': 'Administrador' if user.is_superuser else 'Turista', 'telefono': '-'}
    )
    if user.is_superuser and perfil.rol != 'Administrador':
        perfil.rol = 'Administrador'
        perfil.save()
    return perfil

# 1. CRUD DE CATEGORÍAS (ADMIN)

@login_required
def categoriasData(request):
    perfil = obtener_perfil(request.user)
    if perfil.rol != 'Administrador':
        return HttpResponseRedirect(reverse('home'))

    categorias = Categoria.objects.all()
    data = {'categorias': categorias, 'perfil': perfil}
    return render(request, 'experiencias/categorias.html', data)

@login_required
def crearCategoria(request):
    perfil = obtener_perfil(request.user)
    if perfil.rol != 'Administrador':
        return HttpResponseRedirect(reverse('home'))

    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('categoriasData'))

    data = {'form': form, 'perfil': perfil, 'titulo': 'Crear Categoría'}
    return render(request, 'experiencias/registroCategoria.html', data)

@login_required
def editarCategoria(request, id):
    perfil = obtener_perfil(request.user)
    if perfil.rol != 'Administrador':
        return HttpResponseRedirect(reverse('home'))

    categoria = Categoria.objects.get(id=id)
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('categoriasData'))

    data = {'form': form, 'perfil': perfil, 'titulo': 'Editar Categoría'}
    return render(request, 'experiencias/registroCategoria.html', data)

@login_required
def eliminarCategoria(request, id):
    perfil = obtener_perfil(request.user)
    if perfil.rol == 'Administrador':
        categoria = Categoria.objects.get(id=id)
        categoria.delete()
    return HttpResponseRedirect(reverse('categoriasData'))


# 2. CRUD EXPERIENCIAS POR ROL

@login_required
def experienciasData(request):
    perfil = obtener_perfil(request.user)

    if perfil.rol == 'Administrador':
        experiencias = Experiencia.objects.all()
    elif perfil.rol == 'Guia':
        experiencias = Experiencia.objects.filter(creador=request.user)
    else:
        experiencias = Experiencia.objects.filter(categoria__estado='Activo')

    data = {'experiencias': experiencias, 'perfil': perfil}
    return render(request, 'experiencias/experiencias.html', data)

@login_required
def crearExperiencia(request):
    perfil = obtener_perfil(request.user)
    if perfil.rol not in ['Administrador', 'Guia']:
        return HttpResponseRedirect(reverse('experienciasData'))

    form = ExperienciaForm()
    if request.method == 'POST':
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.creador = request.user
            experiencia.save()
            return HttpResponseRedirect(reverse('experienciasData'))

    data = {'form': form, 'perfil': perfil, 'titulo': 'Registrar Experiencia'}
    return render(request, 'experiencias/registroExperiencia.html', data)

@login_required
def editarExperiencia(request, id):
    perfil = obtener_perfil(request.user)
    experiencia = Experiencia.objects.get(id=id)

    if perfil.rol == 'Guia' and experiencia.creador != request.user:
        return HttpResponseRedirect(reverse('experienciasData'))
    if perfil.rol == 'Turista':
        return HttpResponseRedirect(reverse('experienciasData'))

    form = ExperienciaForm(instance=experiencia)
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('experienciasData'))

    data = {'form': form, 'perfil': perfil, 'titulo': 'Editar Experiencia'}
    return render(request, 'experiencias/registroExperiencia.html', data)

@login_required
def eliminarExperiencia(request, id):
    perfil = obtener_perfil(request.user)
    if perfil.rol == 'Administrador':
        experiencia = Experiencia.objects.get(id=id)
        experiencia.delete()
    return HttpResponseRedirect(reverse('experienciasData'))


# 3. GESTIÓN DE RESERVAS / INSCRIPCIONES

@login_required
def reservasData(request):
    perfil = obtener_perfil(request.user)

    if perfil.rol == 'Administrador':
        reservas = Reserva.objects.all()
    elif perfil.rol == 'Guia':
        reservas = Reserva.objects.filter(experiencia__creador=request.user)
    else:
        reservas = Reserva.objects.filter(usuario=request.user)

    data = {'reservas': reservas, 'perfil': perfil}
    return render(request, 'experiencias/reservas.html', data)

@login_required
def inscribirExperiencia(request, id):
    experiencia = Experiencia.objects.get(id=id)
    dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    Reserva.objects.create(
        usuario=request.user,
        experiencia=experiencia,
        fecha_inscripcion=str(dt),
        estado_pago='Pendiente'
    )
    return HttpResponseRedirect(reverse('reservasData'))

@login_required
def cambiarPagoReserva(request, id):
    reserva = Reserva.objects.get(id=id)
    if reserva.estado_pago == 'Pendiente':
        reserva.estado_pago = 'Confirmado'
    else:
        reserva.estado_pago = 'Pendiente'
    reserva.save()
    return HttpResponseRedirect(reverse('reservasData'))

@login_required
def eliminarReserva(request, id):
    reserva = Reserva.objects.get(id=id)
    reserva.delete()
    return HttpResponseRedirect(reverse('reservasData'))