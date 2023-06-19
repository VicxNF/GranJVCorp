from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone

class Producto(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    asset = models.URLField()
    estado = models.IntegerField()

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_CHOICES = (
        ('En preparacion', 'En preparacion'),
        ('En camino', 'En camino'),
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
    producto = models.ManyToManyField(Producto, blank=True)
    
    
    def calcular_total(self):
        return sum(producto.precio for producto in self.producto.all())

    # Otros campos adicionales según tus necesidades, como productos

    def __str__(self):
        productos = self.producto.all()
        productos_nombres = [str(producto) for producto in productos]
        nombres_productos = ", ".join(productos_nombres)
        return f"Pedido {self.codigo_seguimiento} - Usuario: {self.usuario.username} Productos: {nombres_productos}"


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