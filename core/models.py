from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone

class Pedidos(models.Model):
    ESTADO_CHOICES = (
        ('En preparacion', 'En preparacion'),
        ('En camino', 'En camino'),
        ('Completado', 'Completado'),
    )
    codigo_seguimiento = models.CharField(primary_key=True, unique=True, max_length=50)
    nombre_conductor = models.CharField(max_length=100)
    direccion_origen = models.CharField(max_length=200)
    nombre_destino = models.CharField(max_length=100)
    direccion_destino = models.CharField(max_length=200)
    correo_destino = models.EmailField(max_length=254, default='')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En preparacion', verbose_name='Estado del Pedido')
    fecha_pedido = models.DateTimeField(default=timezone.now, verbose_name='Fecha del Pedido')

    def __str__(self):
        return self.codigo_seguimiento

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:  # Si no se ha proporcionado un código de seguimiento
            # Generar el código de seguimiento automáticamente
            codigo = 'JV' + ''.join(random.choices(string.digits, k=5))
            while Pedidos.objects.filter(codigo_seguimiento=codigo).exists():  # Verificar que el código no esté en uso
                codigo = 'JV' + ''.join(random.choices(string.digits, k=5))

            self.codigo_seguimiento = codigo

        super().save(*args, **kwargs)