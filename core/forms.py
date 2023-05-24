from django import forms
from .models import Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'estado', 'direccion_envio', 'metodo_pago', 'total', 'codigo_seguimiento']

class CustomUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not username or not email or not password1 or not password2:
            raise forms.ValidationError('Por favor, complete todos los campos.')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden. Por favor, inténtelo de nuevo.')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso. Por favor, elija otro.')
        return username