# Generated by Django 3.2.6 on 2023-11-24 18:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0045_configuracion_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracion',
            name='texto_seccion_agradecimientos',
            field=ckeditor.fields.RichTextField(default='Escriba el texto', verbose_name='Texto pestaña Agradecimientos'),
        ),
    ]
