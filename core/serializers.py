from rest_framework import serializers
from .models import *
import requests


class PedidoSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'

    def get_productos(self, obj):
        productos = obj.producto.all()
        productos_nombres = [producto.nombre for producto in productos]
        return productos_nombres


class PedidosSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Pedidos
        fields = '__all__'
        extra_kwargs = {
            'codigo_seguimiento': {'read_only': True},
        }