from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    ESTADOS = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activo')

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    precio = models.IntegerField()
    cupo_maximo = models.IntegerField()
    fecha_realizacion = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Reserva(models.Model):
    ESTADOS_PAGO = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE)
    fecha_inscripcion = models.CharField(max_length=50)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='Pendiente')

    def __str__(self):
        return f"{self.usuario.username} - {self.experiencia.titulo}"