from django import forms
from .models import Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'estado', 'direccion_envio', 'metodo_pago', 'total', 'codigo_seguimiento']
        widgets = {
            'producto': forms.CheckboxSelectMultiple()
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}
