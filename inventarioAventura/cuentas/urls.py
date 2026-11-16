from django.urls import path
from cuentas.views import SignUpView, mi_perfil, usuariosData, crearUsuario, editarUsuario, eliminarUsuario

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('perfil/', mi_perfil, name='mi_perfil'),
    path('usuarios/', usuariosData, name='usuariosData'),
    path('crearUsuario/', crearUsuario, name='crearUsuario'),
    path('editarUsuario/<int:id>', editarUsuario, name='editarUsuario'),
    path('eliminarUsuario/<int:id>', eliminarUsuario, name='eliminarUsuario'),
]