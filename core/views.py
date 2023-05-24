from django.shortcuts import render, redirect
from .models import Pedido
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, 'core/home.html')

def mostrar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'core/mostrar_pedidos.html', {'pedidos': pedidos})

def agregar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mostrar_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'core/agregar_pedido.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            username = user.username
            welcome_message = f'Bienvenido/a, {username}!'
            return redirect('administrador')
        else:
            # Si las credenciales son inválidas, puedes mostrar un mensaje de error o realizar otra acción
            return render(request, 'core/login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'core/login.html')
    
def register(request):
    print("Using register.html template")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            
            # Autenticar y iniciar sesión automáticamente
            user = authenticate(request, username=username, password=form.cleaned_data['password1'])
            login(request, user)
            
            welcome_message = f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.'
            return redirect('administrador')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

#@login_required
#@staff_member_required
def administrador(request):
    # Lógica para obtener los pedidos y usuarios
    pedidos = Pedido.objects.all()
    usuarios = User.objects.all()
    
    # Mensaje de bienvenida para el usuario registrado
    username = request.user.username
    return render(request, 'core/administrador.html', {'pedidos': pedidos, 'usuarios': usuarios, 'welcome_message': messages.get_messages(request)})
