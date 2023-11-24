# Generated by Django 3.2.6 on 2023-11-23 04:10

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0043_auto_20231116_0305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_seccion_arbolsaf', ckeditor.fields.RichTextField(default='Escriba su texto aquí', verbose_name='Texto pestaña Arbolsaf')),
                ('texto_seccion_creditos', ckeditor.fields.RichTextField(default='Escriba los créditos', verbose_name='Texto pestaña Créditos')),
                ('texto_seccion_descargo_responsabilidad', ckeditor.fields.RichTextField(default='Escriba el texto', verbose_name='Texto pestaña Descargo de responsabilidad')),
                ('texto_seccion_agradecimientos', ckeditor.fields.RichTextField(default='Escriba el texto', verbose_name='Texto pestaña Descargo de responsabilidad')),
            ],
            options={
                'verbose_name': 'Configuración',
                'verbose_name_plural': 'Configuración Textos',
                'db_table': 'arbolsaf_configuracion',
                'managed': True,
            },
        ),
        migrations.AlterModelOptions(
            name='bitacora',
            options={'managed': True, 'ordering': ['-created'], 'verbose_name': 'Bitacora', 'verbose_name_plural': 'Bitacora'},
        ),
        migrations.AlterModelOptions(
            name='familymodel',
            options={'managed': True, 'ordering': ['familia'], 'verbose_name': 'Familia', 'verbose_name_plural': 'Familias'},
        ),
        migrations.AlterModelOptions(
            name='gendermodel',
            options={'managed': True, 'ordering': ['genero'], 'verbose_name': 'Género', 'verbose_name_plural': 'Género'},
        ),
        migrations.AlterModelOptions(
            name='measureunittypemodel',
            options={'managed': True, 'ordering': ['abreviatura'], 'verbose_name': 'Tipo unidad de medidas', 'verbose_name_plural': 'Tipos unidad de medidas'},
        ),
        migrations.AlterModelOptions(
            name='referencemodel',
            options={'managed': True, 'ordering': ['fuente_final'], 'verbose_name': 'Referencia', 'verbose_name_plural': 'Referencias'},
        ),
        migrations.AlterModelOptions(
            name='registroreporteherramienta',
            options={'managed': True, 'ordering': ['-created'], 'verbose_name': 'Registro reporte herramienta', 'verbose_name_plural': 'Registros reporte herramienta'},
        ),
        migrations.AlterModelOptions(
            name='synonymousmodel',
            options={'managed': True, 'ordering': ['sinonimo'], 'verbose_name': 'Sinónimo', 'verbose_name_plural': 'Sinónimo'},
        ),
        migrations.AlterModelOptions(
            name='variabletypefamilymodel',
            options={'managed': True, 'ordering': ['nombre'], 'verbose_name': 'Grupo de variable', 'verbose_name_plural': 'Grupos de variables'},
        ),
        migrations.AlterField(
            model_name='variabletypemodel',
            name='tipo_variables',
            field=models.CharField(blank=True, choices=[('boolean', 'Boolean'), ('cualitativo', 'Cualitativo'), ('numerico', 'Numérico'), ('rango', 'Rango'), ('texto', 'Texto')], max_length=50, null=True, verbose_name='tipo variable'),
        ),
    ]
