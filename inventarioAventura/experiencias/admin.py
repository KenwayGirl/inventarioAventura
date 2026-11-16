from django.contrib import admin
from experiencias.models import Categoria, Experiencia, Reserva

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'estado']

class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'precio', 'cupo_maximo', 'fecha_realizacion', 'categoria', 'creador']

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'experiencia', 'fecha_inscripcion', 'estado_pago']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Experiencia, ExperienciaAdmin)
admin.site.register(Reserva, ReservaAdmin)