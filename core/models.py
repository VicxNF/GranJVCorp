from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('P', 'Pendiente'),
        ('E', 'En progreso'),
        ('C', 'Completado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P')
    direccion_envio = models.TextField(blank=True, null=True)
    metodo_pago = models.CharField(max_length=100, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    codigo_seguimiento = models.CharField(max_length=100, unique=True)

    # Otros campos adicionales según tus necesidades, como productos

    def __str__(self):
        return f"Pedido {self.id} - Usuario: {self.usuario.username}"
