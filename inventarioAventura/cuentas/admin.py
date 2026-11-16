from django.contrib import admin
from cuentas.models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'rol', 'telefono']

admin.site.register(Perfil, PerfilAdmin)