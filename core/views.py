from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PedidoForm, PedidosForm
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
from rest_framework import status
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from rest_framework.generics import GenericAPIView





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
def perfil(request):
    return render(request, 'core/perfil.html')


class PedidoView(GenericAPIView):
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
        form = PedidosForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)  # Guardar el formulario sin guardar en la base de datos todavía
            pedido.fecha_pedido = timezone.now()  # Establecer la fecha del pedido como la fecha actual
            pedido.save()
            # Realizar cualquier otra acción que necesites con el pedido creado
            return redirect(to= "lista_pedidos")  # Redirigir a la página de éxito o a otra vista
    else:
        form = PedidosForm()

    return render(request, 'core/generar_pedido.html', {'form': form})

def seguimiento_pedido(request):
    if request.method == 'POST':
        codigo_seguimiento = request.POST.get('codigo_seguimiento')
        # Realiza la solicitud GET a la API con el código de seguimiento
        url_seguimiento = f'https://musicpro.bemtorres.win/api/v1/transporte/seguimiento/{codigo_seguimiento}'
        response = requests.get(url_seguimiento)

        if response.status_code == 200:
            result = response.json().get('result')
            estado_pedido = result.get('estado')
            solicitud = result.get('solicitud')
            direccion_origen = solicitud.get('direccion_origen')
            direccion_destino = solicitud.get('direccion_destino')

            context = {
                'estado_pedido': estado_pedido,
                'direccion_origen': direccion_origen,
                'direccion_destino': direccion_destino
            }

            return render(request, 'core/seguimiento_pedido.html', context)
        else:
            return HttpResponse("Error al obtener el estado del pedido")

    return render(request, 'core/seguimiento_pedido.html')

def lista_pedidos(request):
    pedidos = Pedidos.objects.all()
    return render(request, 'core/lista_pedidos.html', {'pedidos': pedidos})

class PedidosView(viewsets.ModelViewSet):
    serializer_class = PedidosSerializer
    queryset = Pedidos.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Creamos el pedido
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

def modificar_pedido(request, codigo_seguimiento):
    pedido = get_object_or_404(Pedidos, codigo_seguimiento=codigo_seguimiento)

    if request.method == 'POST':
        form = PedidosForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            # Realiza cualquier acción adicional después de modificar el pedido
            return redirect('lista_pedidos')  # Redirige a la página de la lista de pedidos actualizada
    else:
        form = PedidosForm(instance=pedido)

    return render(request, 'core/modificar_pedido.html', {'form': form, 'pedido': pedido})

def eliminar_pedido(request, codigo_seguimiento):
    pedido = get_object_or_404(Pedidos, codigo_seguimiento=codigo_seguimiento)
    pedido.delete()
    # Realiza cualquier acción adicional después de eliminar el pedido
    return redirect('lista_pedidos')  # Redirige a la página de la lista de pedidos actualizada


def enviar_correo(request):
    if request.method == 'POST':
        asunto = request.POST.get('asunto')
        correo = request.POST.get('correo')
        contenido = request.POST.get('contenido')
        foto = request.FILES.get('foto')

        # Crear el mensaje de correo electrónico
        mensaje = MIMEMultipart()
        mensaje['Subject'] = asunto
        mensaje['From'] = 'victormanuelnf12@gmail.com'  # Reemplaza con tu dirección de correo
        mensaje['To'] = correo

        # Agregar el contenido del correo electrónico
        mensaje.attach(MIMEText(contenido, 'plain'))

        # Adjuntar la foto al correo electrónico
        foto_adjunta = MIMEImage(foto.read())
        foto_adjunta.add_header('Content-Disposition', 'attachment', filename='foto.jpg')
        mensaje.attach(foto_adjunta)

        # Enviar el correo electrónico
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)  # Reemplaza con los detalles de tu servidor SMTP
        servidor_smtp.starttls()
        servidor_smtp.login('victormanuelnf12@gmail.com', 'wsodusmjigsdoiia')  # Reemplaza con tus credenciales de correo
        servidor_smtp.send_message(mensaje)
        servidor_smtp.quit()

        return HttpResponse('Correo enviado exitosamente')
    else:
        return render(request, 'core/enviar_correo.html')