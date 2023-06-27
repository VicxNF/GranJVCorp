from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PedidosForm
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
from rest_framework.decorators import api_view
import random
import string
from faker import Faker






def home(request):
    return render(request, 'core/home.html')

    
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
    pedidos= Pedidos.objects.all()
    datos= {
        'pedidos': pedidos
    }
    return render(request, 'core/administrador.html', datos)


@login_required()
def perfil(request):
    return render(request, 'core/perfil.html')



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
def generar_pedido(request):
    if request.method == 'POST':
        form = PedidosForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.fecha_pedido = timezone.now()
            pedido.save()
            return redirect('lista_pedidos')  # Redirige a la página de éxito o a otra vista
    else:
        form = PedidosForm()

    return render(request, 'core/generar_pedido.html', {'form': form})

@login_required
def seguimiento_pedido(request):
    if request.method == 'POST':
        codigo_seguimiento = request.POST.get('codigo_seguimiento')
        try:
            pedido = Pedidos.objects.get(codigo_seguimiento=codigo_seguimiento)
            return render(request, 'core/seguimiento_pedido.html', {'pedido': pedido})
        except Pedidos.DoesNotExist:
            mensaje_error = 'Pedido no encontrado'
            return render(request, 'core/seguimiento_pedido.html', {'error': mensaje_error})
    else:
        return render(request, 'core/seguimiento_pedido.html')

@login_required
def lista_pedidos(request):
    pedidos = Pedidos.objects.all()
    form = PedidosForm()  # Crear una instancia del formulario vacío
    return render(request, 'core/lista_pedidos.html', {'pedidos': pedidos, 'form': form})

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
    
@login_required
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


@login_required
def eliminar_pedido(request, codigo_seguimiento):
    pedido = get_object_or_404(Pedidos, codigo_seguimiento=codigo_seguimiento)
    pedido.delete()
    # Realiza cualquier acción adicional después de eliminar el pedido
    return redirect('lista_pedidos')  # Redirige a la página de la lista de pedidos actualizada


@login_required
def enviar_correo(request):
    if request.method == 'POST':
        codigo_seguimiento = request.POST.get('codigo_seguimiento')
        asunto = request.POST.get('asunto')
        correo = request.POST.get('correo')
        contenido = request.POST.get('contenido')
        foto = request.FILES.get('foto')

        # Crear el mensaje de correo electrónico
        mensaje = MIMEMultipart()
        mensaje['Subject'] = asunto
        mensaje['From'] = 'granjvcorp@gmail.com'  # Reemplaza con tu dirección de correo
        mensaje['To'] = correo

        # Agregar el contenido del correo electrónico
        mensaje.attach(MIMEText(contenido, 'plain'))

        # Adjuntar la foto al correo electrónico
        foto_adjunta = MIMEImage(foto.read())
        foto_adjunta.add_header('Content-Disposition', 'attachment', filename='pedido.jpg')
        mensaje.attach(foto_adjunta)

        # Enviar el correo electrónico
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)  # Reemplaza con los detalles de tu servidor SMTP
        servidor_smtp.starttls()
        servidor_smtp.login('granjvcorp@gmail.com', 'lrexvhtfrsdjgnek')  # Reemplaza con tus credenciales de correo
        servidor_smtp.send_message(mensaje)
        servidor_smtp.quit()

        return redirect('completar_pedido', codigo_seguimiento=codigo_seguimiento)
    else:
        return render(request, 'core/enviar_correo.html')

def completar_pedido(request, codigo_seguimiento):
    try:
        pedido = Pedidos.objects.get(codigo_seguimiento=codigo_seguimiento)
        pedido.estado = 'Completado'
        pedido.save()
    except Pedidos.DoesNotExist:
        # Manejar el caso en el que no se encuentre el pedido
        pass

    return redirect('lista_pedidos')

@api_view(['GET'])
def obtener_estado_pedido(request, codigo_seguimiento):
    try:
        pedido = Pedidos.objects.get(codigo_seguimiento=codigo_seguimiento)
        estado = pedido.estado
        direccion_origen = pedido.direccion_origen
        direccion_destino = pedido.direccion_destino

        return Response({
            'estado': estado,
            'direccion_origen': direccion_origen,
            'direccion_destino': direccion_destino
        })
    except Pedidos.DoesNotExist:
        return Response(status=404, data={'error': 'Pedido no encontrado'})
    
fake = Faker()

def generar_pedidos_falsos(request):
    for _ in range(100):
        nombre_conductor = fake.name()
        direccion_origen = fake.address()
        nombre_destino = fake.name()
        direccion_destino = fake.address()
        correo_destino = fake.email()
        estado = random.choice(['En preparacion', 'En camino', 'Completado'])

        pedido = Pedidos(
            nombre_conductor=nombre_conductor,
            direccion_origen=direccion_origen,
            nombre_destino=nombre_destino,
            direccion_destino=direccion_destino,
            correo_destino=correo_destino,
            estado=estado
        )
        pedido.save()

    return render(request, 'core/generar_pedidos_falsos.html')

def eliminar_pedidos_falsos(request):
    criterios = {
        'estado': 'En preparacion', 
        'estado': 'En camino',
        'estado': 'Completado',
    }

    # Obtener los pedidos falsos basados en los criterios
    pedidos_falsos = Pedidos.objects.filter(**criterios)

    # Eliminar los pedidos falsos
    pedidos_falsos.delete()

    return redirect('lista_pedidos') 