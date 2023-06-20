from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from core.models import Pedidos
from rest_framework import viewsets
from .serializers import PedidosSerializer

class PedidosView(viewsets.ModelViewSet):
    serializer_class = PedidosSerializer
    queryset = Pedidos.objects.all()