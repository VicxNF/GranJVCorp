from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import UserRegisterForm, PedidoForm, PediditoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import *
import requests
from django.http import JsonResponse
from rest_framework.response import Response






def home(request):
    return render(request, 'core/home.html')

@login_required()
def mostrar_pedidos(request):
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        total = 0
        for producto in pedido.producto.all():
            total += producto.precio
        pedido.total = total

    context = {
        'pedidos': pedidos,
    }

    return render(request, 'core/mostrar_pedidos.html', context)


@login_required
def agregar_pedido(request):
    response = requests.get('https://musicpro.bemtorres.win/api/v1/bodega/producto/')
    data = response.json()
    productos_api = data.get('productos', [])

    if request.method == 'POST':
        formulario = PedidoForm(request.POST)
        if formulario.is_valid():
            pedido = formulario.save(commit=False)
            pedido.usuario = request.user

            # Guardar el pedido sin los productos primero
            pedido.save()

            producto_ids = request.POST.getlist('producto_id')
            productos_seleccionados = []

            for producto_id in producto_ids:
                # Buscar el producto correspondiente al ID en la lista de productos de la API
                producto_seleccionado = next(
                    (producto for producto in productos_api if producto['id'] == int(producto_id)), None)

                if producto_seleccionado:
                    # Obtener o crear el objeto Producto correspondiente al producto seleccionado
                    producto, _ = Producto.objects.get_or_create(
                        id=producto_seleccionado['id'],
                        defaults={
                            'codigo': producto_seleccionado['codigo'],
                            'nombre': producto_seleccionado['nombre'],
                            'descripcion': producto_seleccionado['descripcion'],
                            'precio': producto_seleccionado['precio'],
                            'asset': producto_seleccionado['asset'],
                            'estado': producto_seleccionado['estado']
                        }
                    )

                    productos_seleccionados.append(producto)

            pedido.producto.set(productos_seleccionados)
            pedido.save()

            datos = {
                'form': PedidoForm(),
                'productos_api': productos_api,
                'mensaje': "Registrado correctamente"
            }

            return redirect('mostrar_pedidos')

    else:
        formulario = PedidoForm()

    datos = {
        'form': formulario,
        'productos_api': productos_api
    }

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


class PedidoView(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtenemos los IDs de los productos enviados en la solicitud
        productos_ids = request.data.get('producto', [])

        # Creamos el pedido
        self.perform_create(serializer)

        # Agregamos los productos al pedido
        pedido = serializer.instance
        pedido.producto.set(productos_ids)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

@login_required
def rastrear_pedido(request):
    pedido = None

    if request.method == 'POST':
        codigo_seguimiento = request.POST.get('codigo_seguimiento')
        try:
            pedido = Pedido.objects.get(codigo_seguimiento=codigo_seguimiento)
        except Pedido.DoesNotExist:
            pedido = None

    return render(request, 'core/rastrear_pedido.html', {'pedido': pedido})

def generar_pedido(request):
    if request.method == 'POST':
        form = PediditoForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            nombre_origen = form.cleaned_data['nombre_origen']
            direccion_origen = form.cleaned_data['direccion_origen']
            nombre_destino = form.cleaned_data['nombre_destino']
            direccion_destino = form.cleaned_data['direccion_destino']
            comentario = form.cleaned_data['comentario']
            info = form.cleaned_data['info']

            # Crear el objeto JSON con los datos del formulario
            data = {
                'nombre_origen': nombre_origen,
                'direccion_origen': direccion_origen,
                'nombre_destino': nombre_destino,
                'direccion_destino': direccion_destino,
                'comentario': comentario,
                'info': info
            }

            # Realizar la solicitud POST a la API de solicitud con los datos del formulario
            url_solicitud = 'https://musicpro.bemtorres.win/api/v1/transporte/solicitud'
            response = requests.post(url_solicitud, json=data)

            # Verificar si la solicitud fue exitosa (código de respuesta 200)
            if response.status_code == 201:
                # Se generó el pedido y se obtuvo el código de seguimiento
                codigo_seguimiento = response.json()['codigo_seguimiento']
                # Aquí puedes realizar las acciones necesarias con el código de seguimiento

                # Devolver una respuesta adecuada en tu vista
                return HttpResponse(f"Código de seguimiento generado: {codigo_seguimiento}")
            else:
                # Hubo un error en la solicitud
                return HttpResponse("Error al generar el pedido")
    else:
        form = PediditoForm()

    # Renderizar la plantilla con el formulario
    return render(request, 'core/generar_pedido.html', {'form': form})

def seguimiento_pedido(request):
    if request.method == 'POST':
        codigo_seguimiento = request.POST.get('codigo_seguimiento')
        # Realiza la solicitud GET a la API con el código de seguimiento
        url_seguimiento = f'https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{codigo_seguimiento}'
        response = requests.get(url_seguimiento)

        if response.status_code == 200:
            estado_pedido = response.json().get('result')
            return render(request, 'core/seguimiento_pedido.html', {'estado_pedido': estado_pedido})
        else:
            return HttpResponse("Error al obtener el estado del pedido")

    return render(request, 'core/seguimiento_pedido.html')