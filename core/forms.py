from django import forms
from .models import Pedido, Pedidos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'estado', 'direccion_envio', 'metodo_pago', 'codigo_seguimiento']
        widgets = {
            'producto': forms.CheckboxSelectMultiple()
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['nombre_conductor', 'direccion_origen', 'nombre_destino', 'direccion_destino', 'estado']