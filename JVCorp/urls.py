"""
URL configuration for JVCorp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import *
from api.urls import *
from api.views import *
from rest_framework.documentation import include_docs_urls
from django.contrib.auth import views as auth_view
from rest_framework.schemas import get_schema_view
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers, permissions

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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('pedidos/', include('core.urls')),
    path('documentacion/', schema_view.with_ui('swagger', cache_timeout=0), name='documentacion'),
    path('docs/', include_docs_urls(title="Pedidos API"), name='docs'),
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
    path('enviar_correo/', enviar_correo, name='enviar_correo'),
    path('completar_pedido/<str:codigo_seguimiento>/', completar_pedido, name='completar_pedido'),

]
    
