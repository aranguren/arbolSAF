# Generated by Django 3.2.6 on 2023-06-21 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0020_variabletypemodel_seleccion_multiple'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variablemodel',
            name='valor_cualitativo',
        ),
    ]
