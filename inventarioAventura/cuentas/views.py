from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cuentas.models import Perfil
from cuentas.forms import CustomUserCreationForm, PerfilEditarForm

# Vista de registro de usuarios
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def mi_perfil(request):
    perfil, created = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'rol': 'Administrador' if request.user.is_superuser else 'Turista', 'telefono': 'Sin registrar'}
    )
    data = {'perfil': perfil}
    return render(request, 'cuentas/mi_perfil.html', data)


@login_required
def usuariosData(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if not (request.user.is_superuser or perfil.rol == 'Administrador'):
        return HttpResponseRedirect(reverse('home'))

    # Asegurar que cada usuario tenga un perfil asociado
    for u in User.objects.all():
        Perfil.objects.get_or_create(
            usuario=u,
            defaults={'rol': 'Administrador' if u.is_superuser else 'Turista', 'telefono': '-'}
        )

    perfiles = Perfil.objects.all()
    data = {'perfiles': perfiles, 'perfil': perfil}
    return render(request, 'cuentas/usuarios.html', data)


@login_required
def crearUsuario(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if not (request.user.is_superuser or perfil.rol == 'Administrador'):
        return HttpResponseRedirect(reverse('home'))

    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('usuariosData'))

    data = {'form': form, 'perfil': perfil, 'titulo': 'Registrar Usuario'}
    return render(request, 'cuentas/registroUsuario.html', data)


@login_required
def editarUsuario(request, id):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if not (request.user.is_superuser or perfil.rol == 'Administrador'):
        return HttpResponseRedirect(reverse('home'))

    perfil_editar = Perfil.objects.get(id=id)
    form = PerfilEditarForm(instance=perfil_editar)

    if request.method == 'POST':
        form = PerfilEditarForm(request.POST, instance=perfil_editar)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('usuariosData'))

    data = {'form': form, 'perfil': perfil, 'titulo': f'Editar Rol de {perfil_editar.usuario.username}'}
    return render(request, 'cuentas/registroUsuario.html', data)


@login_required
def eliminarUsuario(request, id):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.user.is_superuser or perfil.rol == 'Administrador':
        perfil_eliminar = Perfil.objects.get(id=id)
        if perfil_eliminar.usuario != request.user:
            perfil_eliminar.usuario.delete()
    return HttpResponseRedirect(reverse('usuariosData'))