from django.db import models

from django.db import models

class Pedido(models.Model):
    codigo_seguimiento = models.CharField(max_length=10)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo_seguimiento

