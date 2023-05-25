from django.urls import path, include
from api.views import *
from rest_framework.documentation import include_docs_urls
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'pedidos', PedidoView,'pedidos')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('docs/', include_docs_urls(title="Pedidos API")),
]