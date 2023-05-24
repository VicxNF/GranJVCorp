from django.shortcuts import render, redirect, HttpResponse
from .models import Pedido
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



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


    
def register(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Las contraseñas no coinciden")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'core/register.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('administrador')
        else:
            return HttpResponse ("Credenciales incorrectas")
    return render(request, 'core/login.html')

@login_required
def administrador(request):
    pedidos= Pedido.objects.all()
    datos= {
        'pedidos': pedidos
    }
    return render(request, 'core/administrador.html', datos)