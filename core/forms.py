from django import forms
from .models import Pedido
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

class PediditoForm(forms.Form):
    # Define los campos necesarios para generar un pedido
    nombre_origen = forms.CharField(label='Nombre Origen')
    direccion_origen = forms.CharField(label='Dirección Origen')
    nombre_destino = forms.CharField(label='Nombre Destino')
    direccion_destino = forms.CharField(label='Dirección Destino')