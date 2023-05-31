from rest_framework import serializers
from .models import Pedido
import requests


class PedidoSerializer(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()
    class Meta:
        model = Pedido
        fields = '__all__'
    
    def get_productos(self, obj):
        response = requests.get('https://musicpro.bemtorres.win/api/v1/bodega/producto')
        if response.status_code == 200:
            productos = response.json().get('productos', [])
            return productos
        return []