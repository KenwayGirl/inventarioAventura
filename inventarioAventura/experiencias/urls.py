from django.urls import path
from experiencias.views import *

urlpatterns = [
    path('categorias/', categoriasData, name='categoriasData'),
    path('crearCategoria/', crearCategoria, name='crearCategoria'),
    path('editarCategoria/<int:id>', editarCategoria, name='editarCategoria'),
    path('eliminarCategoria/<int:id>', eliminarCategoria, name='eliminarCategoria'),

    path('experiencias/', experienciasData, name='experienciasData'),
    path('crearExperiencia/', crearExperiencia, name='crearExperiencia'),
    path('editarExperiencia/<int:id>', editarExperiencia, name='editarExperiencia'),
    path('eliminarExperiencia/<int:id>', eliminarExperiencia, name='eliminarExperiencia'),

    path('reservas/', reservasData, name='reservasData'),
    path('inscribir/<int:id>', inscribirExperiencia, name='inscribirExperiencia'),
    path('cambiarPago/<int:id>', cambiarPagoReserva, name='cambiarPagoReserva'),
    path('eliminarReserva/<int:id>', eliminarReserva, name='eliminarReserva'),
]