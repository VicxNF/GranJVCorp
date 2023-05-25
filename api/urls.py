from django.urls import path, include
from api.views import *


urlpatterns = [
    path('lista_pedidos', lista_pedidos, name="lista_pedidos"),
    path('detalle_pedido/<codigo>', detalle_pedido, name="detalle_pedido")
]