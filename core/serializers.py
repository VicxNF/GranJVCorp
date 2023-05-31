from rest_framework import serializers
from .models import *
import requests


class PedidoSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'  # Incluir todos los campos del modelo

    def get_productos(self, obj):
        productos_ids = obj.producto.all().values_list('id', flat=True)
        response = requests.get('https://musicpro.bemtorres.win/api/v1/bodega/producto')
        if response.status_code == 200:
            productos = response.json().get('productos', [])
            productos_dict = {producto['id']: producto['nombre'] for producto in productos}
            nombres_productos = [productos_dict.get(producto_id) for producto_id in productos_ids]
            return nombres_productos
        return []




