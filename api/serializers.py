from rest_framework import serializers
from core.models import Pedidos


class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'