from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from api.urls import path

urlpatterns = [
    path('home/', home, name='home'),
    path('mostrar-pedidos/', mostrar_pedidos, name='mostrar_pedidos'),
    path('agregar-pedido/', agregar_pedido, name='agregar_pedido'),
    path('login/', iniciar_sesion, name='login'),
    path('register/', register, name='register'),
    path('administrador/', login_required(administrador), name='administrador'),
    path('modificar-pedido/<codigo>', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<codigo>', eliminar_pedido, name="eliminar_pedido"),
]