from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Completado', 'Completado'),
    )
    METODO_CHOICES = (
        ('Debito', 'Debito'),
        ('Credito', 'Credito'),
        ('Transferencia', 'Transferencia'),
    )

    codigo_seguimiento = models.IntegerField(primary_key=True, unique=True, verbose_name='Codigo de Seguimiento')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de pedido')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha actualizada')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name='Estado del Pedido')
    direccion_envio = models.CharField(blank=True, max_length=70, verbose_name='Direccion del pedido')
    metodo_pago = models.CharField(max_length=100, choices=METODO_CHOICES, blank=True, verbose_name='Metodo de Pago')
    total = models.IntegerField(verbose_name='Total')
    

    # Otros campos adicionales según tus necesidades, como productos

    def __str__(self):
        return f"Pedido {self.id} - Usuario: {self.usuario.username}"
