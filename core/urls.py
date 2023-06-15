from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from django.contrib.auth import views as auth_view
from rest_framework.documentation import include_docs_urls



urlpatterns = [
    path('home/', home, name='home'),
    path('api/v1/pedidos/', PedidoView.as_view({'post': 'create'}), name='api-agregar-pedido'),
    path('docs/', include_docs_urls(title="Pedidos API")),
    path('mostrar-pedidos/', mostrar_pedidos, name='mostrar_pedidos'),
    path('agregar-pedido/', agregar_pedido, name='agregar_pedido'),
    path('login/', auth_view.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('administrador/', login_required(administrador), name='administrador'),
    path('modificar-pedido/<codigo>', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<codigo>', eliminar_pedido, name="eliminar_pedido"),
    path('perfil/', perfil, name='perfil'),
    path('rastrear_pedido/', rastrear_pedido, name='rastrear_pedido'),
    path('saludo/', obtener_colaborador, name='saludo'),
    path('generar_pedido/', generar_pedido, name='generar_pedido'),
    path('seguimiento_pedido/', seguimiento_pedido, name='seguimiento_pedido'),
]