from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('mostrar-pedidos/', mostrar_pedidos, name='mostrar_pedidos'),
    path('agregar-pedido/', agregar_pedido, name='agregar_pedido'),
    path('login/', iniciar_sesion, name='login'),
    path('register/', register, name='register'),
    path('administrador/', administrador, name='administrador'),
]