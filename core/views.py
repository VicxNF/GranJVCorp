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
            pedido = form.save(commit=False)  # Guardar el formulario sin guardar en la base de datos todavía
            pedido.fecha_pedido = timezone.now()  # Establecer la fecha del pedido como la fecha actual
            pedido.save()
            # Realizar cualquier otra acción que necesites con el pedido creado
            return redirect(to= "lista_pedidos")  # Redirigir a la página de éxito o a otra vista
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
        servidor_smtp.login('granjvcorp@gmail.com', 'lrexvhtfrsdjgnek')  # Reemplaza con tus credenciales de correo
        servidor_smtp.send_message(mensaje)
        servidor_smtp.quit()

        return redirect('lista_pedidos')
    else:
        return render(request, 'core/enviar_correo.html')

def completar_pedido(request, codigo_seguimiento):
    pedido = Pedidos.objects.get(codigo_seguimiento=codigo_seguimiento)
    pedido.estado = 'Completado'
    pedido.save()
    return redirect('enviar_correo')

@api_view(['GET'])
def obtener_estado_pedido(request, codigo_seguimiento):
    try:
        pedido = Pedidos.objects.get(codigo_seguimiento=codigo_seguimiento)
        estado = pedido.estado
        return Response({'estado': estado})
    except Pedidos.DoesNotExist:
        return Response(status=404, data={'error': 'Pedido no encontrado'})