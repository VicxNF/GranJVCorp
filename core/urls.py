from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from api.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('home/', home, name='home'),
    path('mostrar-pedidos/', mostrar_pedidos, name='mostrar_pedidos'),
    path('agregar-pedido/', agregar_pedido, name='agregar_pedido'),
    path('login/', auth_view.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('administrador/', login_required(administrador), name='administrador'),
    path('modificar-pedido/<codigo>', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<codigo>', eliminar_pedido, name="eliminar_pedido"),
    path('perfil/', perfil, name='perfil'),
]