# Generated by Django 4.2.1 on 2023-07-02 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_delete_pedido_delete_producto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidos',
            name='fecha_pedido',
        ),
    ]
