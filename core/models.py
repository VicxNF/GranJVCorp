from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string
from django.utils import timezone
import random
import string
from faker import Faker

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo de correo electrónico es obligatorio.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Añadir los argumentos related_name a los campos de relación
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set'  # Nuevo related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set'  # Nuevo related_name
    )

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class Pedidos(models.Model):
    ESTADO_CHOICES = (
        ('En preparacion', 'En preparacion'),
        ('En camino', 'En camino'),
        ('Completado', 'Completado'),
    )
    LUGAR_ORIGEN = (
        ('Bodega', 'Bodega'),
        ('Sucursal', 'Sucursal'),
    )
    codigo_seguimiento = models.CharField(primary_key=True, unique=True, max_length=50)
    nombre_conductor = models.CharField(max_length=100, default='')
    lugar_origen = models.CharField(max_length=20, choices=LUGAR_ORIGEN, default='Bodega', verbose_name='Lugar de origen')
    nombre_origen = models.CharField(max_length=100, default='')
    direccion_origen = models.CharField(max_length=100, default='')
    nombre_destino = models.CharField(max_length=100, default='')
    direccion_destino = models.CharField(max_length=200, default='')
    correo_destino = models.EmailField(max_length=254, default='')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En preparacion', verbose_name='Estado del Pedido')

    def __str__(self):
        return self.codigo_seguimiento

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:  # Si no se ha proporcionado un código de seguimiento
            # Generar el código de seguimiento automáticamente
            codigo = 'JV' + ''.join(random.choices(string.digits, k=5))
            while Pedidos.objects.filter(codigo_seguimiento=codigo).exists():  # Verificar que el código no esté en uso
                codigo = 'JV' + ''.join(random.choices(string.digits, k=5))

            self.codigo_seguimiento = codigo

        if not self.nombre_conductor:
            # Generar un nombre de conductor aleatorio con faker
            fake = Faker()
            self.nombre_conductor = fake.name()

        super().save(*args, **kwargs)