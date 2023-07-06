from django import forms
from .models import Pedidos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

User = get_user_model()


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not user.is_active:
                raise ValidationError("Las credenciales de inicio de sesión no son válidas.")


class PedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['lugar_origen', 'nombre_origen', 'direccion_origen', 'nombre_destino', 'direccion_destino','correo_destino']

class ModificarPedidosForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['lugar_origen', 'nombre_origen', 'direccion_origen', 'nombre_destino', 'direccion_destino','correo_destino', 'estado']
