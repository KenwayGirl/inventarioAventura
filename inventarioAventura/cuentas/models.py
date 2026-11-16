from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Guia', 'Guía / Operador'),
        ('Turista', 'Turista / Cliente'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=30, choices=ROLES, default='Turista')
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"