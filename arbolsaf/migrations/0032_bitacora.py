# Generated by Django 3.2.6 on 2023-08-24 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arbolsaf', '0031_alter_speciesmodel_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha modificado')),
                ('entidad_modificada', models.CharField(choices=[('especie', 'Especie'), ('variable', 'Variable')], max_length=50, verbose_name='Entidad')),
                ('codigo_especie', models.CharField(blank=True, max_length=50, null=True, verbose_name='Código especie')),
                ('codigo_variable', models.CharField(blank=True, max_length=50, null=True, verbose_name='Código variable')),
                ('descripcion_cambio', models.TextField(verbose_name='Descripción del cambio')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Bitacora',
                'verbose_name_plural': 'Bitacoras',
                'db_table': 'arbolsaf_bitacora_cambios',
                'managed': True,
            },
        ),
    ]
