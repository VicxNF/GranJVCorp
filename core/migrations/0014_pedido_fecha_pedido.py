# Generated by Django 4.2.1 on 2023-06-19 17:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_rename_nombre_origen_pedidos_nombre_conductor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha del Pedido'),
        ),
    ]
