from django import forms
from .models import Pedidos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}

class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['nombre_conductor', 'direccion_origen', 'nombre_destino', 'direccion_destino','correo_destino', 'estado']