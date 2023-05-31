from django import forms
from .models import Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class PedidoForm(ModelForm):
    producto_id = forms.IntegerField(label='ID del producto')
    class Meta:
        model = Pedido
        fields = ['usuario', 'estado', 'direccion_envio', 'metodo_pago', 'total', 'codigo_seguimiento','producto_id']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}
