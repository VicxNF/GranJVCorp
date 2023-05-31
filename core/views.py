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
import requests
from django.http import JsonResponse




def home(request):
    return render(request, 'core/home.html')

@login_required()
def mostrar_pedidos(request):
    pedidos = Pedido.objects.all()
    
    context = {
        'pedidos': pedidos,
    }
    
    return render(request, 'core/mostrar_pedidos.html', context)

@login_required
def agregar_pedido(request):
    # Obtener todos los productos de la API
    response = requests.get('https://musicpro.bemtorres.win/api/v1/bodega/producto/')
    data = response.json()
    productos_api = data.get('productos', [])

    datos = {
        'form': PedidoForm(),
        'productos_api': productos_api
    }

    if request.method == 'POST':
        formulario = PedidoForm(request.POST)

        if formulario.is_valid():
            pedido = formulario.save(commit=False)

            # Obtener el ID del producto seleccionado en el formulario
            producto_id = formulario.cleaned_data['producto_id']

            # Buscar el producto correspondiente al ID en la lista de productos de la API
            producto_seleccionado = next((producto for producto in productos_api if producto['id'] == producto_id), None)

            if producto_seleccionado:
                # Asignar el producto al campo 'producto' del pedido
                pedido.producto = producto_seleccionado

            pedido.save()
            datos['mensaje'] = "Registrado correctamente"

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

def obtener_colaborador(request):
    id = request.GET.get('id')
    response = requests.get('https://musicpro.bemtorres.win/api/v1/bodega/producto/')
    data = response.json()

    colaborador = None
    if id:
        for producto in data['productos']:
            if producto['id'] == int(id):
                colaborador = producto
                break

    context = {
        'colaborador': colaborador,
        'id': id,
    }

    return render(request, 'core/saludo.html', context)


