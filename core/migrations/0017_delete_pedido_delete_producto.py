# Generated by Django 4.2.1 on 2023-06-20 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_pedidos_correo_destino'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pedido',
        ),
        migrations.DeleteModel(
            name='Producto',
        ),
    ]