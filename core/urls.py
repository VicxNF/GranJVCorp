from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from django.contrib.auth import views as auth_view
from rest_framework.documentation import include_docs_urls


router = routers.DefaultRouter()
router.register(r'pedidos', PedidosView,'pedidos')


urlpatterns = [
    path('home/', home, name='home'),
    path('api/v1/', include(router.urls), name='api-agregar-pedido'),
    path('docs/', include_docs_urls(title="Pedidos API")),
    path('mostrar-pedidos/', mostrar_pedidos, name='mostrar_pedidos'),
    path('agregar-pedido/', agregar_pedido, name='agregar_pedido'),
    path('login/', auth_view.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('administrador/', login_required(administrador), name='administrador'),
    path('modificar-pedido/<codigo_seguimiento>', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<codigo_seguimiento>', eliminar_pedido, name="eliminar_pedido"),
    path('perfil/', perfil, name='perfil'),
    path('rastrear_pedido/', rastrear_pedido, name='rastrear_pedido'),
    path('saludo/', obtener_colaborador, name='saludo'),
    path('generar_pedido/', generar_pedido, name='generar_pedido'),
    path('seguimiento_pedido/', seguimiento_pedido, name='seguimiento_pedido'),
    path('lista_pedidos/', lista_pedidos, name='lista_pedidos'),

]