from rest_framework import serializers
from .models import *
import requests




class PedidosSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Pedidos
        fields = '__all__'
        extra_kwargs = {
            'codigo_seguimiento': {'read_only': True},
        }