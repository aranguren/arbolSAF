# Generated by Django 3.2.6 on 2023-06-16 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arbolsaf', '0015_alter_variablemodel_tipo_variable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencemodel',
            name='referencia',
            field=models.TextField(blank=True, null=True, verbose_name='Fuente'),
        ),
        migrations.AlterField(
            model_name='speciesmodel',
            name='nombre_comun',
            field=models.CharField(max_length=255, verbose_name='Nombre común'),
        ),
        migrations.AlterField(
            model_name='variablemodel',
            name='referencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='arbolsaf.referencemodel', verbose_name='Fuente'),
        ),
        migrations.AlterField(
            model_name='variablemodel',
            name='referencia_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='arbolsaf.referencemodel', verbose_name='Repetir fuente'),
        ),
        migrations.AlterField(
            model_name='variabletypemodel',
            name='tipo_variables',
            field=models.CharField(blank=True, choices=[('numerico', 'Numérico'), ('texto', 'Texto'), ('rango', 'Rango'), ('cualitativo', 'Cualitativo'), ('boolean', 'Boolean')], max_length=50, null=True, verbose_name='tipo variable'),
        ),
    ]
