from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cuentas.models import Perfil
from experiencias.models import Categoria, Experiencia, Reserva

@login_required
def index(request):
    perfil, created = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'rol': 'Administrador' if request.user.is_superuser else 'Turista', 'telefono': 'Sin registrar'}
    )
    if request.user.is_superuser and perfil.rol != 'Administrador':
        perfil.rol = 'Administrador'
        perfil.save()

    data = {
        'perfil': perfil,
        'total_categorias': Categoria.objects.count(),
        'total_experiencias': Experiencia.objects.count(),
        'total_reservas': Reserva.objects.count(),
    }
    return render(request, 'core/index.html', data)