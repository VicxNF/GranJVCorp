from django.shortcuts import render, redirect, HttpResponse
from .models import Pedido
from .forms import UserRegisterForm, PedidoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import PedidoSerializer


def home(request):
    return render(request, 'core/home.html')

@login_required()
def mostrar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'core/mostrar_pedidos.html', {'pedidos': pedidos})

@login_required()
def agregar_pedido(request):
    datos = {
        'form' : PedidoForm()
    }

    if request.method== 'POST' :
        formulario = PedidoForm(request.POST)

        if formulario.is_valid:
            
            formulario.save()
            datos['mensaje'] = "Registrado Correctamente"

        return redirect(to="mostrar_pedidos")

    return render(request, 'core/agregar_pedido.html', datos)


    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bienvenido {username}, tu cuenta fue creada exitosamente')
            return redirect('home')
    else:
        form = UserRegisterForm()


    return render(request, 'core/register.html',{'form':form})

@login_required()
def administrador(request):
    pedidos= Pedido.objects.all()
    datos= {
        'pedidos': pedidos
    }
    return render(request, 'core/administrador.html', datos)

@login_required()
def modificar_pedido(request,codigo):
    pedido = Pedido.objects.get(codigo_seguimiento=codigo)

    datos = {
        'form': PedidoForm(instance=pedido)
    }
    if request.method== 'POST':
        formulario = PedidoForm(data=request.POST,instance=pedido)
        if formulario.is_valid:
            formulario.save()
            datos['mensaje'] = "Modificacion exitosa"
        return redirect(to="mostrar_pedidos")

    return render(request, 'core/modificar_pedido.html', datos)

@login_required()
def eliminar_pedido(request, codigo):
    pedido = Pedido.objects.get(codigo_seguimiento=codigo)
    pedido.delete()

    return redirect(to="mostrar_pedidos")

@login_required()
def perfil(request):
    return render(request, 'core/perfil.html')

@login_required()
def rastrear_pedido(request):
    return render(request, 'core/rastrear_pedido.html')

class PedidoView(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()