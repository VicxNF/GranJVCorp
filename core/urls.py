from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required
from rest_framework import routers, permissions
from django.contrib.auth import views as auth_view
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Documentacion API',
        default_version= 'v1',
        description= 'Pedidos de GranJVCorp',
        terms_of_service= 'https://www.google.com/policies/terms/',
        contact= openapi.Contact(email="contact@snippets.local"),
        license= openapi.License(name="BSD License"),
    ),
    public= True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register(r'pedidos', PedidosView,'pedidos')


urlpatterns = [
    path('home/', home, name='home'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include(router.urls), name='api-agregar-pedido'),
    path('docs/', include_docs_urls(title="Pedidos API"), name='docs'),
    path('login/', auth_view.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('administrador/', login_required(administrador), name='administrador'),
    path('modificar-pedido/<codigo_seguimiento>', modificar_pedido, name="modificar_pedido"),
    path('eliminar-pedido/<codigo_seguimiento>', eliminar_pedido, name="eliminar_pedido"),
    path('perfil/', perfil, name='perfil'),
    path('saludo/', obtener_colaborador, name='saludo'),
    path('generar_pedido/', generar_pedido, name='generar_pedido'),
    path('seguimiento_pedido/', seguimiento_pedido, name='seguimiento_pedido'),
    path('lista_pedidos/', lista_pedidos, name='lista_pedidos'),
    path('enviar_correo/', enviar_correo, name='enviar_correo'),
    path('completar_pedido/<str:codigo_seguimiento>/', completar_pedido, name='completar_pedido'),

]